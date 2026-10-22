"""
Shared Data Contracts for ঞ (Nya) — Vocal for Local.
Defines Pydantic v2 data models for API requests, search results, AI citations,
source registry, and evaluation metrics.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


class LanguageType(str, Enum):
    ALL = "all"
    ASSAMESE_NATIVE = "as_native"
    ASSAMESE_ROMANIZED = "as_romanized"
    ENGLISH = "en"
    MIXED = "mixed"


class SafeSearchLevel(str, Enum):
    OFF = "off"
    MODERATE = "moderate"
    STRICT = "strict"


class DateFilter(str, Enum):
    ALL = "all"
    PAST_24H = "past_24h"
    PAST_WEEK = "past_week"
    PAST_MONTH = "past_month"
    PAST_YEAR = "past_year"


class AIAnswerStatus(str, Enum):
    GROUNDED = "grounded"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    DISABLED = "disabled"
    BUDGET_EXCEEDED = "budget_exceeded"
    RATE_LIMITED = "rate_limited"
    AUTHENTICATION_FAILED = "authentication_failed"
    TIMEOUT = "timeout"
    CONFIGURATION_ERROR = "configuration_error"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    VALIDATION_FAILED = "validation_failed"


class SortOption(str, Enum):
    NEWEST = "newest"
    RELEVANCE = "relevance"


class CitationItem(BaseModel):
    citation_index: int = Field(description="1-based index corresponding to [1], [2], etc.")
    document_id: str
    title: str
    url: str
    source_name: str
    source_domain: str
    snippet: str
    quote: Optional[str] = None


class AIAnswer(BaseModel):
    answer: str
    status: AIAnswerStatus
    citations: List[CitationItem] = Field(default_factory=list)
    latency_ms: float = 0.0
    confidence: float = 0.0
    disclaimer: Optional[str] = None
    model_name: Optional[str] = None
    request_id: Optional[str] = None
    error_code: Optional[str] = None
    retry_after_seconds: Optional[int] = None


class SearchResultItem(BaseModel):
    id: str
    title: str
    url: str
    display_url: str
    snippet: str
    language: str
    published_date: Optional[str] = None
    published_at: Optional[str] = None
    updated_at: Optional[str] = None
    crawled_at: Optional[str] = None
    is_news: bool = False
    score: float
    source_name: str
    source_domain: str
    is_authoritative: bool = False


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=250)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)
    language: LanguageType = LanguageType.ALL
    safe_search: SafeSearchLevel = SafeSearchLevel.MODERATE
    date_filter: DateFilter = DateFilter.ALL
    sort: SortOption = SortOption.NEWEST
    enable_ai: bool = True


class SearchResponse(BaseModel):
    query: str
    normalized_query: str
    detected_language: LanguageType
    transliteration_suggestion: Optional[str] = None
    spelling_suggestion: Optional[str] = None
    total_results: int
    page: int
    page_size: int
    latency_ms: float
    sort: SortOption = SortOption.NEWEST
    is_time_sensitive_query: bool = False
    has_fresh_results: bool = True
    freshness_notice: Optional[str] = None
    results: List[SearchResultItem] = Field(default_factory=list)
    ai_answer: Optional[AIAnswer] = None
    related_queries: List[str] = Field(default_factory=list)
    empty_index_notice: Optional[str] = None


class FeedbackRequest(BaseModel):
    query: str
    result_id: Optional[str] = None
    feedback_type: str = Field(description="'relevance', 'ai_quality', 'broken_link', 'privacy', 'other'")
    is_positive: Optional[bool] = None
    comment: Optional[str] = Field(default=None, max_length=1000)


class FeedbackResponse(BaseModel):
    success: bool
    message: str


class HealthStatus(BaseModel):
    status: str
    version: str
    database_connected: bool
    ai_provider: str
    ai_budget_remaining_usd: float
    indexed_documents_count: int
    timestamp: str
