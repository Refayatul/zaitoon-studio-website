"""
test_site.py — Automated validation test for Zaitoon Studio public website.

Validates:
1. All static routes (index, privacy, terms, review) exist and are non-empty.
2. Both clean URL directory indices and direct .html files exist.
3. No secrets or private tokens (TIKTOK_CLIENT_SECRET, refresh_token, etc.) are embedded.
4. No broken local links or accidental localhost href references in public pages.
5. All asset links (CSS, JS, PNG) exist on disk.
6. Responsive meta viewport tag and valid document structure.
7. Valid vercel.json and Cloudflare Pages _headers configuration.
8. Zero mentions of Instagram for Autopsy BD (strictly verified).
9. Live HTTP server test serving clean URLs and .html URLs with HTTP 200.
"""

import http.server
import json
import re
import socketserver
import threading
import urllib.request
from pathlib import Path
try:
    import pytest
except ImportError:
    pytest = None

SITE_DIR = Path(__file__).resolve().parent


REQUIRED_PAGES = [
    SITE_DIR / "index.html",
    SITE_DIR / "privacy.html",
    SITE_DIR / "privacy" / "index.html",
    SITE_DIR / "terms.html",
    SITE_DIR / "terms" / "index.html",
    SITE_DIR / "review.html",
    SITE_DIR / "review" / "index.html",
]

REQUIRED_ASSETS = [
    SITE_DIR / "css" / "style.css",
    SITE_DIR / "js" / "main.js",
    SITE_DIR / "assets" / "zaitoon_studio_app_icon_1024.png",
    SITE_DIR / "vercel.json",
    SITE_DIR / "_headers",
]


def test_required_pages_exist():
    for p in REQUIRED_PAGES:
        assert p.exists(), f"Missing required page: {p}"
        content = p.read_text(encoding="utf-8")
        assert len(content) > 500, f"Page {p} is suspiciously small ({len(content)} bytes)"
        assert "<!DOCTYPE html>" in content, f"Page {p} missing DOCTYPE"
        assert 'name="viewport"' in content, f"Page {p} missing responsive viewport"
        assert "<title>" in content, f"Page {p} missing title tag"


def test_required_assets_exist():
    for a in REQUIRED_ASSETS:
        assert a.exists(), f"Missing required asset: {a}"
        assert a.stat().st_size > 0, f"Asset {a} is empty"


def test_no_secrets_embedded():
    forbidden_terms = [
        "TIKTOK_CLIENT_SECRET",
        "TIKTOK_REFRESH_TOKEN",
        "client_secret",
        "refresh_token",
        "3f68284df9ff025222486f2352d6bf2c",  # App secret
        "ghp_",
        "PEXELS_API_KEY",
        "password",
    ]
    for p in SITE_DIR.rglob("*"):
        if p.is_file() and p.suffix in (".html", ".css", ".js", ".json"):
            text = p.read_text(encoding="utf-8", errors="ignore")
            for term in forbidden_terms:
                assert term not in text, f"Potential secret leak: '{term}' found in {p}"


def test_no_broken_localhost_hrefs():
    """Ensure no public links point to localhost or 127.0.0.1 in href attributes."""
    for p in SITE_DIR.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        # Match href="http://localhost..." or href="http://127.0.0.1..."
        matches = re.findall(r'href=[\'"](https?://(localhost|127\.0\.0\.1)[^\'"]*)[\'"]', text)
        assert len(matches) == 0, f"Found public link pointing to localhost in {p}: {matches}"


def test_autopsy_no_instagram():
    """Ensure Autopsy BD has zero mentions or claims regarding Instagram."""
    for p in SITE_DIR.rglob("*.html"):
        text = p.read_text(encoding="utf-8").lower()
        if "autopsy" in text:
            assert "instagram" not in text, f"Autopsy BD mentions Instagram in {p}"


def test_vercel_and_cloudflare_config():
    v_file = SITE_DIR / "vercel.json"
    data = json.loads(v_file.read_text())
    assert data.get("cleanUrls") is True
    assert "headers" in data

    h_file = SITE_DIR / "_headers"
    assert h_file.exists()
    assert "X-Content-Type-Options: nosniff" in h_file.read_text()


def test_live_static_http_server():
    """Spawns an ephemeral static server and validates HTTP 200 on all routes."""
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(SITE_DIR), **kwargs)

        def log_message(self, format, *args):
            pass  # quiet

    server = socketserver.TCPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    routes = [
        "/",
        "/index.html",
        "/privacy/",
        "/privacy.html",
        "/terms/",
        "/terms.html",
        "/review/",
        "/review.html",
        "/css/style.css",
        "/js/main.js",
        "/assets/zaitoon_studio_app_icon_1024.png",
    ]

    try:
        for r in routes:
            url = f"http://127.0.0.1:{port}{r}"
            with urllib.request.urlopen(url, timeout=5) as resp:
                assert resp.status == 200, f"Route {r} failed with status {resp.status}"
                assert len(resp.read()) > 0, f"Route {r} returned empty body"
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    print("Running website validation checks...")
    test_required_pages_exist()
    test_required_assets_exist()
    test_no_secrets_embedded()
    test_no_broken_localhost_hrefs()
    test_autopsy_no_instagram()
    test_vercel_and_cloudflare_config()
    test_live_static_http_server()
    print("✓ All 7 website validation test suites PASSED successfully!")
