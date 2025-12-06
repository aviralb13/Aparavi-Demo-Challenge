# Aparavi Ingest Instructions

1. Create a new data source in the Aparavi UI (connect to the filesystem or cloud location).
2. Point the source to the `staging_for_aparavi/` folder created by `ingestion/load_data.py`.
3. Trigger indexing / crawling in Aparavi. Wait for extraction to complete.
4. In the Aparavi UI, open a sample document and confirm the extracted text is present.
5. Use `aparavi_integration/sdk_client.py` to connect via the SDK and trigger metadata enrichment (see that module for example code).

Notes
- Ensure API keys and endpoint are populated in `aparavi_integration/config.example.json` (copy to `config.json`).
- For demo mode, you can run enrichment locally and print payloads instead of calling the live API.