#!/usr/bin/env python3
"""Check the built site in dist/. Run after tools/build.py. Exits 1 if anything fails.

Checks: internal links and files exist, every image has an alt attribute, no placeholder text,
exactly one h1 per page, a title and description on every page, no empty sections,
and the bullet rules of DESIGN.md section 5 (no one-item lists, no lists mixing sentences and phrases).
Also: heading levels do not skip, no image over 400 KB, the arrow link is only used for pages of this site,
times are written one way, and no paragraph runs past 150 words.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
TIME = re.compile(r"\b\d{1,2}(?::\d{2})?\s?(?:AM|PM|a\.m\.|p\.m\.)(?!\w)|\b\d{1,2}(?::\d{2})?(?:am|pm)\b|\b(?:PST|PDT|EST|EDT|MST|MDT|CST|CDT)\b")
MAX_PARAGRAPH = 150  # words (DESIGN.md section 5)
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


class CardRows(HTMLParser):
    """Collects, for every grid of cards, whether each card contains a bullet list."""
    VOID = {"img", "br", "hr", "input", "meta", "link", "source"}

    def __init__(self):
        super().__init__()
        self.stack, self.rows = [], []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        cls = (dict(attrs).get("class") or "").split()
        kind = "grid" if "grid" in cls and "cards" in cls else "card" if "card" in cls else None
        if kind == "grid":
            self.rows.append([])
        if kind == "card" and self.stack and self.stack[-1][1] == "grid":
            self.rows[-1].append(False)
            kind = "card-in-grid"
        if tag == "ul":
            for t, k in reversed(self.stack):
                if k == "card-in-grid":
                    self.rows[-1][-1] = True
                    break
        self.stack.append((tag, kind))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def css_problems():
    """Token rule (DESIGN.md section 3): outside :root, styles may not use raw colors, font sizes, weights,
    line heights, radii, durations, or spacing of 4px and more. Values up to 3px are hairlines and optical nudges."""
    css = (DIST / "css" / "site.css").read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"@font-face\s*\{[^}]*\}", "", css)
    css = re.sub(r":root\s*\{[^}]*\}", "", css)
    out = []
    rules = [
        (r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", "a raw color"),
        (r"font-size:(?!\s*var\()[^;}]+", "a raw font size"),
        (r"font-weight:(?!\s*(?:var\(|inherit))[^;}]+", "a raw font weight"),
        (r"line-height:(?!\s*(?:var\(|calc\(|1[;}\s]))[^;}]+", "a raw line height"),
        (r"border-radius:(?!\s*(?:var\(|50%|0 var\())[^;}]+", "a raw radius"),
        (r"transition:[^;}]*\d(?:ms|s)\b[^;}]*", "a raw duration"),
        (r"(?:padding|margin|gap)[a-z-]*:[^;}]*(?<![\w.-])(?:[4-9]|\d{2,})(?:\.\d+)?px[^;}]*", "raw spacing of 4px or more"),
    ]
    for pat, what in rules:
        for m in re.finditer(pat, css):
            out.append(f"css/site.css: {what}: {m.group(0).strip()[:70]!r} (use a token from DESIGN.md section 3)")
    return out


def main():
    problems = css_problems()
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
        main = text[text.find("<main"):text.find("</main>")]
        for attrs, body in re.findall(r"<ul([^>]*)>(.*?)</ul>", main, re.S):
            if any(k in attrs for k in ("grid", "logo-grid", "plain", "steps")):
                continue
            items = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<li[^>]*>(.*?)</li>", body, re.S)]
            ends = [x.endswith((".", "!", "?")) for x in items]
            if len(items) == 1:
                problems.append(f"{name}: a bullet list with one item (use a sentence): {items[0][:50]!r}")
            elif 0 < sum(ends) < len(ends):
                problems.append(f"{name}: a bullet list mixing full sentences and short phrases: {items[0][:50]!r}")
        levels = [int(x) for x in re.findall(r"<h([1-6])[\s>]", main)]
        for prev, cur in zip(levels, levels[1:]):
            if cur > prev + 1:
                problems.append(f"{name}: heading levels skip from h{prev} to h{cur}")
                break
        big = [im.get("src") for im in p.imgs if im.get("src", "").startswith("assets/") and (DIST / im["src"]).exists()
               and (DIST / im["src"]).stat().st_size > 400_000]
        for src in big:
            problems.append(f"{name}: image over 400 KB: {src} (run tools/optimize_images.py)")
        # The arrow means "another page of this site" (DESIGN.md section 3, Link marks)
        for href in re.findall(r'<a class="more" href="([^"]*)"', main):
            if href.startswith(("http", "mailto:", "tel:", "#")):
                problems.append(f"{name}: an arrow link that does not go to a page of this site: {href[:60]}")
        # Times are written "5:00 pm PT" (DESIGN.md section 5, Dates and times)
        plain = re.sub(r"<[^>]+>", " ", main)
        for m in TIME.finditer(plain):
            problems.append(f"{name}: time not in the site's format (write 5:00 pm PT): {m.group(0)!r}")
        for para in re.findall(r"<p[^>]*>(.*?)</p>", main, re.S):
            n = len(re.sub(r"<[^>]+>", " ", para).split())
            if n > MAX_PARAGRAPH:
                problems.append(f"{name}: a paragraph of {n} words (limit {MAX_PARAGRAPH}; split it where a new step or topic starts): {re.sub(r'<[^>]+>', '', para)[:50]!r}")
        # Cards side by side share one shape: either all of them hold a bullet list or none does
        rows = CardRows()
        rows.feed(main)
        for shapes in rows.rows:
            if len(shapes) > 1 and 0 < sum(shapes) < len(shapes):
                problems.append(f"{name}: cards in one row mix bullet lists and plain text")
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
            path = path.split("?")[0]
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
