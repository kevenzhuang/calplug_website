#!/usr/bin/env python3
"""Render tools/share/share.html to assets/brand/share.png (1200x630), the picture shown when the site is shared.

Only needed when the design of the share image changes. Needs Playwright and a Chromium browser:
  pip install playwright && python -m playwright install chromium
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630})
    page.goto((ROOT / "tools" / "share" / "share.html").as_uri())
    page.wait_for_timeout(500)
    page.locator(".card").screenshot(path=str(ROOT / "assets" / "brand" / "share.png"))
    browser.close()
print("Wrote assets/brand/share.png")
