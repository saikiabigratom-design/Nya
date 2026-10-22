/**
 * Shared TypeScript Contracts for ঞ (Nya) — Vocal for Local
 */

export type LanguageType = 'all' | 'as_native' | 'as_romanized' | 'en' | 'mixed';

export type SafeSearchLevel = 'off' | 'moderate' | 'strict';

export type DateFilter = 'all' | 'past_24h' | 'past_week' | 'past_month' | 'past_year';

export type SortOption = 'newest' | 'relevance';

export type AIAnswerStatus =
  | 'grounded'
  | 'insufficient_evidence'
  | 'disabled'
  | 'budget_exceeded'
  | 'rate_limited'
  | 'authentication_failed'
  | 'timeout'
  | 'configuration_error'
  | 'provider_unavailable'
  | 'validation_failed';

export interface CitationItem {
  citation_index: number;
  document_id: string;
  title: string;
  url: string;
  source_name: string;
  source_domain: string;
  snippet: string;
  quote?: string;
}

export interface AIAnswer {
  answer: string;
  status: AIAnswerStatus;
  citations: CitationItem[];
  latency_ms: number;
  confidence: number;
  disclaimer?: string;
  model_name?: string;
  request_id?: string;
  error_code?: string;
  retry_after_seconds?: number;
}

export interface SearchResultItem {
  id: string;
  title: string;
  url: string;
  display_url: string;
  snippet: string;
  language: string;
  published_date?: string;
  published_at?: string;
  updated_at?: string;
  crawled_at?: string;
  is_news?: boolean;
  score: number;
  source_name: string;
  source_domain: string;
  is_authoritative: boolean;
}

export interface SearchResponse {
  query: string;
  normalized_query: string;
  detected_language: LanguageType;
  transliteration_suggestion?: string;
  spelling_suggestion?: string;
  total_results: number;
  page: number;
  page_size: number;
  latency_ms: number;
  sort?: SortOption;
  is_time_sensitive_query?: boolean;
  has_fresh_results?: boolean;
  freshness_notice?: string;
  results: SearchResultItem[];
  ai_answer?: AIAnswer;
  related_queries: string[];
  empty_index_notice?: string;
}

export interface FeedbackRequest {
  query: string;
  result_id?: string;
  feedback_type: 'relevance' | 'ai_quality' | 'broken_link' | 'privacy' | 'other';
  is_positive?: boolean;
  comment?: string;
}

export interface HealthStatus {
  status: string;
  version: string;
  database_connected: boolean;
  ai_provider: string;
  ai_budget_remaining_usd: number;
  indexed_documents_count: number;
  timestamp: string;
}
