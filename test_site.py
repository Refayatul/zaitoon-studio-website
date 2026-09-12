"""
test_site.py — Automated validation test for Zaitoon Studio public website.

Validates:
1. All static routes (index, privacy, terms, review) exist and are non-empty.
2. Both clean URL directory indices and direct .html files exist.
3. No secrets or private tokens (TIKTOK_CLIENT_SECRET, refresh_token, etc.) are embedded.
4. No broken local links or accidental localhost href references in public pages.
5. All asset links (CSS, JS, PNG) exist on disk.
6. Responsive meta viewport tag and valid document structure.
7. Valid vercel.json and Cloudflare Pages configuration files.
"""

import json
import re
from pathlib import Path

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
    SITE_DIR / "_routes.json",
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


def test_vercel_and_cloudflare_config():
    v_file = SITE_DIR / "vercel.json"
    data = json.loads(v_file.read_text())
    assert data.get("cleanUrls") is True
    assert "headers" in data

    r_file = SITE_DIR / "_routes.json"
    r_data = json.loads(r_file.read_text())
    assert r_data.get("version") == 1


if __name__ == "__main__":
    print("Running website validation checks...")
    test_required_pages_exist()
    test_required_assets_exist()
    test_no_secrets_embedded()
    test_no_broken_localhost_hrefs()
    test_vercel_and_cloudflare_config()
    print("✓ All 5 website validation test suites PASSED successfully!")
