# banned_detector/utils/decision/rules_engine.py

from typing import Any, Dict, List


def collect_categories(*parts: Dict[str, Any]) -> List[str]:
    categories = set()

    for part in parts:
        if not isinstance(part, dict):
            continue

        for cat in part.get("categories", []):
            categories.add(cat)

        best_category = part.get("best_category")
        if best_category:
            categories.add(best_category)

    return sorted(categories)


def collect_reasons(*parts: Dict[str, Any]) -> List[str]:
    reasons = []

    for part in parts:
        if not isinstance(part, dict):
            continue

        for reason in part.get("reasons", []):
            reasons.append(reason)

        error = part.get("error")
        if error:
            reasons.append(f"Component error: {error}")

    return reasons