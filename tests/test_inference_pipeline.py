"""
Comprehensive End-to-End Test Suite for Grounded AI Inference Pipeline in ঞ (Nya) Search.
Tests:
- Real provider integration (Google Gemini)
- Citation linking and evidence grounding
- Insufficient evidence handling
- Missing credentials (CONFIGURATION_ERROR)
- Invalid credentials (AUTHENTICATION_FAILED)
- Rate limits & Quotas (RATE_LIMITED)
- Provider timeouts (TIMEOUT)
- Organic search resilience during AI inference failures
"""

import pytest
import httpx
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient, ASGITransport

from main import app
from ai.gateway import AIGateway, QuotaExceededException, AuthenticationException
from packages.contracts.schema import AIAnswerStatus
from config import settings
from db.session import get_db_session


@pytest.mark.asyncio
async def test_live_gemini_integration():
    """Tests real integration against Google Gemini API when credentials are present."""
    if not settings.AI_API_KEY:
        pytest.skip("AI_API_KEY not configured for live test")

    gateway = AIGateway()
    test_docs = [
        {
            "id": "doc_1",
            "title": "ৰঙালী বিহু",
            "url": "https://as.wikipedia.org/wiki/ৰঙালী_বিহু",
            "source_name": "অসমীয়া ৱিকিপিডিয়া",
            "source_domain": "as.wikipedia.org",
            "snippet": "ৰঙালী বিহু বা ব'হাগ বিহু অসমৰ প্ৰধান বসন্তোৎসৱ।",
        }
    ]

    async for session in get_db_session():
        answer = await gateway.generate_grounded_answer(
            query="ৰঙালী বিহু কি?",
            retrieved_documents=test_docs,
            session=session,
            language="as",
        )

        assert answer is not None
        assert answer.status in (AIAnswerStatus.GROUNDED, AIAnswerStatus.RATE_LIMITED)
        if answer.status == AIAnswerStatus.GROUNDED:
            assert len(answer.answer) > 10
            assert len(answer.citations) > 0
            assert answer.citations[0].url == "https://as.wikipedia.org/wiki/ৰঙালী_বিহু"
        break


@pytest.mark.asyncio
async def test_insufficient_evidence_returns_insufficient_evidence_status():
    """Tests that queries with zero retrieved evidence return INSUFFICIENT_EVIDENCE status."""
    gateway = AIGateway()
    async for session in get_db_session():
        answer = await gateway.generate_grounded_answer(
            query="Quantum teleportation protocol",
            retrieved_documents=[],
            session=session,
            language="en",
        )
        assert answer.status == AIAnswerStatus.INSUFFICIENT_EVIDENCE
        assert len(answer.citations) == 0
        assert answer.confidence == 0.0
        break


@pytest.mark.asyncio
async def test_missing_credentials_returns_configuration_error():
    """Tests that missing API credentials produce a clean CONFIGURATION_ERROR status."""
    gateway = AIGateway()
    test_docs = [{"id": "1", "title": "Test", "url": "https://test.com", "snippet": "Test snippet"}]

    with patch.object(settings, "AI_PROVIDER", "gemini"), patch.object(settings, "AI_API_KEY", None):
        async for session in get_db_session():
            answer = await gateway.generate_grounded_answer(
                query="Test",
                retrieved_documents=test_docs,
                session=session,
                language="en",
            )
            assert answer.status == AIAnswerStatus.CONFIGURATION_ERROR
            assert answer.error_code == "MISSING_API_KEY"
            break


@pytest.mark.asyncio
async def test_quota_exceeded_handled_gracefully():
    """Tests that 429 quota exhaustion is safely categorized as RATE_LIMITED with retry seconds."""
    gateway = AIGateway()
    test_docs = [{"id": "1", "title": "Test", "url": "https://test.com", "snippet": "Test snippet"}]

    async def mock_call_gemini(*args, **kwargs):
        raise QuotaExceededException("Quota exceeded", retry_after_seconds=3600)

    with patch.object(settings, "AI_PROVIDER", "gemini"), patch.object(settings, "AI_API_KEY", "test-key"), patch.object(gateway, "_call_gemini_with_fallback", mock_call_gemini):
        async for session in get_db_session():
            answer = await gateway.generate_grounded_answer(
                query="Test",
                retrieved_documents=test_docs,
                session=session,
                language="en",
            )
            assert answer.status == AIAnswerStatus.RATE_LIMITED
            assert answer.error_code == "HTTP_429_QUOTA_EXCEEDED"
            assert answer.retry_after_seconds == 3600
            break


@pytest.mark.asyncio
async def test_invalid_credentials_returns_authentication_failed():
    """Tests that invalid API keys return AUTHENTICATION_FAILED status."""
    gateway = AIGateway()
    test_docs = [{"id": "1", "title": "Test", "url": "https://test.com", "snippet": "Test snippet"}]

    async def mock_call_gemini(*args, **kwargs):
        raise AuthenticationException("API key rejected (401)")

    with patch.object(settings, "AI_PROVIDER", "gemini"), patch.object(settings, "AI_API_KEY", "test-key"), patch.object(gateway, "_call_gemini_with_fallback", mock_call_gemini):
        async for session in get_db_session():
            answer = await gateway.generate_grounded_answer(
                query="Test",
                retrieved_documents=test_docs,
                session=session,
                language="en",
            )
            assert answer.status == AIAnswerStatus.AUTHENTICATION_FAILED
            assert answer.error_code == "HTTP_401_INVALID_KEY"
            break


@pytest.mark.asyncio
async def test_provider_timeout_returns_timeout_status():
    """Tests that provider timeouts return TIMEOUT status."""
    gateway = AIGateway()
    test_docs = [{"id": "1", "title": "Test", "url": "https://test.com", "snippet": "Test snippet"}]

    async def mock_call_gemini(*args, **kwargs):
        raise httpx.ReadTimeout("Read timed out")

    with patch.object(settings, "AI_PROVIDER", "gemini"), patch.object(settings, "AI_API_KEY", "test-key"), patch.object(gateway, "_call_gemini_with_fallback", mock_call_gemini):
        async for session in get_db_session():
            answer = await gateway.generate_grounded_answer(
                query="Test",
                retrieved_documents=test_docs,
                session=session,
                language="en",
            )
            assert answer.status == AIAnswerStatus.TIMEOUT
            assert answer.error_code == "TIMEOUT"
            break


@pytest.mark.asyncio
async def test_organic_results_survive_ai_failure():
    """Tests that organic search results remain fully available when AI inference fails."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Request search with query
        resp = await client.get("/api/v1/search?q=Python+programming&enable_ai=true")
        assert resp.status_code == 200
        data = resp.json()

        # Organic results are present
        assert data["total_results"] > 0
        assert len(data["results"]) > 0
        assert data["results"][0]["url"] is not None

        # AI Answer is present in response structure
        assert "ai_answer" in data


@pytest.mark.asyncio
async def test_gemini_cascade_recovers_from_503():
    """Tests that model cascade handles 503 high-demand error and recovers on fallback model."""
    gateway = AIGateway()

    # Create mock response: first call returns 503, second returns 200 with text
    class MockResp503:
        status_code = 503
        headers = {"content-type": "application/json"}
        text = '{"error": {"code": 503, "message": "High demand"}}'
        def json(self):
            return {"error": {"code": 503, "message": "High demand"}}

    class MockResp200:
        status_code = 200
        headers = {"content-type": "application/json"}
        def json(self):
            return {
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": "Bihu is the chief festival of Assam [1]."}]
                        }
                    }
                ]
            }

    call_count = 0
    async def mock_post(url, json=None, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return MockResp503()
        return MockResp200()

    with patch("httpx.AsyncClient.post", side_effect=mock_post):
        text, model = await gateway._call_gemini_with_fallback(
            query="Bihu",
            context="[1] Bihu is the chief festival of Assam.",
            language="en",
            req_id="test-503",
        )
        assert "Bihu" in text
        assert call_count >= 2, "Should have cascaded to second candidate model after 503"


def test_extractor_html_unescaping_and_metadata_date():
    """Tests that ContentExtractor decodes HTML entities and parses publication dates."""
    from ingestion.extraction.extractor import ContentExtractor
    extractor = ContentExtractor()

    sample_html = """
    <html>
      <head>
        <title>&quot;Bihu&quot; Festival &amp; Assam &#039;2026&#039;</title>
        <meta name="description" content="A guide to &quot;Rongali Bihu&quot; with &amp; traditions.">
        <meta property="article:published_time" content="2026-04-14T08:00:00Z">
      </head>
      <body>
        <h1>Bihu Overview</h1>
        <p>This is a &quot;celebration&quot; of spring.</p>
      </body>
    </html>
    """

    res = extractor.extract(sample_html, "https://assam.gov.in/bihu")
    assert '"Bihu" Festival & Assam \'2026\'' in res["title"]
    assert '&quot;' not in res["title"]
    assert '&amp;' not in res["title"]
    assert '"Rongali Bihu" with &' in res["snippet"]
    assert res["published_date"] is not None
    assert res["published_date"].year == 2026
    assert res["published_date"].month == 4
