// frontend/app/news/upload/page.tsx
"use client";

import { useState, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { AxiosError } from "axios";
import { generateFromImage } from "@/lib/api";
import Image from "next/image";

export default function UploadImage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const mutation = useMutation({
    mutationFn: generateFromImage,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["news"] });
      router.push(`/news/${data.id}`);
    },
  });

  function handleFile(selected: File | null) {
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    mutation.mutate(file);
  }

  return (
    <main className="p-8 max-w-2xl mx-auto">
      <Link href="/" className="text-sm text-blue-500 hover:underline">
        ← Back to dashboard
      </Link>
      <h1 className="text-2xl font-bold mt-4 mb-2">Generate from Image</h1>
      <p className="text-gray-500 text-sm mb-6">
        Upload a photo, screenshot, or newspaper clipping. AI will read and rewrite it as a draft.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setIsDragging(false);
            handleFile(e.dataTransfer.files?.[0] ?? null);
          }}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition ${
            isDragging ? "border-black bg-gray-50" : "border-gray-300"
          }`}
        >
          {preview ? (
           <div className="relative w-full h-64 mx-auto">
           <Image
           src={preview}
           alt="Preview"
           fill
           className="object-contain rounded"
           unoptimized
           />
           </div>
          ) : (
            <p className="text-gray-500">Click to browse or drag an image here</p>
          )}
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            title="Upload image"
            className="hidden"
            onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
          />
        </div>

        {mutation.isPending && (
          <div className="text-sm text-gray-500 flex items-center gap-2">
            <span className="animate-spin h-4 w-4 border-2 border-gray-400 border-t-transparent rounded-full inline-block" />
            Reading text from image and rewriting with AI — this can take 10–20 seconds...
          </div>
        )}

        {mutation.isError && (
          <p className="text-red-600 text-sm">
            {mutation.error instanceof AxiosError
              ? mutation.error.response?.data?.detail ?? "Failed to process image."
              : "Failed to process image."}
          </p>
        )}

        <button
          type="submit"
          disabled={mutation.isPending || !file}
          className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {mutation.isPending ? "Processing..." : "Generate Article"}
        </button>
      </form>
    </main>
  );
}