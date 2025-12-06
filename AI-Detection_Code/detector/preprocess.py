"""
Preprocessing utilities for cleaning and normalizing text before detection.
"""
import re


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def remove_metadata_headers(text: str) -> str:
    # Placeholder: remove common header patterns
    return re.sub(r"^\s*\[.*?\]\s*", "", text)


def preprocess(text: str) -> str:
    t = remove_metadata_headers(text)
    t = normalize_whitespace(t)
    return t
