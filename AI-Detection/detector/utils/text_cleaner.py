"""
Reusable text cleaning helpers.
"""
import re


def strip_non_printable(text: str) -> str:
    return ''.join(ch for ch in text if ch.isprintable())


def safe_truncate(text: str, max_chars: int=10000) -> str:
    return text[:max_chars]
