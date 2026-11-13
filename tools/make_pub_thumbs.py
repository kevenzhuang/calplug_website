#!/usr/bin/env python3
"""Make a thumbnail for every publication that has a link.

Usage: python tools/make_pub_thumbs.py   (needs `pdftoppm` from poppler-utils and ImageMagick `convert`)
Output: assets/pubs/<key>.jpg, where key = first 12 characters of sha1(url).

Tried in this order for each link:
  1. the link is a PDF                         -> first page
  2. the page names a PDF (citation_pdf_url, or a link ending in .pdf) -> first page of that PDF
  3. the page has a preview image (og:image)   -> that image
Anything else keeps the standard default image (assets/brand/pub-default.svg).
"""
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_SITE = "https://www.calplug.org"
OUT = ROOT / "assets" / "pubs"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
      "Accept": "text/html,application/pdf,image/*,*/*"}


def key(url):
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read(), r.geturl()


def pdf_to_jpg(data, dest):
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "p.pdf"
        pdf.write_bytes(data)
        subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-jpeg", "-singlefile", "-scale-to-x", "360",
                        "-scale-to-y", "-1", str(pdf), str(dest.with_suffix(""))], check=True, timeout=120)


def image_to_jpg(data, dest):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "i"
        src.write_bytes(data)
        subprocess.run(["convert", f"{src}[0]", "-resize", "360x", "-background", "white", "-flatten", str(dest)],
                       check=True, timeout=120)


def make(url, dest):
    full = OLD_SITE + urllib.parse.quote(url) if url.startswith("/") else url
    data, final = get(full)
    if data.startswith(b"%PDF"):
        pdf_to_jpg(data, dest)
        return "pdf"
    html = data.decode("utf-8", "ignore")
    candidates = re.findall(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html)
    candidates += re.findall(r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']', html)[:3]
    for c in candidates:
        try:
            d2, _ = get(urllib.parse.urljoin(final, c))
            if d2.startswith(b"%PDF"):
                pdf_to_jpg(d2, dest)
                return "pdf found on page"
        except Exception:
            continue
    og = re.findall(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html)
    if og:
        d3, _ = get(urllib.parse.urljoin(final, og[0].replace("&amp;", "&")))
        image_to_jpg(d3, dest)
        return "preview image"
    raise ValueError("no PDF or preview image found")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pubs = json.loads((ROOT / "data" / "publications.json").read_text(encoding="utf-8"))["publications"]
    made, skipped, failed = {}, 0, []
    for p in pubs:
        url = p.get("url")
        if not url:
            continue
        dest = OUT / f"{key(url)}.jpg"
        if dest.exists():
            skipped += 1
            continue
        try:
            how = make(url, dest)
            made[how] = made.get(how, 0) + 1
        except Exception as ex:
            failed.append(f"{p['title'][:60]}: {str(ex)[:80]}")
    print(f"Thumbnails made {made}, already present {skipped}, failed {len(failed)}")
    for f in failed:
        print("  FAILED", f)


if __name__ == "__main__":
    main()
