#!/usr/bin/env python3
"""
SearX Search Module

Public SearXNG fallback search (clearnet, NOT anonymous).
Use when DorXNG is unavailable or explicitly not desired.
"""

import gzip
import json
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

SEARX_SPACE_INSTANCES_JSON = "https://searx.space/data/instances.json"

# Static fallback list if searx.space is unavailable
DEFAULT_INSTANCES = [
    "https://searx.tiekoetter.com",
    "https://search.rhscz.eu",
    "https://search.sapti.me",
    "https://search.inetol.net",
    "https://searxng.shreven.org",
]

# Per-instance pacing (be polite to public instances)
_MIN_DELAY_SECONDS = 3.0
_last_query_time: Dict[str, float] = {}


@dataclass
class SearXError(Exception):
    instance: str
    error_type: str
    detail: str
    retriable: bool = False

    def __str__(self) -> str:
        return f"[{self.error_type}] {self.instance}: {self.detail}"


class _HTMLResultParser(HTMLParser):
    """Lightweight fallback parser for HTML search results."""

    def __init__(self, instance_base: str):
        super().__init__()
        self.instance_base = instance_base.rstrip("/")
        self._in_link = False
        self._current_href = ""
        self._current_text = []
        self.results: List[Dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "a":
            return
        attrs_dict = {k: (v or "") for k, v in attrs}
        href = attrs_dict.get("href", "")
        if href.startswith("http://") or href.startswith("https://"):
            # Filter internal SearX links
            if href.startswith(self.instance_base):
                return
            self._in_link = True
            self._current_href = href
            self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._in_link:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._in_link:
            title = " ".join(x.strip() for x in self._current_text if x.strip())
            if title and self._current_href:
                self.results.append(
                    {
                        "title": title[:200],
                        "url": self._current_href,
                        "content": "",
                        "engine": "searx-html-fallback",
                    }
                )
            self._in_link = False
            self._current_href = ""
            self._current_text = []


def _normalize_instance(instance_url: str) -> str:
    return instance_url.rstrip("/")


def _instance_delay(instance: str) -> None:
    now = time.time()
    last = _last_query_time.get(instance, 0)
    if now - last < _MIN_DELAY_SECONDS:
        time.sleep(_MIN_DELAY_SECONDS - (now - last))


def _decode_response(body: bytes, content_encoding: str) -> bytes:
    encoding = (content_encoding or "").lower()
    if "gzip" in encoding:
        return gzip.decompress(body)
    return body


def _classify_error(instance: str, err: Exception) -> SearXError:
    if isinstance(err, urllib.error.HTTPError):
        if err.code == 429:
            return SearXError(instance, "rate_limit", "HTTP 429 Too Many Requests", retriable=True)
        if err.code == 403:
            return SearXError(instance, "forbidden", "HTTP 403 Forbidden", retriable=False)
        if err.code in (500, 502, 503, 504):
            return SearXError(instance, "server_error", f"HTTP {err.code}", retriable=True)
        return SearXError(instance, "http_error", f"HTTP {err.code}", retriable=False)

    if isinstance(err, urllib.error.URLError):
        reason = getattr(err, "reason", None)
        if isinstance(reason, socket.gaierror):
            return SearXError(instance, "dns", str(reason), retriable=False)
        return SearXError(instance, "network", str(reason or err), retriable=True)

    if isinstance(err, TimeoutError):
        return SearXError(instance, "timeout", str(err), retriable=True)

    if isinstance(err, json.JSONDecodeError):
        return SearXError(instance, "json_decode", str(err), retriable=True)

    return SearXError(instance, "unknown", str(err), retriable=False)


def fetch_instances_from_searx_space(
    timeout: int = 20,
    min_initial_success: int = 80,
    min_search_success: int = 50,
) -> List[str]:
    """
    Fetch candidate public instances from searx.space.

    Filters for:
    - normal network type
    - HTTP status 200
    - initial response success >= threshold
    - search success >= threshold (where available)
    - main instance URLs
    - no analytics flag where provided

    Returns instances ranked by health score (best first).
    """
    req = urllib.request.Request(
        SEARX_SPACE_INSTANCES_JSON,
        headers={"User-Agent": "The-Dork/1.0"},
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8", errors="replace"))

    scored: List[Tuple[float, str]] = []
    instances = payload.get("instances", {})
    for instance_url, meta in instances.items():
        if meta.get("network_type") != "normal":
            continue
        if meta.get("http", {}).get("status_code") != 200:
            continue
        if meta.get("analytics") is True:
            continue
        if not meta.get("main", True):
            continue

        initial_success = float(meta.get("timing", {}).get("initial", {}).get("success_percentage", 0) or 0)
        if initial_success < min_initial_success:
            continue

        search_success_raw = meta.get("timing", {}).get("search", {}).get("success_percentage", 0)
        try:
            search_success = float(search_success_raw or 0)
        except Exception:
            search_success = 0.0

        if search_success < min_search_success:
            continue

        # Weighted score favors actual search success over initial ping health
        score = (search_success * 2.0) + initial_success
        scored.append((score, _normalize_instance(instance_url)))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [url for _, url in scored]


def get_candidate_instances(limit: int = 10) -> List[str]:
    """Get candidate instances from searx.space, fallback to static list."""
    candidates: List[str] = []

    try:
        dynamic = fetch_instances_from_searx_space()
        candidates.extend(dynamic)
    except Exception:
        pass

    # Ensure static fallbacks are always present at tail
    candidates.extend(DEFAULT_INSTANCES)

    # De-dup while preserving order
    seen = set()
    unique = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    return unique[:limit]


def check_instance(instance_url: str, timeout: int = 10) -> bool:
    """Check if an instance supports JSON search responses."""
    instance = _normalize_instance(instance_url)
    query = urllib.parse.quote("test", safe="")
    url = f"{instance}/search?q={query}&format=json"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "The-Dork/1.0",
            "Accept": "application/json,text/plain,*/*",
            "Accept-Encoding": "gzip",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = _decode_response(response.read(), response.headers.get("Content-Encoding", ""))
            data = json.loads(body.decode("utf-8", errors="replace"))
            return isinstance(data, dict) and "results" in data
    except Exception:
        return False


def _search_json(instance: str, query: str, timeout: int) -> List[Dict[str, Any]]:
    encoded = urllib.parse.quote(query, safe="")
    url = f"{instance}/search?q={encoded}&format=json"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json,text/plain,*/*",
            "Accept-Encoding": "gzip",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        _last_query_time[instance] = time.time()
        body = _decode_response(response.read(), response.headers.get("Content-Encoding", ""))
        data = json.loads(body.decode("utf-8", errors="replace"))
        return data.get("results", [])


def _query_terms(query: str) -> List[str]:
    terms = re.findall(r"[a-zA-Z0-9]+", query.lower())
    return [t for t in terms if len(t) >= 4]


def _looks_relevant(result: Dict[str, Any], query: str) -> bool:
    terms = _query_terms(query)
    if not terms:
        return True
    hay = f"{result.get('title','')} {result.get('url','')} {result.get('content','')}".lower()
    return any(t in hay for t in terms)


def _search_html_fallback(instance: str, query: str, timeout: int) -> List[Dict[str, Any]]:
    encoded = urllib.parse.quote(query, safe="")
    url = f"{instance}/search?q={encoded}&categories=general"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        _last_query_time[instance] = time.time()
        body = _decode_response(response.read(), response.headers.get("Content-Encoding", ""))
        html = body.decode("utf-8", errors="replace")

    parser = _HTMLResultParser(instance)
    parser.feed(html)

    # de-dup and relevance filter to avoid anti-bot/challenge noise
    seen = set()
    filtered = []
    for r in parser.results:
        u = r.get("url", "")
        if not u or u in seen:
            continue
        seen.add(u)
        if _looks_relevant(r, query):
            filtered.append(r)

    return filtered


def search_searx(
    query: str,
    instance: Optional[str] = None,
    timeout: int = 30,
    rotate: bool = True,
    max_retries: int = 1,
    backoff_seconds: int = 4,
) -> List[Dict[str, Any]]:
    """
    Search via SearX with rotation, backoff, and fallback parsing.

    NOTE: Public SearX is clearnet and NOT anonymous.
    """
    if instance:
        candidates = [_normalize_instance(instance)]
    else:
        candidates = get_candidate_instances(limit=12)

    errors: List[SearXError] = []

    for idx, inst in enumerate(candidates):
        if idx > 0 and not rotate and instance is None:
            break

        for attempt in range(max_retries + 1):
            try:
                _instance_delay(inst)
                results = _search_json(inst, query, timeout=timeout)
                if results:
                    return results
                # JSON succeeded but empty; try html fallback once
                _instance_delay(inst)
                html_results = _search_html_fallback(inst, query, timeout=min(timeout, 20))
                if html_results:
                    return html_results
                break
            except Exception as raw_err:
                serr = _classify_error(inst, raw_err)
                errors.append(serr)

                if serr.error_type == "rate_limit" and attempt < max_retries:
                    # exponential backoff per instance
                    sleep_for = backoff_seconds * (2 ** attempt)
                    time.sleep(sleep_for)
                    continue

                # For JSON decoding, try HTML fallback immediately
                if serr.error_type == "json_decode":
                    try:
                        _instance_delay(inst)
                        html_results = _search_html_fallback(inst, query, timeout=min(timeout, 20))
                        if html_results:
                            return html_results
                    except Exception as raw_html_err:
                        errors.append(_classify_error(inst, raw_html_err))

                break

        # polite pause before next instance
        time.sleep(1.0)

    # concise diagnostics
    if errors:
        summary = {}
        for e in errors:
            summary[e.error_type] = summary.get(e.error_type, 0) + 1
        print(f"SearX search failed across instances. Error summary: {summary}")

    return []


def find_instances() -> List[str]:
    """Return preferred candidate list (dynamic first)."""
    return get_candidate_instances(limit=20)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python search.py <query> [--instance URL] [--no-rotate] [--check]")
        print("")
        print("Examples:")
        print("  python search.py \"SearXNG docs\"")
        print("  python search.py \"query\" --instance https://searx.tiekoetter.com")
        print("  python search.py \"query\" --check")
        sys.exit(1)

    query = sys.argv[1]
    instance = None
    rotate = True
    check_mode = False

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--instance" and i + 1 < len(sys.argv):
            instance = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--no-rotate":
            rotate = False
            i += 1
        elif sys.argv[i] == "--check":
            check_mode = True
            i += 1
        else:
            i += 1

    if check_mode:
        candidates = find_instances()[:12]
        print("Checking candidate instances...\n")
        for inst in candidates:
            ok = check_instance(inst)
            print(f"{'OK ' if ok else 'BAD'}  {inst}")
        sys.exit(0)

    print(f"Searching via public SearX (clearnet): {query}")
    print(f"Instance: {instance or 'auto-select'}")
    print(f"Rotate: {rotate}")
    print()

    results = search_searx(query, instance=instance, rotate=rotate)

    print(f"Found {len(results)} results:\n")
    for r in results[:10]:
        print(f"  {r.get('title', 'No title')[:90]}")
        print(f"    {r.get('url', '')}")
        content = r.get("content", "")
        if content:
            print(f"    {content[:130]}...")
        print()
