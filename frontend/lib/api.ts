import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export interface NewsItem {
  id: string;
  headline: string;
  summary: string | null;
  article: string | null;
  status: string;
  language: string;
  source: string | null;
  category: string | null;
  created_at: string;
  updated_at: string;
}

export async function fetchNewsList(): Promise<NewsItem[]> {
  const res = await api.get<NewsItem[]>("/news");
  return res.data;
}

export async function fetchNewsById(id: string): Promise<NewsItem> {
  const res = await api.get<NewsItem>(`/news/${id}`);
  return res.data;
}

export interface NewsCreateInput {
  headline: string;
  summary?: string;
  article?: string;
  language?: string;
  source?: string;
  category?: string;
}

export async function createNews(data: NewsCreateInput): Promise<NewsItem> {
  const res = await api.post<NewsItem>("/news", data);
  return res.data;
}

export async function generateFromUrl(url: string): Promise<NewsItem> {
  const res = await api.post<NewsItem>("/news/generate-from-url", { url });
  return res.data;
}