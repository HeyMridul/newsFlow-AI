"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { generateFromUrl } from "@/lib/api";
import { AxiosError } from "axios";

export default function GenerateFromUrl() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [url, setUrl] = useState("");

  const mutation = useMutation({
    mutationFn: generateFromUrl,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["news"] });
      router.push(`/news/${data.id}`);
    },
  });

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) return;
    mutation.mutate(url.trim());
  }

  return (
    <main className="p-8 max-w-2xl mx-auto">
      <Link href="/" className="text-sm text-blue-500 hover:underline">
        ← Back to dashboard
      </Link>
      <h1 className="text-2xl font-bold mt-4 mb-2">Generate from URL</h1>
      <p className="text-gray-500 text-sm mb-6">
        Paste a news article link. AI will extract and rewrite it as a draft.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          required
          type="url"
          placeholder="https://example.com/news-article"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full border rounded px-3 py-2 bg-transparent"
        />

        {mutation.isPending && (
          <div className="text-sm text-gray-500 flex items-center gap-2">
            <span className="animate-spin h-4 w-4 border-2 border-gray-400 border-t-transparent rounded-full inline-block" />
            Scraping and rewriting with AI — this can take 10–20 seconds...
          </div>
        )}

        {mutation.isError && (
          <p className="text-red-600 text-sm">
            {mutation.error instanceof AxiosError
            ? mutation.error.response?.data?.detail ?? "Failed to generate article."
            : "Failed to generate article."}
          </p>
        )}

        <button
          type="submit"
          disabled={mutation.isPending}
          className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {mutation.isPending ? "Generating..." : "Generate Article"}
        </button>
      </form>
    </main>
  );
}