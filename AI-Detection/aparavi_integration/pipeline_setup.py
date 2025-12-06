
import argparse
import json
from pathlib import Path

from aparavi_integration import sdk_client as _sdk
from aparavi_integration import metadata_enrichment as _meta
from detector import ai_classifier as _det


def load_inputs(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f'Input file not found: {path}')
    return json.loads(p.read_text())


def load_config(path: str):
    p = Path(path)
    if not p.exists():
        # fallback to example config
        return {}
    return json.loads(p.read_text())


def run_pipeline(inputs_json: str, config_path: str):
    inputs = load_inputs(inputs_json)
    cfg = load_config(config_path)
    client = _sdk.AparaviClient(cfg)

    results = {}
    for rel in inputs.get('samples', []):
        p = Path(rel)
        if not p.exists():
            results[str(p)] = {'error': 'file not found'}
            continue

        ai_result = _det.run_on_file(str(p))
        payload = _meta.build_metadata_payload(ai_result)

        # Attempt to find document id in Aparavi and enrich metadata (demo)
        doc = client.find_document_by_path(str(p))
        doc_id = doc.get('id') if doc else None
        if doc_id:
            client.enrich_metadata(doc_id, payload)
        else:
            # fallback: print payload
            print(f"No document id found for {p}; payload:\n{json.dumps(payload, indent=2)}")

        results[str(p)] = {'ai_result': ai_result, 'metadata_payload': payload}

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', default='data/test_inputs.json', help='Path to JSON inputs')
    parser.add_argument('--config', default='aparavi_integration/config.example.json', help='Config path')
    args = parser.parse_args()

    out = run_pipeline(args.inputs, args.config)
    print(json.dumps(out, indent=2))
"""
Defines a simple pipeline orchestration: ingest -> extract (Aparavi) -> classify -> enrich
"""
from aparavi_integration.sdk_client import AparaviClient
from detector.ai_classifier import classify_text


def run_pipeline_for_path(config: dict, path: str):
    client = AparaviClient(config.get('aparavi', {}))
    # find document in Aparavi
    doc = client.find_document_by_path(path)
    # For demo, read file locally
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # classify
    result = classify_text(text)
    # enrich
    client.enrich_metadata(doc['id'], result)
    return result
