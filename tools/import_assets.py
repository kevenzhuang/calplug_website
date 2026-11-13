#!/usr/bin/env python3
"""Copy the files that data/*.json and content/legacy/*.html point to on the old WordPress site into this repository.

Images go to assets/legacy/. Documents (PDF) go to wp-content/uploads/, the same path they had on the old site,
so that addresses already used in papers, e-mails and other websites keep working after the domain moves.

Usage: python tools/import_assets.py
Run it once per new path. Files already present are skipped.
"""
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_SITE = "https://www.calplug.org"
PATTERN = re.compile(r'"(?:https?://(?:www\.)?calplug\.org)?(/wp-content/uploads/[^"]+\.(?:png|jpe?g|gif|webp|avif|svg))"', re.I)
DOCS = re.compile(r'"(?:https?://(?:www\.)?calplug\.org)?(/wp-content/uploads/[^"]+\.pdf)"', re.I)
DOC_LIMIT = 90 * 1024 * 1024  # GitHub refuses files over 100 MB; anything over 90 MB is reported, not stored
EXTRA = ["/wp-content/uploads/calpluglogo-small.png", "/wp-content/uploads/zotwatt-2.jpg",
         "/wp-content/uploads/clplg_space.jpg",
         "/wp-content/uploads/calpluglogo2022.jpg"]  # largest copy of the logo on the old site (1187 px wide)


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
    # Documents keep their old path (see the note at the top of this file).
    docs = set()
    for f in sources:
        docs.update(DOCS.findall(f.read_text(encoding="utf-8")))
    total = 0
    for p in sorted(docs):
        dest = ROOT / urllib.parse.unquote(p)[1:]
        if dest.exists():
            skipped += 1
            total += dest.stat().st_size
            continue
        req = urllib.request.Request(OLD_SITE + urllib.parse.quote(urllib.parse.unquote(p)), headers={"User-Agent": "calplug-site-import"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if not data.startswith(b"%PDF"):
                failed.append(f"{p}: the old site did not return a PDF")
                continue
            if len(data) > DOC_LIMIT:
                failed.append(f"{p}: {len(data) // 1048576} MB, over the {DOC_LIMIT // 1048576} MB limit; left on the old site")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            total += len(data)
            ok += 1
        except Exception as ex:  # report and continue
            failed.append(f"{p}: {ex}")
    print(f"Documents: {len(docs)} listed, {total // 1048576} MB stored in wp-content/uploads/")
    # Images hosted on other sites (project figures, mentor photos): keep a copy in assets/ext/ so the site
    # does not break when the other site moves them. The name is a hash of the address (see ext_name in build.py).
    import hashlib, os
    ext_pat = re.compile(r'"(https?://(?!(?:www\.)?calplug\.org)[^"]+\.(?:png|jpe?g|gif|webp)(?:\?[^"]*)?)"', re.I)
    for f in (ROOT / "data").glob("*.json"):
        for u in set(ext_pat.findall(f.read_text(encoding="utf-8"))):
            ext = os.path.splitext(u.split("?")[0])[1].lower()
            dest = ROOT / "assets" / "ext" / (hashlib.sha1(u.encode()).hexdigest()[:12] + ext)
            if dest.exists():
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (calplug-site-import)"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    dest.write_bytes(r.read())
                ok += 1
            except Exception as ex:
                failed.append(f"{u}: {ex}")
    print(f"Downloaded {ok}, already present {skipped}, failed {len(failed)}")
    for f in failed:
        print("  FAILED", f)
    sys.exit(1 if failed and not ok and not skipped else 0)


if __name__ == "__main__":
    main()
