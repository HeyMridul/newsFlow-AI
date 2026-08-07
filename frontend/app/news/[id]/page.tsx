"use client";

import Image from "next/image";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { fetchNewsById, mediaUrl } from "@/lib/api";
import Link from "next/link";

export default function NewsDetail() {
  const params = useParams<{ id: string }>();
  const { data, isLoading, isError } = useQuery({
    queryKey: ["news", params.id],
    queryFn: () => fetchNewsById(params.id),
  });

  if (isLoading) return <main className="p-8">Loading...</main>;
  if (isError || !data) return <main className="p-8 text-red-600">News item not found.</main>;

  return (
    <main className="p-8 max-w-3xl mx-auto">
      <Link href="/" className="text-sm text-blue-500 hover:underline">
        ← Back to dashboard
      </Link>
      <h1 className="text-3xl font-bold mt-4 mb-2">{data.headline}</h1>
      <div className="text-sm text-gray-500 mb-6">
        {data.category ?? "Uncategorized"} · {data.status} ·{" "}
        {new Date(data.created_at).toLocaleDateString()}
      </div>

      {data.media?.length > 0 && (
        <div className="mb-6">
          <div className="relative w-full h-80 rounded overflow-hidden mb-3">
            <Image
              src={mediaUrl(
                data.media.find((m) => m.is_featured)?.file_path ?? data.media[0].file_path
              )}
              alt={data.headline}
              fill
              className="object-cover"
              unoptimized
            />
          </div>
          {data.media.length > 1 && (
            <div className="flex gap-2 overflow-x-auto">
              {data.media.map((m) => (
                <div key={m.id} className="relative w-24 h-24 shrink-0 rounded overflow-hidden">
                  <Image src={mediaUrl(m.file_path)} alt="" fill className="object-cover" unoptimized />
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {data.summary && <p className="text-lg text-gray-600 mb-4">{data.summary}</p>}
      {data.article && <p className="whitespace-pre-line">{data.article}</p>}
    </main>
  );
}