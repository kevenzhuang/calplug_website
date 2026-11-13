#!/usr/bin/env python3
"""Copy whole pages from the old site, word for word, into content/legacy/<slug>.html.

Usage: python tools/import_pages.py
Keeps text, headings, lists, links, tables and images; drops scripts, styling and page chrome.
The build wraps each file in the site template. Edit these files by hand only to fix spelling.
"""
import re
import urllib.request
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_SITE = "https://www.calplug.org"
PAGES = {"sim-home": "/sim-home", "sim-lab": "/sim-lab", "1-kwh-challenge": "/1-kwh-challenge",
         "careers": "/about/careers", "events-archive": "/eventsarchive", "support": "/support",
         "friends": "/friends", "members": "/members-2"}
KEEP = {"p", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "a", "img", "strong", "b", "em", "i", "br",
        "table", "thead", "tbody", "tr", "td", "th", "blockquote"}
SKIP = {"script", "style", "noscript", "svg", "form", "button", "nav", "header", "footer", "iframe", "h1"}
VOID = {"img", "br"}


class Clean(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.depth_main, self.skip, self.in_main = [], 0, 0, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main" and not self.in_main:
            self.in_main, self.depth_main = True, 1
            return
        if not self.in_main:
            return
        if tag == "main":
            self.depth_main += 1
        if tag in SKIP:
            if tag not in VOID:
                self.skip += 1
            return
        if self.skip or tag not in KEEP:
            return
        if tag == "a":
            self.out.append(f'<a href="{escape(a.get("href") or "#", quote=True)}">')
        elif tag == "img":
            src = a.get("src") or ""
            if src.startswith("data:"):
                src = a.get("data-src") or a.get("data-lazy-src") or ""
            if src:
                self.out.append(f'<img src="{escape(src, quote=True)}" alt="{escape(a.get("alt") or "", quote=True)}" loading="lazy">')
        elif tag == "br":
            self.out.append("<br>")
        else:
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if not self.in_main:
            return
        if tag == "main":
            self.depth_main -= 1
            if self.depth_main == 0:
                self.in_main = False
            return
        if tag in SKIP:
            if tag not in VOID:
                self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in KEEP or tag in VOID:
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if self.in_main and not self.skip:
            self.out.append(escape(data, quote=False))


def clean(html):
    p = Clean()
    p.feed(html)
    out = "".join(p.out).replace("​", "")
    out = re.sub(r"[ \t\r\f\v]+", " ", out)
    for _ in range(4):  # remove empty elements left behind
        out = re.sub(r"<(p|h[2-6]|li|ul|ol|strong|b|em|i|a|blockquote)(?: [^>]*)?>\s*(?:<br>\s*)*</\1>", "", out)
    out = re.sub(r"\n\s*\n+", "\n", out)
    out = re.sub(r"(</(?:p|h[2-6]|ul|ol|table|blockquote|li|tr)>)", r"\1\n", out)
    return out.strip() + "\n"


def main():
    dest = ROOT / "content" / "legacy"
    dest.mkdir(parents=True, exist_ok=True)
    for slug, path in PAGES.items():
        req = urllib.request.Request(OLD_SITE + path, headers={"User-Agent": "Mozilla/5.0 (calplug-site-import)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            html = r.read().decode("utf-8", "ignore")
        text = clean(html)
        (dest / f"{slug}.html").write_text(text, encoding="utf-8")
        print(f"{slug}: {len(re.sub('<[^>]+>', ' ', text).split())} words, {text.count('<img')} images")


if __name__ == "__main__":
    main()
