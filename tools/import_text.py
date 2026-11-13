#!/usr/bin/env python3
"""Copy original wording from the old site into the data files, so nothing is retyped or reworded.

Usage: python tools/import_text.py
- Project descriptions: calplug.org/projects  -> data/projects.json  ("description", original paragraphs)
- Director and staff bios: calplug.org/about/team -> data/people.json ("bio")
Only the spelling fixes in FIXES are applied. Existing "_flag" items are left alone.
"""
import difflib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_SITE = "https://www.calplug.org"
FIXES = {"adopption": "adoption", "short-tern term": "short-term", "Opimization": "Optimization", "benifiting": "benefiting",
         "accessibble": "accessible", "Commision": "Commission", "Edision": "Edison", "Sponser": "Sponsor",
         "Dr. Li serves as director of California Institute": "Dr. Li served as director of California Institute",
         "tends to address": "aims to address", "replying on": "relying on", "are been constructed": "are being constructed"}
BLOCK = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li"}


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.tag, self.buf, self.skip = [], None, [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "nav", "header", "footer"):
            self.skip += 1
        if tag in BLOCK and not self.skip:
            self.flush()
            self.tag = tag

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "header", "footer"):
            self.skip = max(0, self.skip - 1)
        if tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if self.tag and not self.skip:
            self.buf.append(data)

    def flush(self):
        if self.tag:
            text = re.sub(r"\s+", " ", "".join(self.buf)).replace("​", "").strip()
            if text:
                self.out.append((self.tag, text))
        self.tag, self.buf = None, []


def blocks(path):
    req = urllib.request.Request(OLD_SITE + path, headers={"User-Agent": "Mozilla/5.0 (calplug-site-import)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        p = Blocks()
        p.feed(r.read().decode("utf-8", "ignore"))
        p.flush()
        return p.out


def fix(text):
    for a, b in FIXES.items():
        text = text.replace(a, b)
    return text


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def import_projects():
    f = ROOT / "data" / "projects.json"
    data = json.loads(f.read_text(encoding="utf-8"))
    by_title = {norm(p["title"]): p for p in data["projects"]}
    found, current, paras = 0, None, []

    def close():
        nonlocal found
        if current is not None and paras and not current.get("_flag", "").startswith("The description on the current site duplicates"):
            current["description"] = [fix(x) for x in paras]
            found += 1

    for tag, text in blocks("/projects"):
        if tag in ("h3", "h4"):
            close()
            current, paras = None, []
            m = difflib.get_close_matches(norm(fix(text)), list(by_title), n=1, cutoff=0.75)
            if m:
                current = by_title[m[0]]
            continue
        if current is None or tag != "p":
            continue
        if re.match(r"^(Sponsor|Sponser)\b", text) or re.match(r"^(Report|Final Report|Software Report|Article)\s*:", text):
            continue
        paras.append(text)
    close()
    f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    missing = [p["title"][:50] for p in data["projects"] if not isinstance(p.get("description"), list)]
    print(f"Project descriptions imported: {found}; without original text: {missing}")


def import_bios():
    f = ROOT / "data" / "people.json"
    data = json.loads(f.read_text(encoding="utf-8"))
    n = 0
    for tag, text in blocks("/about/team"):
        if tag != "p":
            continue
        if text.startswith("G. P. Li is a professor"):
            data["director"]["bio"] = fix(text)
            n += 1
        # Staff bios on the old page are not in <p> tags; they were copied by hand into people.json.
    f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Bios imported: {n}")


if __name__ == "__main__":
    import_projects()
    import_bios()
