/**
 * Search API Client for ঞ (Nya) — Vocal for Local.
 */

import {
  SearchResponse,
  FeedbackRequest,
  HealthStatus,
  LanguageType,
  DateFilter,
  SafeSearchLevel,
  SortOption,
} from "@/types/contracts";

export const getApiBaseUrl = (): string => {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "");
  }
  // When running in browser (client-side), relative path calls the current origin
  if (typeof window !== "undefined") {
    return "";
  }
  // During local development SSR fallback
  return "http://127.0.0.1:8000";
};

const API_BASE_URL = getApiBaseUrl();

export async function fetchSearch(params: {
  query: string;
  page?: number;
  pageSize?: number;
  language?: LanguageType;
  dateFilter?: DateFilter;
  safeSearch?: SafeSearchLevel;
  sort?: SortOption;
  enableAi?: boolean;
  signal?: AbortSignal;
}): Promise<SearchResponse> {
  const queryParams = new URLSearchParams();
  queryParams.set("q", params.query);
  if (params.page) queryParams.set("page", params.page.toString());
  if (params.pageSize) queryParams.set("page_size", params.pageSize.toString());
  if (params.language) queryParams.set("language", params.language);
  if (params.dateFilter) queryParams.set("date_filter", params.dateFilter);
  if (params.safeSearch) queryParams.set("safe_search", params.safeSearch);
  queryParams.set("sort", params.sort || "newest");
  if (params.enableAi !== undefined) queryParams.set("enable_ai", params.enableAi.toString());

  const response = await fetch(`${API_BASE_URL}/api/v1/search?${queryParams.toString()}`, {
    method: "GET",
    headers: {
      "Accept": "application/json",
    },
    signal: params.signal,
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Search request failed with status: ${response.status}`);
  }

  return response.json();
}

export async function submitFeedback(payload: FeedbackRequest): Promise<{ success: boolean; message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/feedback`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Feedback submission failed with status: ${response.status}`);
  }

  return response.json();
}

export async function fetchHealth(): Promise<HealthStatus> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
    method: "GET",
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Health check failed with status: ${response.status}`);
  }

  return response.json();
}
