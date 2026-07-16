from typing import List, Optional, Literal
from datetime import datetime, timedelta


Region = Literal["global", "india", "us", "eu", "apac"]
DateSpec = Literal["today", "this-week"] | str


TOPIC_KEYWORDS = {
    "ma-funding": [
        "FMCG M&A deal",
        "retail acquisition",
        "food company funding",
        "consumer brand investment",
        "private equity food retail",
        "strategic acquisition FMCG",
        "joint venture food retail",
        "IPO food company",
        "merger consumer goods",
        "venture capital food retail",
        "buyout food brand",
        "deal value FMCG",
        "funding round food tech",
        "retail consolidation",
        "cross-border deal FMCG",
    ],
    "plant-based": [
        "plant-based",
        "plant based",
        "alternative protein",
        "meat alternative",
        "dairy alternative",
        "vegan",
        "vegetarian",
        "pea protein",
        "mycoprotein",
        "cultivated meat",
        "cultured meat",
        "cell-cultured",
        "fermentation-derived",
        "precision fermentation",
        "algae protein",
        "insect protein",
    ],
    "food-tech": [
        "food technology",
        "food tech",
        "precision fermentation",
        "AI food",
        "artificial intelligence food",
        "3D food printing",
        "high pressure processing",
        "HPP",
        "personalized nutrition",
        "food safety technology",
        "blockchain traceability",
        "rapid pathogen testing",
        "novel food processing",
    ],
    "retail-tech": [
        "retail technology",
        "retail tech",
        "e-grocery",
        "online grocery",
        "quick commerce",
        "instant delivery",
        "dark store",
        "micro-fulfillment",
        "electronic shelf label",
        "smart cart",
        "checkout-free",
        "autonomous checkout",
        "retail media network",
        "loyalty program",
        "personalization engine",
        "demand forecasting",
    ],
    "regulations": [
        "food regulation",
        "food safety regulation",
        "labeling regulation",
        "novel food regulation",
        "front-of-pack labeling",
        "Nutri-Score",
        "Health Star Rating",
        "ultra-processed food",
        "UPF regulation",
        "plastic packaging ban",
        "single-use plastic",
        "food additive",
        "GRAS",
        "Codex Alimentarius",
    ],
    "supply-chain": [
        "food supply chain",
        "cold chain",
        "commodity price",
        "palm oil price",
        "cocoa price",
        "coffee price",
        "wheat price",
        "edible oil price",
        "upcycled ingredient",
        "alternative fat",
        "alternative oil",
        "regional sourcing",
        "local sourcing",
        "food waste valorization",
        "harvest report",
        "logistics bottleneck",
    ],
    "consumer-trends": [
        "consumer trend",
        "food trend",
        "health and wellness",
        "gut health",
        "protein fortification",
        "low sugar",
        "sugar reduction",
        "sustainability claim",
        "carbon footprint",
        "regenerative agriculture",
        "snackification",
        "meal occasion",
        "premiumization",
        "value-seeking",
        "Gen Z food",
        "clean label",
        "ingredient transparency",
    ],
    "sustainability": [
        "sustainability",
        "ESG",
        "Scope 3 emissions",
        "regenerative agriculture",
        "water stewardship",
        "packaging circularity",
        "recyclable packaging",
        "compostable packaging",
        "reuse packaging",
        "deforestation-free",
        "science-based target",
        "SBTi",
        "net zero",
        "carbon neutral",
    ],
}

SUBTOPIC_KEYWORDS = {
    "ma-funding": {
        "india": ["FMCG India acquisition", "Indian retail funding", "food startup India investment", "D2C brand funding India", "quick commerce funding India"],
        "global": ["global FMCG M&A", "cross-border food deal", "international retail acquisition", "global consumer brand buyout"],
        "pe-vc": ["private equity food retail", "venture capital consumer brand", "growth equity FMCG", "buyout fund food"],
        "ipo": ["food company IPO", "retail IPO", "FMCG public listing", "consumer brand IPO"],
    },
    "plant-based": {
        "meat": ["plant-based meat", "meat alternative", "vegan meat", "cultivated meat", "cultured meat"],
        "dairy": ["plant-based dairy", "dairy alternative", "vegan cheese", "oat milk", "almond milk", "soy milk"],
        "seafood": ["plant-based seafood", "alternative seafood", "vegan fish", "cultivated seafood"],
        "fermentation": ["precision fermentation", "fermentation-derived protein", "mycoprotein", "Quorn"],
        "ingredients": ["pea protein", "soy protein", "wheat protein", "fava protein", "algae protein", "insect protein"],
    },
    "regulations": {
        "india": ["FSSAI", "Food Safety and Standards Authority", "FSSAI notification", "FSSAI labeling", "PLI scheme food", "FDI food retail", "GST food"],
        "global": ["FDA", "EFSA", "Codex", "Novel Food", "GRAS"],
        "labeling": ["front-of-pack", "Nutri-Score", "warning label", "traffic light label", "Health Star Rating"],
        "packaging": ["plastic ban", "single-use plastic", "EPR", "extended producer responsibility"],
    },
    "retail-tech": {
        "quick-commerce": ["quick commerce", "instant delivery", "10-minute delivery", "Zepto", "Blinkit", "BigBasket", "Swiggy Instamart", "Dunzo"],
        "omnichannel": ["omnichannel", "click and collect", "BOPIS", "endless aisle"],
        "retail-media": ["retail media", "retail media network", "advertising platform"],
    },
    "supply-chain": {
        "commodities": ["palm oil", "cocoa", "coffee", "wheat", "rice", "edible oil", "sugar", "dairy commodity"],
        "cold-chain": ["cold chain", "cold storage", "refrigerated transport", "perishable logistics"],
        "upcycling": ["upcycled", "food waste", "by-product valorization", "circular ingredient"],
    },
}

REGION_KEYWORDS = {
    "global": [],
    "india": [
        "India",
        "Indian",
        "FSSAI",
        "FMCG India",
        "quick commerce India",
        "PLI scheme",
        "food processing India",
        "agri-export",
        "mandi price",
        "APMC",
        "FCI",
        "NABARD",
        "ICAR",
        "CFTRI",
        "DFRL",
    ],
    "us": [
        "United States",
        "US",
        "FDA",
        "USDA",
        "FTC",
        "GRAS",
        "FSMA",
    ],
    "eu": [
        "European Union",
        "EU",
        "EFSA",
        "European Commission",
        "Novel Food Regulation",
        "Farm to Fork",
        "Green Deal",
    ],
    "apac": [
        "Asia Pacific",
        "APAC",
        "China",
        "Japan",
        "Australia",
        "New Zealand",
        "Singapore",
        "South Korea",
        "Southeast Asia",
        "ASEAN",
    ],
}

BREAKING_NEWS_KEYWORDS = {
    "major-ma-funding": [
        "acquires",
        "acquisition",
        "merger",
        "funding round",
        "Series A",
        "Series B",
        "Series C",
        "unicorn",
        "billion dollar",
        "strategic investment",
        "buyout",
        "takeover",
        "divestiture",
        "stake sale",
    ],
    "regulatory-action": [
        "warning letter",
        "product recall",
        "import alert",
        "gazette notification",
        "compliance deadline",
        "enforcement action",
        "show cause notice",
    ],
    "food-safety": [
        "outbreak",
        "Salmonella",
        "E. coli",
        "Listeria",
        "allergen",
        "mislabeling",
        "contamination",
        "foreign object",
        "food poisoning",
    ],
    "supply-disruption": [
        "port strike",
        "strike",
        "drought",
        "flood",
        "extreme weather",
        "trade restriction",
        "export ban",
        "import ban",
        "logistics disruption",
        "shipping crisis",
    ],
    "commodity-shock": [
        "price surge",
        "price spike",
        "record high",
        "all-time high",
        "commodity rally",
    ],
    "retail-strategy": [
        "store closure",
        "store opening",
        "format change",
        "market entry",
        "market exit",
        "private label",
        "loyalty program",
    ],
    "policy-announcement": [
        "Union Budget",
        "Budget announcement",
        "policy change",
        "scheme launch",
        "incentive scheme",
        "GST rate",
        "FDI policy",
    ],
    "sustainability-scandal": [
        "greenwashing",
        "lawsuit",
        "deforestation",
        "labor violation",
        "human rights",
        "forced labor",
        "child labor",
    ],
}


def _date_context(date_spec: DateSpec) -> str:
    today = datetime.now().date()
    if date_spec == "today":
        return today.strftime("%B %d, %Y")
    elif date_spec == "this-week":
        week_start = today - timedelta(days=today.weekday())
        return f"week of {week_start.strftime('%B %d, %Y')}"
    else:
        return date_spec


def generate_queries(
    topic: str,
    region: Region = "global",
    date: DateSpec = "today",
    include_breaking: bool = False,
    subtopics: Optional[List[str]] = None,
    max_queries: int = 8,
) -> List[str]:
    """
    Generate search queries for a given topic, region, and date.
    
    Args:
        topic: Main topic key from TOPIC_KEYWORDS (e.g., "plant-based", "food-tech")
        region: Target region ("global", "india", "us", "eu", "apac")
        date: "today", "this-week", or specific date string
        include_breaking: Whether to include breaking news style queries
        subtopics: Optional list of subtopic keys to focus on
        max_queries: Maximum number of queries to generate
    
    Returns:
        List of query strings optimized for Tavily search
    """
    if topic not in TOPIC_KEYWORDS:
        raise ValueError(f"Unknown topic: {topic}. Available: {list(TOPIC_KEYWORDS.keys())}")
    
    topic_kws = TOPIC_KEYWORDS[topic]
    region_kws = REGION_KEYWORDS.get(region, [])
    date_ctx = _date_context(date)
    
    queries = []
    
    # Primary topic + region + date query
    primary_kws = topic_kws[:3]
    query_parts = primary_kws + region_kws[:3] + [date_ctx]
    queries.append(" ".join(query_parts))
    
    # Subtopic-focused queries
    if subtopics:
        for sub in subtopics:
            if topic in SUBTOPIC_KEYWORDS and sub in SUBTOPIC_KEYWORDS[topic]:
                sub_kws = SUBTOPIC_KEYWORDS[topic][sub][:3]
                q = " ".join(sub_kws + region_kws[:2] + [date_ctx])
                queries.append(q)
    elif topic in SUBTOPIC_KEYWORDS:
        for sub_name, sub_kws in list(SUBTOPIC_KEYWORDS[topic].items())[:3]:
            q = " ".join(sub_kws[:2] + region_kws[:2] + [date_ctx])
            queries.append(q)
    
    # Topic variations
    for i in range(3, min(len(topic_kws), 6), 2):
        q = " ".join(topic_kws[i:i+2] + region_kws[:2] + [date_ctx])
        queries.append(q)
    
    # Broader industry query
    broader_terms = {
        "ma-funding": "FMCG retail deal investment news",
        "plant-based": "alternative protein industry",
        "food-tech": "food technology innovation",
        "retail-tech": "grocery retail technology",
        "regulations": "food regulation update",
        "supply-chain": "food supply chain",
        "consumer-trends": "food consumer trend",
        "sustainability": "food sustainability ESG",
    }
    if topic in broader_terms:
        queries.append(f"{broader_terms[topic]} {region_kws[0] if region_kws else ''} {date_ctx}")
    
    # Breaking news style queries
    if include_breaking:
        breaking_kws = []
        for cat_kws in BREAKING_NEWS_KEYWORDS.values():
            breaking_kws.extend(cat_kws[:1])
        q = " ".join(topic_kws[:2] + breaking_kws[:3] + region_kws[:2] + [date_ctx])
        queries.append(q)
    
    # Deduplicate and limit
    seen = set()
    unique_queries = []
    for q in queries:
        q = q.strip()
        if q and q not in seen:
            seen.add(q)
            unique_queries.append(q)
    
    return unique_queries[:max_queries]


def generate_breaking_news_queries(
    region: Region = "global",
    date: DateSpec = "today",
    categories: Optional[List[str]] = None,
    max_queries: int = 10,
) -> List[str]:
    """
    Generate queries specifically for breaking news monitoring.
    
    Args:
        region: Target region
        date: Date spec
        categories: Specific alert categories to include (default: all)
        max_queries: Maximum queries to return
    
    Returns:
        List of breaking news query strings
    """
    region_kws = REGION_KEYWORDS.get(region, [])
    date_ctx = _date_context(date)
    
    cats = categories or list(BREAKING_NEWS_KEYWORDS.keys())
    queries = []
    
    for cat in cats:
        if cat not in BREAKING_NEWS_KEYWORDS:
            continue
        kws = BREAKING_NEWS_KEYWORDS[cat][:3]
        q = " ".join(kws + region_kws[:2] + [date_ctx])
        queries.append(q)
    
    # Cross-category combo queries
    if len(cats) > 1:
        combo_kws = []
        for cat in cats[:3]:
            combo_kws.extend(BREAKING_NEWS_KEYWORDS[cat][:1])
        queries.append(" ".join(combo_kws + region_kws[:2] + [date_ctx]))
    
    # Deduplicate
    seen = set()
    unique = []
    for q in queries:
        q = q.strip()
        if q and q not in seen:
            seen.add(q)
            unique.append(q)
    
    return unique[:max_queries]


def get_available_topics() -> List[str]:
    return list(TOPIC_KEYWORDS.keys())


def get_available_regions() -> List[Region]:
    return ["global", "india", "us", "eu", "apac"]


def get_subtopics(topic: str) -> List[str]:
    return list(SUBTOPIC_KEYWORDS.get(topic, {}).keys())


if __name__ == "__main__":
    print("=== Topic List ===")
    for t in get_available_topics():
        print(f"  {t}: {len(TOPIC_KEYWORDS[t])} keywords")
        if t in SUBTOPIC_KEYWORDS:
            print(f"    Subtopics: {list(SUBTOPIC_KEYWORDS[t].keys())}")
    
    print("\n=== Region Keywords ===")
    for r, kws in REGION_KEYWORDS.items():
        print(f"  {r}: {kws[:5]}...")
    
    print("\n=== Sample Queries ===")
    test_cases = [
        ("ma-funding", "india", "today"),
        ("ma-funding", "global", "this-week"),
        ("plant-based", "india", "today", True, ["india"]),
        ("retail-tech", "india", "today", False, ["quick-commerce"]),
        ("supply-chain", "global", "today"),
    ]
    
    for tc in test_cases:
        topic = tc[0]
        region = tc[1]
        date = tc[2]
        include_breaking = tc[3] if len(tc) > 3 else False
        subtopics = tc[4] if len(tc) > 4 else None
        
        qs = generate_queries(topic, region, date, include_breaking, subtopics, max_queries=5)
        print(f"\n  Topic: {topic} | Region: {region} | Date: {date} | Breaking: {include_breaking}")
        for i, q in enumerate(qs, 1):
            print(f"    {i}. {q}")
    
    print("\n=== Breaking News Queries (India) ===")
    bnq = generate_breaking_news_queries("india", "today", max_queries=8)
    for i, q in enumerate(bnq, 1):
        print(f"  {i}. {q}")