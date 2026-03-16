# banned_detector/utils/text/text_detector.py

from typing import Any, Dict

from utils.text.keyword_matcher import exact_keyword_match
from utils.text.fuzzy_matcher import fuzzy_keyword_match
from utils.config.thresholds import (
    TEXT_EXACT_MATCH_SCORE,
    TEXT_FUZZY_MATCH_SCORE,
)


def analyze_text(title: str = "", description: str = "") -> Dict[str, Any]:
    combined_text = f"{title} {description}".strip()

    exact_matches = exact_keyword_match(combined_text)
    fuzzy_matches = fuzzy_keyword_match(combined_text)

    categories = set(exact_matches.keys()) | set(fuzzy_matches.keys())

    max_score = 0.0
    matched_terms = {}
    reasons = []

    for category in categories:
        matched_terms[category] = {
            "exact": exact_matches.get(category, []),
            "fuzzy": fuzzy_matches.get(category, []),
        }

        if exact_matches.get(category):
            max_score = max(max_score, TEXT_EXACT_MATCH_SCORE)
            reasons.append(f"Exact text match in category '{category}'")

        if fuzzy_matches.get(category):
            max_score = max(max_score, TEXT_FUZZY_MATCH_SCORE)
            reasons.append(f"Fuzzy text match in category '{category}'")

    return {
        "score": round(max_score, 4),
        "categories": sorted(categories),
        "matched_terms": matched_terms,
        "reasons": reasons,
        "raw_text": combined_text,
    }