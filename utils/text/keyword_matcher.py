# banned_detector/utils/text/keyword_matcher.py

from typing import Dict, List

from utils.text.tokenizer import normalize_text
from utils.config.banned_keywords import CATEGORY_KEYWORDS, KEYWORD_ALIASES


def build_expanded_keywords() -> Dict[str, List[str]]:
    expanded: Dict[str, List[str]] = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        collected = set()

        for keyword in keywords:
            normalized_keyword = normalize_text(keyword)
            if normalized_keyword:
                collected.add(normalized_keyword)

            aliases = KEYWORD_ALIASES.get(normalized_keyword, [])
            for alias in aliases:
                normalized_alias = normalize_text(alias)
                if normalized_alias:
                    collected.add(normalized_alias)

        expanded[category] = sorted(collected)

    return expanded


EXPANDED_KEYWORDS = build_expanded_keywords()


def exact_keyword_match(text: str) -> Dict[str, List[str]]:
    normalized_text = normalize_text(text)
    matches: Dict[str, List[str]] = {}

    for category, keywords in EXPANDED_KEYWORDS.items():
        found = []

        for keyword in keywords:
            if keyword and keyword in normalized_text:
                found.append(keyword)

        if found:
            matches[category] = sorted(set(found))

    return matches