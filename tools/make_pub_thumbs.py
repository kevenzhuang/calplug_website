#!/usr/bin/env python3
"""Make a first-page thumbnail for every publication whose link is a PDF.

Usage: python tools/make_pub_thumbs.py   (needs `pdftoppm` from poppler-utils)
Output: assets/pubs/<key>.jpg, where key = first 12 characters of sha1(url).
Publications without a PDF link keep the standard type tile (see DESIGN.md, Publications).
"""
import hashlib
import json
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_SITE = "https://www.calplug.org"
OUT = ROOT / "assets" / "pubs"


def key(url):
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pubs = json.loads((ROOT / "data" / "publications.json").read_text(encoding="utf-8"))["publications"]
    made = skipped = 0
    failed = []
    for p in pubs:
        url = p.get("url") or ""
        if not url.split("?")[0].lower().endswith(".pdf"):
            continue
        dest = OUT / f"{key(url)}.jpg"
        if dest.exists():
            skipped += 1
            continue
        full = OLD_SITE + urllib.parse.quote(url) if url.startswith("/") else url
        try:
            req = urllib.request.Request(full, headers={"User-Agent": "Mozilla/5.0 (calplug-site-import)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if not data.startswith(b"%PDF"):
                raise ValueError("not a PDF")
            with tempfile.TemporaryDirectory() as tmp:
                pdf = Path(tmp) / "p.pdf"
                pdf.write_bytes(data)
                subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-jpeg", "-singlefile", "-scale-to-x", "360",
                                "-scale-to-y", "-1", str(pdf), str(dest.with_suffix(""))], check=True, timeout=120)
            made += 1
        except Exception as ex:
            failed.append(f"{p['title'][:60]}: {ex}")
    print(f"Thumbnails made {made}, already present {skipped}, failed {len(failed)}")
    for f in failed:
        print("  FAILED", f)


if __name__ == "__main__":
    main()
