"""
Multilingual Search and Grounded AI Evaluation Harness for ঞ (Nya).
Measures:
- nDCG@10 for Native Assamese, Romanized Assamese, English, and Mixed Queries
- AI Citation Precision and Fabrication Count
"""

import sys
from pathlib import Path
import math
import asyncio
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure services and repo root are in python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "services" / "search-api"))
sys.path.insert(0, str(root_dir))

from db.session import async_session_factory, init_db
from nlp.query_processor import QueryProcessor
from search.retrieval import RetrievalEngine
from ai.gateway import AIGateway
from evaluation.benchmark_dataset import EVALUATION_QUERIES


def compute_dcg(relevance_scores: List[float], k: int = 10) -> float:
    """Compute Discounted Cumulative Gain at rank k."""
    dcg = 0.0
    for i, rel in enumerate(relevance_scores[:k], start=1):
        if rel > 0:
            dcg += (2.0 ** rel - 1.0) / math.log2(i + 1.0)
    return dcg


def compute_ndcg(retrieved_urls: List[str], expected_urls: List[str], k: int = 10) -> float:
    """Computes Normalized Discounted Cumulative Gain (nDCG@k)."""
    # Grade relevance: 2 for exact URL match, 1 for domain match, 0 otherwise
    rel_scores = []
    expected_domains = {u.split("/")[2] for u in expected_urls if "/" in u}

    for url in retrieved_urls[:k]:
        if url in expected_urls:
            rel_scores.append(2.0)
        elif any(d in url for d in expected_domains):
            rel_scores.append(1.0)
        else:
            rel_scores.append(0.0)

    actual_dcg = compute_dcg(rel_scores, k)

    # Ideal DCG: best possible ranking of expected matches
    ideal_scores = sorted([2.0] * len(expected_urls), reverse=True)
    if not ideal_scores:
        return 1.0

    idcg = compute_dcg(ideal_scores, k)
    if idcg == 0.0:
        return 0.0

    return min(1.0, actual_dcg / idcg)


async def run_evaluation():
    """Runs end-to-end evaluation benchmark over the indexed documents."""
    print("=" * 70)
    print("ঞ (Nya) — Vocal for Local: Multilingual Benchmark Evaluation")
    print("=" * 70)

    await init_db()
    qp = QueryProcessor()
    retrieval = RetrievalEngine()
    ai = AIGateway()

    category_scores: Dict[str, List[float]] = {
        "as_native": [],
        "as_romanized": [],
        "en": [],
        "mixed": [],
    }

    total_citations = 0
    valid_citations = 0
    fabricated_citations = 0

    async with async_session_factory() as session:
        for item in EVALUATION_QUERIES:
            query = item["query"]
            cat = item["category"]
            expected = item["expected_relevant_urls"]

            processed = qp.process(query)
            results, total = await retrieval.search(
                session=session,
                processed_query=processed,
                page_size=10,
            )

            retrieved_urls = [r["url"] for r in results]
            ndcg = compute_ndcg(retrieved_urls, expected, k=10)
            category_scores[cat].append(ndcg)

            # Evaluate AI Grounding & Citations
            if results:
                ai_resp = await ai.generate_grounded_answer(
                    query=processed.normalized_query,
                    retrieved_documents=results,
                    session=session,
                    language=processed.detected_language,
                )
                for cit in ai_resp.citations:
                    total_citations += 1
                    # Check citation points to a genuine retrieved document in results
                    if 1 <= cit.citation_index <= len(results):
                        valid_citations += 1
                    else:
                        fabricated_citations += 1

            print(f"[{cat:12}] Query: {query:<38} -> nDCG@10: {ndcg:.3f}")

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY & QUALITY GATES:")
    print("=" * 70)

    targets = {
        "as_native": 0.70,
        "as_romanized": 0.60,
        "en": 0.70,
        "mixed": 0.70,
    }

    all_passed = True
    for cat, scores in category_scores.items():
        avg = sum(scores) / len(scores) if scores else 0.0
        target = targets[cat]
        status = "PASSED" if avg >= target else "UNMET"
        if avg < target:
            all_passed = False
        print(f"• {cat:14} Average nDCG@10: {avg:.3f} (Target: >={target:.2f}) -> {status}")

    cit_accuracy = (valid_citations / total_citations * 100) if total_citations > 0 else 100.0
    print(f"• AI Citation Correctness: {cit_accuracy:.1f}% (Target: >=95.0%) -> {'PASSED' if cit_accuracy >= 95.0 else 'UNMET'}")
    print(f"• Fabricated Citations: {fabricated_citations} (Target: 0) -> {'PASSED' if fabricated_citations == 0 else 'UNMET'}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_evaluation())
