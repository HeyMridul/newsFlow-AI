# app/services/scraper_service.py
import httpx
from readability import Document
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
}


def scrape_article(url: str) -> dict:
    try:
        response = httpx.get(url, timeout=15, follow_redirects=True, headers=HEADERS)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise ValueError(
            f"Could not fetch article — the site returned {e.response.status_code}. "
            f"It may be blocking automated requests."
        ) from e
    except httpx.RequestError as e:
        raise ValueError(f"Network error while fetching article: {e}") from e

    doc = Document(response.text)
    title = doc.title()
    content_html = doc.summary()

    soup = BeautifulSoup(content_html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    if not text.strip():
        raise ValueError("Could not extract readable article content from this page.")

    # Extract image URLs from the article body, resolving relative URLs to absolute
    image_urls = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            absolute_url = httpx.URL(src, base=url)
            image_urls.append(str(absolute_url))

    return {
        "title": title,
        "text": text,
        "source_url": url,
        "image_urls": image_urls[:5],  # cap at 5 to avoid downloading dozens of tracking pixels/icons
    }