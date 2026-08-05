"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchNewsList } from "@/lib/api";
import Link from "next/link";

export default function Home() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["news"],
    queryFn: fetchNewsList,
  });

  if (isLoading) return <main className="p-8">Loading...</main>;
  if (isError) return <main className="p-8 text-red-600">Failed to load news.</main>;

  return (
    <main className="p-8 max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-6">
  <h1 className="text-2xl font-bold">NewsFlow AI — Dashboard</h1>
  <div className="flex gap-2">
    <Link href="/news/generate" className="border px-4 py-2 rounded text-sm hover:bg-gray-50">
      🔗 From URL
    </Link>
    <Link href="/news/upload" className="border px-4 py-2 rounded text-sm hover:bg-gray-50">
    📷 From Image
  </Link>
    <Link href="/news/new" className="bg-black text-white px-4 py-2 rounded text-sm">
      + New News
    </Link>
  </div>
</div>
      <div className="space-y-4">
        {data?.map((item) => (
          <Link key={item.id} href={`/news/${item.id}`}>
            <div className="border rounded-lg p-4">
              <div className="flex justify-between items-start">
                <h2 className="font-semibold text-lg">{item.headline}</h2>
                <span className="text-xs px-2 py-1 bg-gray-100 rounded">
                  {item.status}
                </span>
              </div>
              {item.summary && <p className="text-gray-600 mt-1">{item.summary}</p>}
              <p className="text-xs text-gray-400 mt-2">
                {item.category ?? "Uncategorized"} · {new Date(item.created_at).toLocaleDateString()}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}