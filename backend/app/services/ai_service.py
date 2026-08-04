# import json
# from google import genai

# from app.core.config import settings

# client = genai.Client(api_key=settings.gemini_api_key)

# REWRITE_PROMPT = """You are a journalist rewriting a news article in your own words for a different publication.

# Rules:
# - Do not copy sentences verbatim from the source.
# - Keep all facts, names, numbers, and dates accurate.
# - Write in clear, neutral journalistic style.
# - Output ONLY valid JSON, no markdown, no commentary, no ```json fences.

# Source title: {title}
# Source content:
# {content}

# Return JSON with exactly these keys:
# {{
#   "headline": "string",
#   "summary": "one sentence, max 200 characters",
#   "article": "full rewritten article, 3-6 paragraphs",
#   "category": "one word or short phrase, e.g. Politics, Weather, Sports, Business",
#   "tags": ["array", "of", "3-6", "keywords"]
# }}
# """


# def rewrite_article(title: str, content: str) -> dict:
#     prompt = REWRITE_PROMPT.format(title=title, content=content[:8000])

#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=prompt,
#     )

#     raw = response.text.strip()

#     # Gemini sometimes wraps output in ```json fences despite instructions — strip if present
#     if raw.startswith("```"):
#         raw = raw.split("```")[1]
#         if raw.startswith("json"):
#             raw = raw[4:]
#         raw = raw.strip()

#     return json.loads(raw)

import json
from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

REWRITE_PROMPT = """You are a journalist rewriting a news article in your own words for a different publication.

Rules:
- Do not copy sentences verbatim from the source.
- Keep all facts, names, numbers, and dates accurate.
- Write in clear, neutral journalistic style.
- Output ONLY valid JSON, no markdown, no commentary.

Source title: {title}
Source content:
{content}

Return JSON with exactly these keys:
{{
  "headline": "string",
  "summary": "one sentence, max 200 characters",
  "article": "full rewritten article, 3-6 paragraphs",
  "category": "one word or short phrase, e.g. Politics, Weather, Sports, Business",
  "tags": ["array", "of", "3-6", "keywords"]
}}
"""


def rewrite_article(title: str, content: str) -> dict:
    prompt = REWRITE_PROMPT.format(title=title, content=content[:8000])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    raw = response.choices[0].message.content
    return json.loads(raw)