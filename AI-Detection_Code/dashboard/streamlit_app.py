"""
Improved Streamlit demo UI.

Features:
- Choose a sample file from the repo
- Upload a file or paste text
- Run the detector and view results
- Optionally enrich metadata to Aparavi (dry-run by default)

Run with: `streamlit run dashboard/streamlit_app.py`
"""
import json
import sys
from pathlib import Path
from typing import Optional

import streamlit as st

# Ensure project root is on sys.path so local modules import correctly when
# Streamlit runs the script from a different working directory.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from detector import ai_classifier as detector
from aparavi_integration.sdk_client import AparaviClient
from aparavi_integration.metadata_enrichment import build_metadata_payload


st.set_page_config(page_title='Shadow AI Detection', layout='wide')

st.title('AI Detection — Interactive Demo')

SAMPLES_ROOT = ROOT
SAMPLES = list((SAMPLES_ROOT / 'data' / 'sample_docs').rglob('*.txt'))

with st.sidebar:
    st.header('Input')
    sample_choice = st.selectbox('Choose a sample file', options=[str(p) for p in SAMPLES] if SAMPLES else ['(no samples)'])
    uploaded = st.file_uploader('Or upload a text file', type=['txt'], accept_multiple_files=False)
    pasted = st.text_area('Or paste text here', height=120)
    st.markdown('---')
    st.header('Aparavi')
    enrich = st.checkbox('Enrich metadata to Aparavi', value=False)
    dry_run = st.checkbox('Dry run (do not call API)', value=True)

st.header('Run detector')


def _read_text_from_source(sample: Optional[str], uploaded_file, pasted_text: str) -> Optional[str]:
    if uploaded_file is not None:
        try:
            return uploaded_file.getvalue().decode('utf-8')
        except Exception:
            return None
    if pasted_text and pasted_text.strip():
        return pasted_text
    if sample and Path(sample).exists():
        return Path(sample).read_text(encoding='utf-8')
    return None


text = _read_text_from_source(sample_choice, uploaded, pasted)

if not text:
    st.info('Select a sample, upload a file, or paste text to begin.')

if st.button('Run Detector'):
    if not text:
        st.error('No text available to analyze')
    else:
        with st.spinner('Running detector...'):
            result = detector.classify_text(text)

        st.subheader('Detection Result')
        st.json(result)

        st.metric('AI Generated', str(result.get('ai_generated')))
        st.metric('Confidence', result.get('confidence'))
        st.metric('Risk', result.get('risk_score'))

        st.subheader('Features')
        st.write(result.get('features', {}))

        st.subheader('Heuristics')
        st.write(result.get('rules', {}))

        payload = build_metadata_payload(result)
        st.subheader('Metadata Payload')
        st.json(payload)

        st.download_button('Download metadata JSON', data=json.dumps(payload, indent=2), file_name='metadata_payload.json')

        if enrich:
            st.write('Enrichment settings: dry_run=' + str(dry_run))
            if dry_run:
                st.info('Dry run enabled — not calling Aparavi API. Toggle to disable dry run.')
            else:
                try:
                    cfg_path = ROOT / 'aparavi_integration' / 'config.example.json'
                    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
                    client = AparaviClient(cfg)
                    # For demo we try to lookup document by path if sample was used
                    doc_id = None
                    if sample_choice:
                        doc = client.find_document_by_path(sample_choice)
                        doc_id = doc.get('id') if doc else None
                    if not doc_id:
                        st.warning('No document id found for this input — supply document id mapping if you want to enrich')
                    else:
                        resp = client.enrich_metadata(doc_id, payload)
                        st.success('Enrichment response')
                        st.write(resp)
                except Exception as e:
                    st.error(f'Enrichment failed: {e}')

st.sidebar.markdown('---')
st.sidebar.write('Samples found: ' + str(len(SAMPLES)))
