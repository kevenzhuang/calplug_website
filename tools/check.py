#!/usr/bin/env python3
"""Check the built site in dist/. Run after tools/build.py. Exits 1 if anything fails.

Checks: internal links and files exist, every image has an alt attribute, no placeholder text,
exactly one h1 per page, a title and description on every page, no empty sections.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
PLACEHOLDER = re.compile(r"\b(lorem ipsum|coming soon|TODO|TBD|placeholder)\b|>\s*test\s*<", re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.h1, self.ids = [], [], 0, set()
        self.title = self.desc = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("link", "script") and (a.get("href") or a.get("src")):
            self.links.append(a.get("href") or a.get("src"))
        if tag == "img":
            self.imgs.append(a)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.title = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.desc = True


def main():
    problems = []
    pages = {}
    for f in sorted(DIST.glob("*.html")):
        p = Page()
        text = f.read_text(encoding="utf-8")
        p.feed(text)
        pages[f.name] = (p, text)
    for name, (p, text) in pages.items():
        if p.h1 != 1:
            problems.append(f"{name}: has {p.h1} h1 headings, needs exactly 1")
        if not p.title or not p.desc:
            problems.append(f"{name}: missing title or description")
        if PLACEHOLDER.search(text):
            problems.append(f"{name}: placeholder text found: {PLACEHOLDER.search(text).group(0)!r}")
        if re.search(r'<(ul|div) class="(grid[^"]*|rows|logos[^"]*|chips[^"]*)">\s*</\1>', text):
            problems.append(f"{name}: an empty section is being published")
        for im in p.imgs:
            if "alt" not in im:
                problems.append(f"{name}: image without alt: {im.get('src')}")
            src = im.get("src", "")
            if not src.startswith("http") and not (DIST / src).exists():
                problems.append(f"{name}: image file missing: {src}")
        for href in p.links:
            if href.startswith(("http", "mailto:", "tel:")):
                continue
            path, _, frag = href.partition("#")
            target = name if not path else path
            if path and not (DIST / path).exists():
                problems.append(f"{name}: broken link: {href}")
            elif frag and target in pages and frag not in pages[target][0].ids:
                problems.append(f"{name}: link to missing section: {href}")
    if problems:
        print(f"{len(problems)} problem(s):")
        for x in problems:
            print("  -", x)
        sys.exit(1)
    print(f"All checks passed on {len(pages)} pages.")


if __name__ == "__main__":
    main()
