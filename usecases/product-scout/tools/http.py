# product_tools/http.py
import os, time, random, requests
from typing import Dict, Any, Optional

DEFAULT_UA = os.getenv("PRODUCT_TOOLS_UA", "AndreCareBot/0.1 (andre@example.com)")

def http_get_json(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 15.0,
) -> dict:
    h = {"Accept": "application/json"}
    if headers:
        h.update(headers)
    r = requests.get(url, params=params, headers=h, timeout=timeout)
    r.raise_for_status()
    return r.json()

def http_get_json_with_retries(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 20.0,
    max_attempts: int = 4,
) -> dict:
    attempt = 0
    while True:
        try:
            return http_get_json(url, params=params, headers=headers, timeout=timeout)
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status in (429, 500, 502, 503, 504) and attempt < max_attempts - 1:
                backoff = (2 ** attempt) + random.random()
                attempt += 1
                time.sleep(backoff)
                continue
            if status == 404:
                return {}
            raise
        except requests.RequestException:
            if attempt < max_attempts - 1:
                backoff = (2 ** attempt) + random.random()
                attempt += 1
                time.sleep(backoff)
                continue
            raise
