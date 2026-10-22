-- Schema definition for ঞ (Nya) — Vocal for Local
-- PostgreSQL 16 with pgvector and Full-Text Search (tsvector)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Permitted Source Registry
CREATE TABLE IF NOT EXISTS source_registry (
    id VARCHAR(36) PRIMARY KEY,
    domain VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    base_url VARCHAR(512) NOT NULL,
    crawl_allowed BOOLEAN NOT NULL DEFAULT TRUE,
    robots_txt_url VARCHAR(512),
    license_info VARCHAR(255) DEFAULT 'Public Web / Fair Indexing',
    language_focus VARCHAR(50) DEFAULT 'as',
    rate_limit_delay FLOAT DEFAULT 1.5,
    is_authoritative BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Indexed Documents with Full-Text Search
CREATE TABLE IF NOT EXISTS indexed_documents (
    id VARCHAR(36) PRIMARY KEY,
    url VARCHAR(1024) UNIQUE NOT NULL,
    canonical_url VARCHAR(1024) NOT NULL,
    title VARCHAR(512) NOT NULL,
    body_text TEXT NOT NULL,
    snippet TEXT NOT NULL,
    language VARCHAR(50) DEFAULT 'as',
    source_id VARCHAR(36) REFERENCES source_registry(id) ON DELETE SET NULL,
    content_hash VARCHAR(64) NOT NULL,
    published_date TIMESTAMP WITH TIME ZONE,
    indexed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_removed BOOLEAN NOT NULL DEFAULT FALSE,
    -- Full-text search tsvector column
    tsv_content tsvector GENERATED ALWAYS AS (
        to_tsvector('simple', coalesce(title, '') || ' ' || coalesce(body_text, ''))
    ) STORED
);

-- Indexes for performance and takedown compliance
CREATE INDEX IF NOT EXISTS idx_docs_language ON indexed_documents(language);
CREATE INDEX IF NOT EXISTS idx_docs_canonical ON indexed_documents(canonical_url);
CREATE INDEX IF NOT EXISTS idx_docs_hash ON indexed_documents(content_hash);
CREATE INDEX IF NOT EXISTS idx_docs_removed ON indexed_documents(is_removed);
CREATE INDEX IF NOT EXISTS idx_docs_tsv ON indexed_documents USING GIN (tsv_content);

-- 3. Feedback Submissions (Privacy Preserving: raw queries hashed)
CREATE TABLE IF NOT EXISTS feedback (
    id VARCHAR(36) PRIMARY KEY,
    query_hash VARCHAR(64) NOT NULL,
    result_id VARCHAR(36),
    feedback_type VARCHAR(50) NOT NULL,
    is_positive BOOLEAN,
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_feedback_hash ON feedback(query_hash);

-- 4. AI Usage and Cost Audit Table
CREATE TABLE IF NOT EXISTS ai_usage_log (
    id VARCHAR(36) PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    estimated_cost_usd FLOAT DEFAULT 0.0,
    status VARCHAR(50) NOT NULL
);
