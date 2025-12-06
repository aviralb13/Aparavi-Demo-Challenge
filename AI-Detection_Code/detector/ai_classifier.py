"""AI classifier wrapper — small demo detector.

This implementation combines simple fingerprint features and rule-based
heuristics to produce a demo `ai_generated` decision and confidence score.
Replace with a model-backed classifier in production.
"""
import argparse
import json
import os
from typing import Dict

from detector import preprocess as _pre
from detector import fingerprint_model as _fp
from detector import heuristics as _hr


def classify_text(text: str) -> Dict:
    t = _pre.preprocess(text)
    features = _fp.extract_features(t)
    rules = _hr.rule_based_score(t)

    # Simple scoring heuristic for demo purposes
    score = 0.0
    # Lower perplexity (placeholder) means more AI-like in this demo
    perplexity = features.get('perplexity', 100.0)
    score += max(0.0, (200.0 - perplexity) / 200.0) * 0.6
    # Burstiness: higher burstiness increases AI suspicion slightly
    burst = features.get('burstiness', 0.0)
    score += min(1.0, burst / 10.0) * 0.2
    # Rule-based strong signals
    if rules.get('signature_present'):
        score += 0.5
    if rules.get('over_perfect_grammar'):
        score += 0.2

    # Normalize confidence to [0,1]
    confidence = max(0.0, min(1.0, score))

    # Configurable threshold (env var DETECTOR_AI_THRESHOLD). Default: 0.6
    try:
        threshold = float(os.environ.get('DETECTOR_AI_THRESHOLD', '0.6'))
    except Exception:
        threshold = 0.6

    ai_generated = confidence > threshold

    # Simple model guess placeholder (uses same threshold)
    model_guess = 'gpt-like' if confidence > threshold else None

    # Risk score mapping
    if confidence > 0.8:
        risk = 'high'
    elif confidence > threshold:
        risk = 'medium'
    else:
        risk = 'low'

    return {
        'ai_generated': bool(ai_generated),
        'confidence': round(float(confidence), 3),
        'model_guess': model_guess,
        'risk_score': risk,
        'features': features,
        'rules': rules
    }


def run_on_file(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return classify_text(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to a single file or JSON list')
    args = parser.parse_args()

    if args.input.endswith('.json'):
        with open(args.input, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        results = {}
        for p in data.get('samples', []):
            try:
                results[p] = run_on_file(p)
            except Exception as e:
                results[p] = {'error': str(e)}
        print(json.dumps(results, indent=2))
    else:
        print(json.dumps(run_on_file(args.input), indent=2))
