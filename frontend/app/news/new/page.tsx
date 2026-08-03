"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createNews } from "@/lib/api";

export default function NewNews() {
  const router = useRouter();
  const queryClient = useQueryClient();

  const [headline, setHeadline] = useState("");
  const [summary, setSummary] = useState("");
  const [article, setArticle] = useState("");
  const [category, setCategory] = useState("");
  const [language, setLanguage] = useState("en");

  const mutation = useMutation({
    mutationFn: createNews,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["news"] });
      router.push(`/news/${data.id}`);
    },
  });

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    mutation.mutate({
      headline,
      summary: summary || undefined,
      article: article || undefined,
      category: category || undefined,
      language,
    });
  }

  return (
    <main className="p-8 max-w-2xl mx-auto">
      <Link href="/" className="text-sm text-blue-500 hover:underline">
        ← Back to dashboard
      </Link>
      <h1 className="text-2xl font-bold mt-4 mb-6">Create News</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="headline" className="block text-sm font-medium mb-1">
            Headline *
          </label>
          <input
            id="headline"
            required
            placeholder="Enter headline"
            title="Headline"
            value={headline}
            onChange={(e) => setHeadline(e.target.value)}
            className="w-full border rounded px-3 py-2 bg-transparent"
          />
        </div>

        <div>
          <label htmlFor="summary" className="block text-sm font-medium mb-1">
            Summary
          </label>
          <input
            id="summary"
            placeholder="Enter summary"
            title="Summary"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            className="w-full border rounded px-3 py-2 bg-transparent"
          />
        </div>

        <div>
          <label htmlFor="article" className="block text-sm font-medium mb-1">
            Article
          </label>
          <textarea
            id="article"
            placeholder="Write the article"
            title="Article"
            value={article}
            onChange={(e) => setArticle(e.target.value)}
            rows={6}
            className="w-full border rounded px-3 py-2 bg-transparent"
          />
        </div>

        <div className="flex gap-4">
          <div className="flex-1">
            <label htmlFor="category" className="block text-sm font-medium mb-1">
              Category
            </label>
            <input
              id="category"
              placeholder="Enter category"
              title="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full border rounded px-3 py-2 bg-transparent"
            />
          </div>
          <div className="flex-1">
            <label htmlFor="language" className="block text-sm font-medium mb-1">
              Language
            </label>
            <select
              id="language"
              title="Language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full border rounded px-3 py-2 bg-transparent"
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
            </select>
          </div>
        </div>

        {mutation.isError && (
          <p className="text-red-600 text-sm">Failed to create news. Check console for details.</p>
        )}

        <button
          type="submit"
          disabled={mutation.isPending}
          className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {mutation.isPending ? "Saving..." : "Create News"}
        </button>
      </form>
    </main>
  );
}