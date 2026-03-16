# banned_detector/utils/decision/decision_engine.py

from typing import Any, Dict

HIGH_RISK_CATEGORIES = {
    "drugs",
    "weapons",
    "fraud_docs",
    "cybercrime",
    "adult",
    "gambling",
    "alcohol_tobacco_vape",
    "human_samples",
    "wildlife",
}

HIGH_RISK_FUZZY_BAN_THRESHOLD = 0.80
HIGH_RISK_FUZZY_REVIEW_THRESHOLD = 0.70


def _has_exact_hit(matched_terms: Dict[str, Any], categories: set[str]) -> bool:
    for category, values in matched_terms.items():
        if category in categories and values.get("exact"):
            return True
    return False


def _max_fuzzy_score(matched_terms: Dict[str, Any], categories: set[str]) -> float:
    best = 0.0
    for category, values in matched_terms.items():
        if category not in categories:
            continue

        for item in values.get("fuzzy", []):
            if len(item) >= 3:
                score = float(item[2])
                if score > best:
                    best = score
    return best


def decide(
    merged_text_result: Dict[str, Any],
) -> Dict[str, Any]:
    categories = set(merged_text_result.get("categories", []))
    matched_terms = merged_text_result.get("matched_terms", {})
    risky_categories = categories & HIGH_RISK_CATEGORIES

    has_exact_hit = _has_exact_hit(matched_terms, risky_categories)
    max_fuzzy = _max_fuzzy_score(matched_terms, risky_categories)

    reasons = list(merged_text_result.get("reasons", []))

    if has_exact_hit:
        decision = "banned"
        reasons.append("Direct ban: exact banned keyword matched.")
    elif max_fuzzy >= HIGH_RISK_FUZZY_BAN_THRESHOLD:
        decision = "banned"
        reasons.append(
            f"Direct ban: high-confidence fuzzy banned keyword matched ({max_fuzzy})."
        )
    elif max_fuzzy >= HIGH_RISK_FUZZY_REVIEW_THRESHOLD:
        decision = "manual_review"
        reasons.append(
            f"Manual review: medium-confidence fuzzy banned keyword matched ({max_fuzzy})."
        )
    else:
        decision = "allowed"
        if not reasons:
            reasons.append("No banned keyword matched.")

    return {
        "decision": decision,
        "final_score": round(float(merged_text_result.get("score", 0.0)), 4),
        "categories": sorted(risky_categories),
        "reasons": reasons,
        "component_scores": {
            "merged_text_score": round(float(merged_text_result.get("score", 0.0)), 4),
        },
    }