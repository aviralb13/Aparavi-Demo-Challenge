"""
Feature extractor for fingerprinting and heuristic signals.
Provides functions to compute perplexity (placeholder), burstiness, and simple signatures.
"""
import math


def compute_perplexity(text: str) -> float:
    # Placeholder: return a mock perplexity
    return 42.0


def compute_burstiness(text: str) -> float:
    # Placeholder: simple variance-like score of sentence lengths
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if not sentences:
        return 0.0
    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths)/len(lengths)
    var = sum((l-mean)**2 for l in lengths)/len(lengths)
    return math.sqrt(var)


def extract_features(text: str) -> dict:
    return {
        'perplexity': compute_perplexity(text),
        'burstiness': compute_burstiness(text)
    }
