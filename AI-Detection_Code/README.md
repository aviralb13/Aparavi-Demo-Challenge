# Shadow AI Detection

Minimal demo project that detects AI-generated text and enriches documents' metadata using the Aparavi data toolchain.

Goals
- Demo an AI-based detection pipeline
- Show integration with Aparavi (ingest → classify → metadata enrichment)
- Provide a small dashboard/report layer for reviewers

Quick start
1. Populate `data/sample_docs/` with sample files (AI / human / mixed).
2. Prepare `aparavi_integration/config.example.json` and rename to `config.json` with your keys.
3. Run ingestion helper:

```bash
python ingestion/load_data.py --source data/sample_docs --out staging_for_aparavi/
```

4. Run the detector locally on sample inputs:

```bash
python detector/ai_classifier.py --input data/test_inputs.json
```

5. (Optional) Launch the Streamlit demo UI:

```bash
streamlit run dashboard/streamlit_app.py
```

Repository structure
See the `shadow-ai-detection/` top-level folders for demos, ingest code, detector code, Aparavi integration glue, dashboard and docs.

License & notes
This skeleton contains placeholder implementations for demonstration. Replace keys and LLM usage with your secure implementations before running in production.