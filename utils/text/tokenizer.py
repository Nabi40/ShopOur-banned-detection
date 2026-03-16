# banned_detector/utils/text/tokenizer.py

import re
from typing import List


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[_\-\/]+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_text(text: str) -> List[str]:
    normalized = normalize_text(text)
    if not normalized:
        return []
    return normalized.split()