from checkpoints.duplicates import SYSTEM_PROMPT_DEDUP, USER_PROMPT_DEDUP
from checkpoints.relevance_fmcg_deals import SYSTEM_PROMPT_RELEVANCE, USER_PROMPT_RELEVANCE
from checkpoints.credibility import SYSTEM_PROMPT_CREDIBILITY, USER_PROMPT_CREDIBILITY
from checkpoints.output_structured import SYSTEM_PROMPT_OUTPUT, USER_PROMPT_OUTPUT


SYSTEM_PROMPT = """You are a senior industry analyst for a premium food & retail newsletter. 
Your task is to perform a comprehensive, multi-page analysis of the provided news content.

ANALYSIS FRAMEWORK (produce 3-4 pages of structured output):

## 1. EXECUTIVE SUMMARY (1 paragraph)
High-level synthesis of the most critical developments this period.

## 2. MARKET MOVEMENTS & M&A (0.5-1 page)
- Major deals, funding rounds, valuations, strategic rationale
- Buyer/seller profiles, deal multiples, geographic patterns
- Implications for competitive landscape

## 3. REGULATORY & POLICY SHIFTS (0.5-1 page)
- New regulations, draft notifications, compliance deadlines
- FSSAI/FDA/EFSA actions, labeling laws, import/export changes
- Industry impact assessment and compliance timelines

## 4. TECHNOLOGY & INNOVATION (0.5-1 page)
- New product launches, R&D breakthroughs, pilot-to-scale transitions
- AI/ML applications, precision fermentation, novel processing
- IP/patent activity, corporate-startup partnerships

## 5. SUPPLY CHAIN & COMMODITIES (0.5 page)
- Price movements (cocoa, palm oil, coffee, edible oils, proteins)
- Logistics disruptions, cold chain capacity, sourcing shifts
- Climate/geopolitical risk factors

## 6. CONSUMER & RETAIL TRENDS (0.5 page)
- Shifting demand patterns, category growth/decline
- Quick commerce expansion, omnichannel metrics, private label
- Health/sustainability claim adoption, demographic splits

## 7. INDIA-SPECIFIC DEEP DIVE (0.5-1 page, if region=India)
- FSSAI notifications, PLI scheme updates, FDI policy changes
- Quick commerce wars (Zepto/Blinkit/Swiggy/BigBasket)
- State-level policies, mandi prices, export performance
- Domestic M&A (ITC, Tata, Reliance, Adani, DMart)

## 8. RISK SIGNALS & WATCHLIST (0.5 page)
- Early warning indicators: recalls, warnings, protests, strikes
- Companies/segments under pressure
- Upcoming catalysts (earnings, regulatory decisions, harvests)

## 9. ACTIONABLE INSIGHTS FOR DECISION-MAKERS (0.5 page)
- 5-7 specific recommendations with reasoning
- Timeline sensitivity (immediate/30-day/quarter)
- Portfolio/strategy implications

STYLE GUIDELINES:
- Data-driven: cite specific numbers, dates, company names, sources
- Forward-looking: emphasize implications over event description
- Discriminating: distinguish signal from noise; flag unverified claims
- Comparable: reference historical precedents or peer benchmarks
- Professional tone: concise, analytical, no marketing language"""

USER_PROMPT_TEMPLATE = """Analyze the following news content for a food & retail industry newsletter.

TOPIC: {topic}
REGION: {region}
DATE PERIOD: {date}

SOURCE ARTICLES:
{articles}

Produce a comprehensive 3-4 page analysis following the system prompt framework. 
Structure with clear headings. Prioritize business impact and actionable intelligence.
If India region, include dedicated India deep-dive section.
"""

CHECKPOINT_PROMPTS = {
    "dedup": {
        "system": SYSTEM_PROMPT_DEDUP,
        "user": USER_PROMPT_DEDUP,
        "description": "Remove duplicate/near-duplicate articles"
    },
    "relevance": {
        "system": SYSTEM_PROMPT_RELEVANCE,
        "user": USER_PROMPT_RELEVANCE,
        "description": "Filter for FMCG deals relevance (score >= 50)"
    },
    "credibility": {
        "system": SYSTEM_PROMPT_CREDIBILITY,
        "user": USER_PROMPT_CREDIBILITY,
        "description": "Score source credibility (0-100), flag issues"
    },
    "output": {
        "system": SYSTEM_PROMPT_OUTPUT,
        "user": USER_PROMPT_OUTPUT,
        "description": "Generate structured newsletter draft"
    },
}


def format_articles_for_prompt(articles: list[dict]) -> str:
    """Format articles list for prompt injection."""
    lines = []
    for i, a in enumerate(articles):
        lines.append(f"[{i}] Title: {a.get('title', '')}")
        lines.append(f"    Source: {a.get('url', '')}")
        lines.append(f"    Content: {a.get('content', '')[:500]}...")
        lines.append("")
    return "\n".join(lines)


def get_checkpoint_prompt(stage: str, articles: list[dict], **kwargs) -> tuple[str, str]:
    """Get system and user prompt for a checkpoint stage."""
    cp = CHECKPOINT_PROMPTS[stage]
    user_prompt = cp["user"].format(
        articles=format_articles_for_prompt(articles),
        **kwargs
    )
    return cp["system"], user_prompt


def get_analysis_prompt(topic: str, region: str, date: str, articles: list[dict]) -> tuple[str, str]:
    """Get prompts for final comprehensive analysis."""
    user_prompt = USER_PROMPT_TEMPLATE.format(
        topic=topic, region=region, date=date,
        articles=format_articles_for_prompt(articles)
    )
    return SYSTEM_PROMPT, user_prompt
