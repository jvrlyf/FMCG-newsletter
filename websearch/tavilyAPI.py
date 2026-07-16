import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Lazy initialization
_tavily_client = None
_DEFAULT_DOMAINS = [
    "reuters.com",
    "bloomberg.com",
    "foodnavigator.com",
    "just-food.com",
    "retaildive.com",
]

_INDIA_DOMAINS = _DEFAULT_DOMAINS + [
    "economictimes.indiatimes.com",
    "business-standard.com",
    "livemint.com",
    "thehindubusinessline.com",
    "moneycontrol.com",
    "fssai.gov.in",
    "pib.gov.in",
]


def _get_client():
    global _tavily_client
    if _tavily_client is None:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")
        from tavily import TavilyClient
        _tavily_client = TavilyClient(api_key=api_key)
    return _tavily_client


def search_news(
    query: str,
    max_results: int = 20,
    search_depth: str = "advanced",
    include_domains: Optional[List[str]] = None,
    region: str = "global",
) -> List[Dict[str, Any]]:
    """
    Search for news articles using Tavily API.
    """
    domains = include_domains
    if domains is None:
        domains = _INDIA_DOMAINS if region == "india" else _DEFAULT_DOMAINS

    try:
        client = _get_client()
        response = client.search(
            query=query,
            search_depth=search_depth,
            max_results=max_results,
            include_domains=domains,
            include_answer=False,
            include_raw_content=False,
            include_images=False,
        )
    except Exception as e:
        raise RuntimeError(f"Tavily API error: {e}")

    results = []
    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0.0),
            "published_date": item.get("published_date", ""),
        })

    return results


def search_breaking_news(
    query: str,
    max_results: int = 10,
    region: str = "global",
) -> List[Dict[str, Any]]:
    """Search for breaking news with tighter recency focus."""
    return search_news(
        query=query,
        max_results=max_results,
        search_depth="basic",
        region=region,
    )


if __name__ == "__main__":
    import sys
    test_query = sys.argv[1] if len(sys.argv) > 1 else "plant-based food India"
    try:
        results = search_news(test_query, max_results=5, region="india")
        for r in results:
            print(f"- {r['title']} ({r['url']})")
            print(f"  Score: {r['score']:.2f} | Date: {r['published_date']}")
            print(f"  {r['content'][:200]}...")
            print()
    except Exception as e:
        print(f"Error: {e}")
