# banned_detector/utils/text/fuzzy_matcher.py

from typing import Dict, List, Tuple

from rapidfuzz import fuzz

from utils.text.tokenizer import tokenize_text, normalize_text
from utils.text.keyword_matcher import EXPANDED_KEYWORDS


def similarity(a: str, b: str) -> float:
    return fuzz.ratio(a, b) / 100.0


def fuzzy_keyword_match(
    text: str,
    threshold: float = 0.75,
) -> Dict[str, List[Tuple[str, str, float]]]:
    """
    Returns:
    {
        "drugs": [("ganga", "ganja", 0.8)]
    }
    """
    tokens = tokenize_text(text)
    results: Dict[str, List[Tuple[str, str, float]]] = {}

    for category, keywords in EXPANDED_KEYWORDS.items():
        found = []

        for token in tokens:
            token_norm = normalize_text(token)
            if not token_norm:
                continue

            for keyword in keywords:
                keyword_norm = normalize_text(keyword)
                if not keyword_norm:
                    continue

                if token_norm == keyword_norm:
                    continue

                score = similarity(token_norm, keyword_norm)

                if score >= threshold:
                    found.append((token_norm, keyword_norm, round(score, 4)))

        if found:
            dedup = list({(a, b, c) for a, b, c in found})
            results[category] = sorted(dedup, key=lambda x: x[2], reverse=True)

    return results