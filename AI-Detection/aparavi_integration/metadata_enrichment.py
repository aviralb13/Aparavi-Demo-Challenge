"""
Utilities to build metadata payloads for Aparavi enrichment.
"""

def build_metadata_payload(ai_result: dict) -> dict:
    return {
        'ai_generated': ai_result.get('ai_generated', False),
        'confidence': ai_result.get('confidence', 0.0),
        'model_guess': ai_result.get('model_guess'),
        'risk_score': ai_result.get('risk_score', 'unknown')
    }


if __name__ == '__main__':
    example = {'ai_generated': True, 'confidence': 0.92, 'model_guess': 'gpt-4o', 'risk_score': 'high'}
    print(build_metadata_payload(example))