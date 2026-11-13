#!/usr/bin/env python3
"""Copy the images that data/*.json points to on the old WordPress site into assets/legacy/.

Usage: python tools/import_assets.py
Run it once per new image path. Files already present are skipped.
"""
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_SITE = "https://www.calplug.org"
PATTERN = re.compile(r'"(?:https?://(?:www\.)?calplug\.org)?(/wp-content/uploads/[^"]+\.(?:png|jpe?g|gif|webp|avif|svg))"', re.I)
EXTRA = ["/wp-content/uploads/calpluglogo-small.png", "/wp-content/uploads/zotwatt-2.jpg",
         "/wp-content/uploads/clplg_space.jpg"]


def main():
    paths = set(EXTRA)
    sources = list((ROOT / "data").glob("*.json")) + list((ROOT / "content" / "legacy").glob("*.html"))
    for f in sources:
        paths.update(PATTERN.findall(f.read_text(encoding="utf-8")))
    ok = skipped = 0
    failed = []
    for p in sorted(paths):
        dest = ROOT / "assets" / "legacy" / p[len("/wp-content/uploads/"):]
        if dest.exists():
            skipped += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(OLD_SITE + urllib.parse.quote(p), headers={"User-Agent": "calplug-site-import"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                dest.write_bytes(r.read())
            ok += 1
        except Exception as ex:  # report and continue
            failed.append(f"{p}: {ex}")
    print(f"Downloaded {ok}, already present {skipped}, failed {len(failed)}")
    for f in failed:
        print("  FAILED", f)
    sys.exit(1 if failed and not ok and not skipped else 0)


if __name__ == "__main__":
    main()
