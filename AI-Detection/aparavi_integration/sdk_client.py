"""
Aparavi API client wrapper (requests-based).

This client provides minimal functionality used by the demo pipeline:
- `find_document_by_path(path)` — attempts to locate a document record
- `enrich_metadata(document_id, metadata)` — posts metadata for a document

Configuration sources (in order of precedence):
1. `config` dict passed to the constructor (look for `aparavi.api_key` / `aparavi.endpoint`)
2. Environment variables: `APARAVI_API_KEY`, `APARAVI_ENDPOINT`

Notes:
- This is a small wrapper intended for demo/testing. Update endpoints/paths
  to match your actual Aparavi API.
"""
from __future__ import annotations

import os
import logging
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOG = logging.getLogger(__name__)


def _build_session(retries: int = 3, backoff_factor: float = 0.3) -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


class AparaviClient:
    def __init__(self, config: Optional[Dict[str, Any]] = None, session: Optional[requests.Session] = None):
        cfg = config or {}
        aparavi_cfg = cfg.get('aparavi', {}) if isinstance(cfg, dict) else {}

        self.api_key = "xeTRYOIhTZZMr9lyQ2wxHJba3oIVq8vS3h_kHuYCJIW5QZbZ4D6vaAdUUqgTzLhH"
        self.endpoint = (
            aparavi_cfg.get('endpoint')
            or os.environ.get('APARAVI_ENDPOINT')
            or 'https://eaas-dev.aparavi.com'
        )

        if not self.api_key:
            LOG.warning('No Aparavi API key provided; network calls will fail until configured.')

        self.session = session or _build_session()

    def _headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError('Missing Aparavi API key. Set APARAVI_API_KEY or provide in config.')
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

    def enrich_metadata(self, document_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Post metadata for a document. Returns API response as dict.

        Endpoint path used here is `/documents/{id}/metadata` — update if your
        Aparavi API uses a different route.
        """
        if not document_id:
            raise ValueError('document_id is required')

        url = f"{self.endpoint.rstrip('/')}/documents/{document_id}/metadata"
        LOG.debug('Posting metadata to %s', url)
        resp = self.session.post(url, headers=self._headers(), json=metadata, timeout=15)
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            LOG.error('Failed to enrich metadata: %s %s', resp.status_code, resp.text)
            raise
        # Return parsed JSON or raw text fallback
        try:
            return resp.json()
        except ValueError:
            return {'status_text': resp.text}

    def find_document_by_path(self, path: str) -> Optional[Dict[str, Any]]:
        """Try to find a document record by path. Returns the first match or None.

        This function assumes an API endpoint `/documents/search` that accepts
        a `path` query parameter and returns a JSON with an `items` list.
        Adjust to your actual API.
        """
        url = f"{self.endpoint.rstrip('/')}/documents/search"
        params = {'path': path}
        LOG.debug('Searching for document by path: %s', path)
        resp = self.session.get(url, headers=self._headers(), params=params, timeout=10)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            LOG.warning('Search by path failed: %s %s', resp.status_code, resp.text)
            return None

        try:
            data = resp.json()
        except ValueError:
            LOG.warning('Search response not JSON: %s', resp.text)
            return None

        items = data.get('items') if isinstance(data, dict) else None
        if items and len(items) > 0:
            return items[0]
        return None

