import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from websearch.prompt import generate_queries, generate_breaking_news_queries
from websearch.tavilyAPI import search_news
from LLM.ollama import generate
from LLM.prompt import get_checkpoint_prompt, format_articles_for_prompt

DEFAULT_TOPIC = "ma-funding"
DEFAULT_REGION = "india"
DEFAULT_DATE = "today"

STAGES = ["dedup", "relevance", "credibility"]


def run_pipeline(topic: str = DEFAULT_TOPIC, region: str = DEFAULT_REGION, date: str = DEFAULT_DATE) -> str:
    """Run the full newsletter generation pipeline."""
    # 1. Generate queries
    queries = generate_queries(topic, region, date, include_breaking=True, max_queries=6)
    breaking_queries = generate_breaking_news_queries(region, date, max_queries=4)
    all_queries = queries + breaking_queries

    # 2. Search for articles
    all_articles = []
    for q in all_queries:
        try:
            results = search_news(q, max_results=10, region=region)
            all_articles.extend(results)
        except Exception as e:
            print(f"Search error for '{q}': {e}")

    # 3. Deduplicate
    if not all_articles:
        return "<p>No articles found. Check Tavily API key and Ollama connection.</p>"

    # Format articles for LLM
    articles_formatted = format_articles_for_prompt(all_articles)

    # 4. Run checkpoint pipeline
    current_articles = all_articles
    for stage in STAGES:
        sys_prompt, user_prompt = get_checkpoint_prompt(stage, current_articles, date=date, region=region)
        try:
            result = generate(user_prompt, system=sys_prompt)
            parsed = json.loads(result.strip())

            if stage == "dedup":
                kept = parsed if isinstance(parsed, list) else parsed.get("kept", [])
                current_articles = [current_articles[i] for i in kept if i < len(current_articles)]
            elif stage == "relevance":
                kept = parsed.get("kept", []) if isinstance(parsed, dict) else []
                current_articles = [current_articles[i] for i in kept if i < len(current_articles)]
            elif stage == "credibility":
                scores = parsed.get("scores", {}) if isinstance(parsed, dict) else {}
                for i, a in enumerate(current_articles):
                    a["credibility"] = scores.get(str(i), scores.get(i, 50))
        except Exception as e:
            print(f"Checkpoint {stage} error: {e}")

    # 5. Generate final newsletter
    sys_prompt, user_prompt = get_checkpoint_prompt("output", current_articles, date=date, region=region)
    newsletter = generate(user_prompt, system=sys_prompt)

    return newsletter
