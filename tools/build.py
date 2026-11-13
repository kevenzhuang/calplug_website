#!/usr/bin/env python3
"""Build the CalPlug site: data/*.json + templates below -> dist/*.html.

Usage: python tools/build.py
Standard library only. Fails with a clear message when data is missing a required field.
"""
import hashlib
import os
import json
import re
import shutil
import sys
from datetime import date
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, SRC, DIST, ASSETS = ROOT / "data", ROOT / "src", ROOT / "dist", ROOT / "assets"
OLD_SITE = "https://www.calplug.org"
ERRORS = []
MISSING = []  # files the data points to on the old site that have not been imported yet
# Version stamp so browsers fetch new CSS/JS after a change (DESIGN.md: cache and versions)
STAMP = hashlib.sha1(b"".join(f.read_bytes() for f in sorted((SRC).rglob("*.*")))).hexdigest()[:8]

NEWS_DEFAULT = "assets/brand/news-default.svg"
PUB_LABELS = {"journal": "Journal", "conference": "Conference", "report": "Report", "press": "In the press"}

# Eight items of equal rank, no buttons, no drop-down menus (DESIGN.md section 2). The logo goes home.
NAV = [
    ("about.html", "About"), ("people.html", "People"), ("research.html", "Research"),
    ("publications.html", "Publications"), ("news.html", "News"), ("careers.html", "Careers"), ("support.html", "Support"), ("contact.html", "Contact"),
]
# which top-level item is "current" for each page
SECTION = {"sim-home.html": "research.html", "sim-lab.html": "research.html", "1-kwh-challenge.html": "research.html",
           "facilities.html": "research.html", "events-archive.html": "news.html"}
OLD_LINKS = {"/sim-home": "sim-home.html", "/sim-lab": "sim-lab.html", "/1-kwh-challenge": "1-kwh-challenge.html",
             "/friends": "support.html#friends", "/members-2": "support.html#members", "/support": "support.html",
             "/affiliations": "support.html#affiliates", "/about/careers": "careers.html", "/about/contact": "contact.html",
             "/eventsarchive": "events-archive.html", "/projects": "research.html", "/publications": "publications.html",
             "/about/team": "people.html#team", "/about": "about.html", "/facilities": "research.html#labs", "/": "index.html", "": "index.html"}


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def need(item, fields, where):
    for f in fields:
        if not item.get(f):
            ERRORS.append(f"{where}: '{item.get('id') or item.get('name') or item.get('title')}' is missing '{f}'")


def ext_name(u):
    """File name under assets/ext/ for an image hosted on another site (see tools/import_assets.py)."""
    ext = os.path.splitext(u.split("?")[0])[1].lower()
    return hashlib.sha1(u.encode()).hexdigest()[:12] + (ext if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg") else ".jpg")


def url(path):
    """Where an image or file is served from: a smaller optimized copy (assets/opt) when there is one, then the
    imported copy (assets/legacy for the old site, assets/ext for other sites), otherwise the original address."""
    if not path:
        return ""
    path = re.sub(r"^https?://(?:www\.)?calplug\.org(?=/wp-content/)", "", path)
    local = None
    if path.startswith("/wp-content/uploads/"):
        if (ROOT / path[1:]).is_file():
            return path[1:]  # documents (PDF) keep the address they had on the old site, so links from elsewhere still work
        local = "assets/legacy/" + path[len("/wp-content/uploads/"):]
        if not (ROOT / local).exists():
            MISSING.append(path)
            return OLD_SITE + path
    elif path.startswith("http") and re.search(r"\.(png|jpe?g|gif|webp)(\?|$)", path, re.I) and (ASSETS / "ext" / ext_name(path)).exists():
        local = "assets/ext/" + ext_name(path)
    elif path.startswith("assets/"):
        local = path
    if local:
        opt = "assets/opt/" + local[len("assets/"):] + ".jpg"
        return opt if (ROOT / opt).exists() else local
    return path


def img_size(rel):
    """Pixel size of a local PNG, GIF or JPEG, read from the file header (standard library only)."""
    try:
        with open(ROOT / rel, "rb") as f:
            h = f.read(26)
            if h[:8] == b"\x89PNG\r\n\x1a\n":
                return int.from_bytes(h[16:20], "big"), int.from_bytes(h[20:24], "big")
            if h[:6] in (b"GIF87a", b"GIF89a"):
                return int.from_bytes(h[6:8], "little"), int.from_bytes(h[8:10], "little")
            if h[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    m = f.read(4)
                    if len(m) < 4 or m[0] != 0xFF:
                        return None
                    n = int.from_bytes(m[2:4], "big")
                    if 0xC0 <= m[1] <= 0xCF and m[1] not in (0xC4, 0xC8, 0xCC):
                        d = f.read(5)
                        return int.from_bytes(d[3:5], "big"), int.from_bytes(d[1:3], "big")
                    f.seek(n - 2, 1)
    except OSError:
        pass
    return None


def img(path, alt="", cls="", eager=False):
    """Images below the first screen load lazily; pass eager=True for images at the top of a page."""
    c = f' class="{cls}"' if cls else ""
    src = url(path)
    size = img_size(src) if not src.startswith("http") else None
    wh = f' width="{size[0]}" height="{size[1]}"' if size else ""  # reserves the space so the page does not jump while loading
    return f'<img src="{e(src)}" alt="{e(alt)}"{wh} loading="{"eager" if eager else "lazy"}"{c}>'


def links(items):
    if not items:
        return ""
    return '<div class="links">' + "".join(
        f'<a href="{e(url(l["url"]))}">{e(l["label"])}</a>' for l in items) + "</div>"


def more_link(href, label):
    """A text link that stands alone. The arrow (added by CSS on .more) means "another page of this site" and nothing
    else, so links that leave the site, write an e-mail or jump within the page do not get the class (DESIGN.md section 3)."""
    cls = ' class="more"' if re.match(r"[a-z0-9-]+\.html", href) else ""
    return f'<a{cls} href="{e(href)}">{e(label)}</a>'


def paras(p):
    """Original description as a list of paragraphs (data may hold a string or a list)."""
    d = p.get("description") or []
    return [d] if isinstance(d, str) else d




def years(p):
    s, en = p.get("start"), p.get("end")
    if not s:
        return ""
    return str(s) if s == en or not en else f"{s}–{en}"


NOBREAK = ["UC Irvine", "Calit2 Building", "CalPlug/ITAC", "Calit2 UCI Division", "Dr. Shuoyu (Arnold) Wang", "Dr. G. P. Li"]


def nobreak(html):
    """Keep names and fixed terms on one line (DESIGN.md section 3, Line breaks). Text only, never inside tags or URLs."""
    def fix(s):
        for term in NOBREAK:
            s = s.replace(term, term.replace(" ", "\u00a0"))
        s = re.sub(r"\b([A-Z]{2,4})-([A-Z]?\d{2,4})\b", "\\1\u2011\\2", s)  # IDs such as DC-S26
        s = re.sub(r"\b(\w{2,4})-(\w{2,4})\b", "\\1\u2011\\2", s)  # short hyphenated words such as Net-load, AI-TES
        return s.replace(" \u2013 ", "\u00a0\u2013 ")  # a dash never starts a line
    return re.sub(r">([^<]+)<", lambda m: ">" + fix(m.group(1)) + "<", html)


def fmt_date(ev):
    if not ev.get("date"):
        return ""
    d = date.fromisoformat(ev["date"])
    out = f"{d.strftime('%b')} {d.day}, {d.year}"
    if ev.get("end_date"):
        d2 = date.fromisoformat(ev["end_date"])
        out = f"{d.strftime('%b')} {d.day}–{d2.day}, {d.year}"
    return out.replace(" ", "\u00a0")


def initials(name):
    parts = re.sub(r"\(.*?\)|,.*", "", name).split()
    return (parts[0][0] + parts[-1][0]).upper() if parts else ""


ICONS = {
    "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.69.24 2.69.24v2.97h-1.51c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg>',
}


# Ring icons (DESIGN.md section 6): the logo's half-blue, half-green ring around a line icon.
LINE_ICONS = {
    "plug": "M9 2v5M15 2v5M6 7h12v4a6 6 0 0 1-12 0zM12 17v5",
    "person": "M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8zM4 21a8 8 0 0 1 16 0",
    "factory": "M2 21h20M3 21V11l6 4v-4l6 4V4h5v17",
    "bolt": "M13 2L4 14h7l-1 8l9-12h-7z",
    "building": "M4 21V4h10v17M14 9h6v12M2 21h20M8 8h2M8 12h2M8 16h2M17 13h0.01M17 17h0.01",
    "calendar": "M5 5h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zM3 10h18M8 3v4M16 3v4",
    "document": "M6 3h8l5 5v13H6zM14 3v5h5M9 13h7M9 17h7",
    "cap": "M2 9l10-5l10 5l-10 5zM6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5M22 9v6",
    "signal": "M2.5 9a13.5 13.5 0 0 1 19 0M5.5 12.5a9 9 0 0 1 13 0M8.5 16a4.5 4.5 0 0 1 7 0M12 19.5h0.01",
    "heart": "M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z",
    "pin": "M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12zM12 6.5a2.5 2.5 0 1 1 0 5a2.5 2.5 0 0 1 0-5z",
}
# One ring icon per page title (DESIGN.md section 4, Page icon). Project pages use their research area's icon.
PAGE_ICON = {"About": "mark", "People": "person", "Research": "plug", "Publications": "document", "Our labs": "building",
             "News & Events": "calendar", "Events Archive": "calendar", "Careers": "cap", "Support & Memberships": "heart",
             "Contact": "pin", "SIM Home": "building", "SIM Lab": "building", "1 kWh Challenge": "bolt"}
AREA_ICON = {"plug-loads": "plug", "behavior": "person", "smart-manufacturing": "factory", "grid": "bolt", "buildings": "building"}


# The CalPlug icon itself, drawn to the original logo's measurements (assets/brand/calplug-mark.svg).
MARK_INNER = '<path d="M0 83A83 83 0 0 1 166 83H144.7A61.7 61.7 0 0 0 21.3 83Z" fill="#005BAA"/><path d="M0 83A83 83 0 0 0 166 83H144.7A61.7 61.7 0 0 1 21.3 83Z" fill="#8BC53F"/><g fill="none" stroke="#005BAA" stroke-width="7" stroke-linecap="round"><path d="M70.41 66.71A17.8 17.8 0 0 1 95.59 66.71"/><path d="M60.30 58.50A32.1 32.1 0 0 1 105.70 58.50"/><path d="M51.96 48.26A43.9 43.9 0 0 1 114.04 48.26"/></g><path d="M48 95.5H118A35 35 0 0 1 48 95.5Z" fill="#8BC53F"/><g stroke="#8BC53F" stroke-width="7.5" stroke-linecap="round"><path d="M67.1 81.5V96.5M98.9 81.5V96.5"/></g>'


def ring(icon, cls="ring"):
    """A line icon inside a ring with the logo's own proportions: inner radius 74% of outer, split on the
    horizontal, blue above and green below, icon drawn in the logo's blue with round ends.
    icon "mark" is the CalPlug icon itself."""
    if icon == "mark":
        return f'<svg class="{cls}" viewBox="0 0 166 166" aria-hidden="true">{MARK_INNER}</svg>'
    return (f'<svg class="{cls}" viewBox="0 0 32 32" aria-hidden="true">'
            f'<path d="M0 16A16 16 0 0 1 32 16H27.9A11.9 11.9 0 0 0 4.1 16Z" class="r-top"/>'
            f'<path d="M0 16A16 16 0 0 0 32 16H27.9A11.9 11.9 0 0 1 4.1 16Z" class="r-bottom"/>'
            f'<path d="{LINE_ICONS[icon]}" class="r-icon" transform="translate(8.5 8.5) scale(0.625)"/></svg>')


def share_image(site, image=None):
    """Picture shown when a page is shared (DESIGN.md section 6, Share image). Must be an absolute address."""
    if image and url(image).startswith("http"):
        return url(image)
    path = url(image) if image else "assets/brand/share.png"
    return f"{site['site_url'].rstrip('/')}/{path}"


def page(filename, title, description, body, site, image=None, extra_head=""):
    cur = SECTION.get(filename, filename)
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{e(label)}</a></li>' for h, label in NAV)
    c = site["contact"]
    full_title = "CalPlug \u2013 California Plug Load Research Center" if filename == "index.html" else f"{title} \u2013 CalPlug"
    social = "".join(f'<a href="{e(site["social"][k])}" aria-label="CalPlug on {k.title().replace("Linkedin", "LinkedIn")}">{ICONS[k]}</a>' for k in ("linkedin", "facebook"))
    body = nobreak(body)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#FFFFFF">
<meta name="robots" content="noindex, nofollow">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{e(site['site_url'].rstrip('/') + '/' + ('' if filename == 'index.html' else filename))}">
<meta property="og:image" content="{e(share_image(site, image))}">
<meta property="og:site_name" content="CalPlug">
<meta name="twitter:card" content="summary_large_image">{extra_head}
<link rel="icon" href="assets/brand/calplug-mark.svg" type="image/svg+xml">
<link rel="preload" href="fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/montserrat-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css?v={STAMP}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap main-row">
    <a class="brand" href="index.html"><img src="assets/brand/calplug-logo-compact.svg" alt="CalPlug" width="517" height="96"></a>
    <nav class="nav" id="nav" aria-label="Main"><ul>{nav}</ul></nav>
    <div class="header-actions"><button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><i aria-hidden="true"></i></button></div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p class="vision"><a class="vision-mark" href="index.html" aria-label="CalPlug home">{ring("mark")}</a><span>\u201c{e(site['vision'])}\u201d</span></p>
    <div class="foot-row">
      <p class="affil"><a href="https://www.uci.edu/" class="affil-uci"><img src="assets/brand/uci-logo-white.png" alt="UC Irvine" width="266" height="45" loading="lazy"></a><a href="https://www.calit2.uci.edu/" class="affil-logo"><img src="assets/brand/calit2-logo.png" alt="Calit2" width="447" height="447" loading="lazy"></a></p>
      <p class="social">{social}</p>
    </div>
    <p class="legal"><span>{e(", ".join(c["address"])).replace("UC Irvine", "UC&nbsp;Irvine")}</span><span><a href="mailto:{e(c['general']['email'])}">{e(c['general']['email'])}</a></span><span><a href="contact.html">Contact</a></span><span>&copy;&nbsp;{date.today().year} {e(site['full_name'])}</span></p>
  </div>
</footer>
<script src="js/site.js?v={STAMP}" defer></script>
</body>
</html>
"""


def legacy(slug):
    """Original page content copied from the old site (content/legacy), with links and images pointed at this site."""
    f = ROOT / "content" / "legacy" / f"{slug}.html"
    if not f.exists():
        ERRORS.append(f"content/legacy/{slug}.html is missing; run tools/import_pages.py")
        return ""
    html = f.read_text(encoding="utf-8")

    def src(m):
        return f'src="{e(url(m.group(1)))}"'

    def href(m):
        path = m.group(1)
        if path.startswith("/wp-content/"):
            return f'href="{e(url(path))}"'
        key = path.rstrip("/")
        return f'href="{OLD_LINKS[key]}"' if key in OLD_LINKS else f'href="{OLD_SITE}{path}"'

    html = re.sub(r'src="(?:https?://(?:www\.)?calplug\.org)?(/wp-content/uploads/[^"]+)"', src, html)
    html = re.sub(r'href="(?:https?://(?:www\.)?calplug\.org)?(/[^"]*|)"', href, html)
    # line breaks pasted inside links on the old site push the link mark onto its own line
    html = re.sub(r"(<a [^>]*>)\s*(?:<br>\s*)+", r"\1", html)
    html = re.sub(r"\s*(?:<br>\s*)+</a>", "</a>", html)
    return html


def tidy_lists(html):
    """Bullet rules (DESIGN.md section 5) applied to copied pages: a list of one item is a paragraph;
    a list whose every item is "Label: value" is a label / value list."""
    def fix(m):
        items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
        if len(items) == 1:
            return f"<p>{items[0].strip()}</p>"
        pairs = [re.match(r"\s*(?:<h\d>)?\s*<strong>\s*([^<:]+?):\s*</strong>\s*(.*?)\s*(?:</h\d>)?\s*$", i, re.S) for i in items]
        if items and all(pairs):
            return '<dl class="facts wide">' + "".join(f"<dt>{p.group(1).strip()}</dt><dd>{p.group(2).strip()}</dd>" for p in pairs) + "</dl>"
        return m.group(0)
    return re.sub(r"<ul>((?:(?!<ul>).)*?)</ul>", fix, html, flags=re.S)


LEGACY_BACK = {"events-archive.html": ("news.html", "News & Events"), "sim-home.html": ("research.html#labs", "Our labs"),
               "sim-lab.html": ("research.html#labs", "Our labs"), "1-kwh-challenge.html": ("research.html#labs", "Our labs")}


def legacy_page(filename, title, slug, site, description):
    html = tidy_lists(legacy(slug))
    back = LEGACY_BACK.get(filename)
    back = f'<p class="back"><a href="{back[0]}">\u2190 {e(back[1])}</a></p>' if back else ""
    body = head(title) + f'<section class="section"><div class="wrap prose">{html}{back}</div></section>'
    return page(filename, title, description, body, site)


def head(title, extra="", icon=None):
    """Every page starts the same way: title, green line (CSS), then content (DESIGN.md section 2). icon is unused (page icons removed in 0.15)."""
    return f'<div class="page-head"><div class="wrap"><h1>{e(title)}</h1>{extra}</div></div>'


def pub_thumb(p):
    """First page of the PDF when we have it, otherwise the standard tile for the publication type."""
    u = p.get("url") or ""
    f = f"assets/pubs/{hashlib.sha1(u.encode()).hexdigest()[:12]}.jpg"
    if u and (ROOT / f).exists():
        return f'<div class="pubthumb"><img src="{f}" alt="" loading="lazy"></div>'
    return '<div class="pubthumb"><img src="assets/brand/pub-default.svg" alt="" loading="lazy"></div>'


def pub_entry(p, tag=True):
    u = p.get("url")
    title = f'<a href="{e(url(u))}">{e(p["title"])}</a>' if u else e(p["title"])
    kind = "Read"  # one word for every publication link; the PDF or external mark is added by CSS
    link = f'<a href="{e(url(u))}">{kind}</a>' if u else ""
    meta = f'<div class="links">{f"<span class=\"tag\">{PUB_LABELS[p["type"]]}</span>" if tag else ""}{link}</div>'
    return (f'<article class="pub" data-tags="{p["type"]}">{pub_thumb(p)}<div><h3>{title}</h3><p>{e(p["authors"])}</p>'
            f'<p>{e(p.get("venue", ""))}{"" if tag else ", " + str(p["year"])}</p>{meta}</div></article>')


def person(p, sub, tag="h3"):
    pos = f' style="object-position: {e(p["photo_position"])}"' if p.get("photo_position") else ""
    pic = img(p["photo"], f'Portrait of {p["name"]}').replace("<img ", f"<img{pos} ", 1) if p.get("photo") else f'<div class="ph" aria-hidden="true">{e(initials(p["name"]))}</div>'
    # Names are never links: in a grid where only some people have a page, linked names made a patchwork of blue and
    # black. The link gets its own line and says where it goes (DESIGN.md section 4, People).
    link = "".join(f'<p><a href="{e(p[k])}">{label}</a></p>' for k, label in (("linkedin", "LinkedIn"), ("url", "Profile")) if p.get(k))
    return f'<li class="person">{pic}<{tag}>{e(p["name"])}</{tag}>{"".join(f"<p>{e(s)}</p>" for s in sub if s)}{link}</li>'


# ---------- pages ----------

def news_item(ev):
    thumb = f'<div class="thumb">{img(ev.get("image") or NEWS_DEFAULT, "")}</div>'
    return (f'<article class="news">{thumb}<div><div class="when">{e(fmt_date(ev))}</div>'
            f'<h3>{e(ev["title"])}</h3>'
            f'{f"<p>{e(ev.get("summary") or ev.get("theme") or "")}</p>" if ev.get("summary") or ev.get("theme") else ""}'
            f'{links(ev.get("links"))}</div></article>')


def words(text):
    return len((text or "").split())


def limit(text, n, where):
    """Text rules (DESIGN.md section 5): short pieces stay short. Fails the build when a piece is too long."""
    if words(text) > n:
        ERRORS.append(f"{where}: {words(text)} words, the limit is {n}: {text[:60]}...")


def project_page_name(p):
    """A project's page. 'page' in the data names an existing page instead (SIM Home has its lab page), so that
    one subject never has two pages with the same title."""
    return p.get("page") or f"project-{p['id']}.html"


def has_page(p):
    return bool(paras(p) or p.get("page"))


def project_meta(p, themes):
    active = p.get("status") == "active"
    bits = [active_label(p)] if active else []
    bits += [e(years(p))] if years(p) else ([] if active else ["Ongoing"])
    bits += [e(p["sponsor"])] if p.get("sponsor") else []
    return " · ".join(bits)


def theme_names(p, themes):
    return " · ".join(e(themes[t]) for t in p.get("themes", []) if t in themes)


def theme_tags(p, themes):
    return "".join(f'<span class="area">{ring(AREA_ICON.get(t, "plug"))}{e(themes[t])}</span>' for t in p.get("themes", []) if t in themes)


def active_label(p):
    return '<span class="active-dot">Active</span>' if p.get("status") == "active" else ""


def project_card(p, themes, short=False):
    """Card component (DESIGN.md section 4): image, meta line, title, summary, link."""
    href = project_page_name(p)
    title = p.get("short_title") if short and p.get("short_title") else p["title"]
    pic = img(p["image"], p.get("image_alt", "")) if p.get("image") else img(NEWS_DEFAULT, "")
    tags = f'<p class="tags">{theme_tags(p, themes)}</p>' if not short and p.get("themes") else ""
    summary = "" if short else f'<p>{e(p.get("summary", ""))}</p>'  # Home cards show no summary: three lines cut mid-sentence look unfinished
    short_meta = " · ".join(x for x in [active_label(p), e(years(p))] if x) or "Ongoing"
    return (f'<article class="card" data-tags="{" ".join(p.get("themes", []))}"><a class="thumb" href="{href}" tabindex="-1" aria-hidden="true">{pic}</a>'
            f'<div class="card-body"><p class="when">{project_meta(p, themes) if not short else short_meta}</p>'
            f'<h3><a href="{href}">{e(title)}</a></h3>{summary}{tags}'
            f'<div class="links"><a class="more" href="{href}">Details</a></div></div></article>')


def project_row(p, themes):
    """List row (DESIGN.md section 4): years on the left; title, sponsor and area, summary, links."""
    href = project_page_name(p)
    meta = " · ".join(x for x in [e(p.get("sponsor", "")), theme_names(p, themes)] if x)
    ls = list(p.get("links") or [])
    more = f'<a class="more" href="{href}">Details</a>' if has_page(p) else ""
    link_html = '<div class="links">' + "".join(f'<a href="{e(url(l["url"]))}">{e(l["label"])}</a>' for l in ls) + more + "</div>"
    title = f'<a href="{href}">{e(p["title"])}</a>' if has_page(p) else e(p["title"])
    return (f'<article class="item" id="{e(p["id"])}" data-tags="{" ".join(p.get("themes", []))}"><div class="when">{years(p) or "Ongoing"}</div>'
            f'<div><h3>{title}</h3><p class="meta">{meta}</p>'
            f'{f"<p>{e(p["summary"])}</p>" if p.get("summary") else ""}{link_html}</div></article>')


def build_project_page(p, themes, site):
    partners = f'<p class="meta">With {e(", ".join(p["partners"]))}</p>' if p.get("partners") else ""
    pic = f'<figure class="figure">{img(p["image"], p.get("image_alt", ""), eager=True)}</figure>' if p.get("image") else ""
    icon = AREA_ICON.get((p.get("themes") or ["plug-loads"])[0], "plug")
    body = head(p["title"], f'<p class="meta head-meta">{project_meta(p, themes)}{" · " + theme_names(p, themes) if p.get("themes") else ""}</p>', icon=icon) + f"""
<section class="section"><div class="wrap prose">
  {partners}
  {''.join(f"<p>{e(x)}</p>" for x in paras(p))}
  {pic}
  {links(p.get("links"))}
  <p class="back"><a href="research.html">← All research</a></p>
</div></section>
"""
    return page(project_page_name(p), p["title"], (p.get("summary") or p["title"])[:155], body, site, image=p.get("image"))


def build_home(site, projects, pubs, events, people, partners):
    P = projects["projects"]
    active = [p for p in P if p["status"] == "active"]
    news = sorted([x for x in events["events"] if x.get("date")], key=lambda x: x["date"], reverse=True)[:3]
    recent = sorted([x for x in pubs["publications"] if x["type"] != "press"], key=lambda x: x["year"], reverse=True)[:3]
    limit(site["tagline"], 40, "site.json tagline")
    body = f"""
<section class="welcome"><div class="wrap">
  <div class="welcome-text">
    <h1>California Plug Load Research Center</h1>
    <p class="lead">{e(site['tagline'])}</p>
    <p class="textlinks"><a href="about.html">About</a><a href="careers.html">Join us</a><a href="contact.html">Contact</a></p>
  </div>
  <figure>{img('/wp-content/uploads/zotwatt-2.jpg', 'CalPlug student researchers in front of the CalPlug sign', eager=True)}</figure>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Latest news</h2><a class="more" href="news.html">All news and events</a></div>
  <div class="list">{''.join(news_item(x) for x in news)}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Current projects</h2><a class="more" href="research.html">All projects</a></div>
  <div class="grid c4 cards">{''.join(project_card(p, projects['themes'], short=True) for p in active)}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Recent publications</h2><a class="more" href="publications.html">All publications</a></div>
  <div class="list">{''.join(pub_entry(x, tag=False) for x in recent)}</div>
</div></section>
"""
    return page("index.html", "Home", site["tagline"][:155], body, site)


def build_about(site, about):
    out = ""
    for s in about["sections"]:
        inner = f'<blockquote>\u201c{e(s["quote"])}\u201d</blockquote>' if s.get("quote") else ""
        inner += "".join(f"<p>{e(x)}</p>" for x in s.get("paragraphs", []))
        if s.get("bullets"):
            inner += '<ul class="bullets">' + "".join(f"<li>{e(x)}</li>" for x in s["bullets"]) + "</ul>"
        if s.get("logo"):
            inner += f'<img class="about-logo" src="{e(s["logo"]["src"])}" alt="{e(s["logo"]["alt"])}" loading="lazy">'
        if s.get("link"):
            inner += f'<p class="links">{more_link(s["link"]["href"], s["link"]["label"])}</p>'
        out += f'<section class="about-row"><h2>{e(s["title"])}</h2><div>{inner}</div></section>'
    c = site["contact"]
    out += (f'<section class="about-row" id="contact"><h2>Contact</h2><div><p>{"<br>".join(e(a) for a in c["address"])}</p>'
            f'<p>{e(c["general"]["phone"])} · <a href="mailto:{e(c["general"]["email"])}">{e(c["general"]["email"])}</a></p>'
            f'<p class="links">{more_link("contact.html", "Directions and all contacts")}</p></div></section>')
    body = head("About") + f'<div class="wrap about">{out}</div>'
    return page("about.html", "About", about["sections"][0]["paragraphs"][0][:155], body, site)


def labs_section(partners):
    """Our labs: the former Facilities page, now part of Research (DESIGN.md section 2)."""
    pages = {"sim-home": "sim-home.html", "sim-lab": "sim-lab.html", "1-kwh-challenge": "1-kwh-challenge.html"}
    cards = ""
    for f in partners["facilities"]:
        limit(f["blurb"], 60, f"partners.json facility {f['id']} blurb")
        h = pages[f["id"]]
        cards += (f'<article class="card" id="{e(f["id"])}"><a class="thumb" href="{h}" tabindex="-1" aria-hidden="true">{img(f["images"][0], f["name"])}</a>'
                  f'<div class="card-body"><h3><a href="{h}">{e(f["name"])}</a></h3><p>{e(f["blurb"])}</p><div class="links"><a class="more" href="{h}">Read more</a></div></div></article>')
    return f"""
<section class="section" id="labs"><div class="wrap">
  <h2>Our labs</h2>
  <p>{e(partners['facility_intro'])}</p>
  <div class="grid c3 cards">{cards}</div>
  <details class="compare"><summary>Floor plan of the CalPlug space</summary>
    <figure class="plan">{img('/wp-content/uploads/clplg_space.jpg', 'Floor plan of the CalPlug space on the fourth floor of the Calit2 Building')}</figure>
  </details>
</div></section>"""


def build_research(site, projects, partners):
    P, themes = projects["projects"], projects["themes"]
    for p in P:
        need(p, ["id", "title", "status"], "projects.json")
        limit(p.get("summary"), 35, f"projects.json {p['id']} summary")
    limit(projects["intro"], 45, "projects.json intro")
    active = [p for p in P if p["status"] == "active"]
    done = sorted([p for p in P if p["status"] == "completed"], key=lambda p: (p.get("end") or 0, p.get("start") or 0), reverse=True)
    used = [t for t in themes if any(t in p.get("themes", []) for p in P)]
    buttons = '<button aria-pressed="true" data-filter="all">All</button>' + "".join(
        f'<button aria-pressed="false" data-filter="{t}">{ring(AREA_ICON.get(t, "plug"))}{e(themes[t])}</button>' for t in used)
    students = ""
    for g in projects["student_projects"]:
        students += f'<h3>{e(g["group"])}</h3><ul class="plain">' + "".join(
            f'<li><a href="{e(url(i["url"]))}">{e(i["title"])}</a></li>' for i in g["items"]) + "</ul>"
    body = head("Research", f'<p class="intro">{e(projects["intro"])}</p>') + f"""
<section class="section"><div class="wrap" data-filter-scope>
  <div class="filters" role="group" aria-label="Filter by research area">{buttons}</div>
  <p class="visually-hidden" data-count aria-live="polite"></p>
  <div data-group>
    <h2>Current projects</h2>
    <div class="grid c2 cards">{''.join(project_card(p, themes) for p in active)}</div>
  </div>
  <div data-group id="completed" class="group">
    <h2>Completed projects</h2>
    <div class="list">{''.join(project_row(p, themes) for p in done)}</div>
  </div>
</div></section>
{labs_section(partners)}
<section class="section" id="student-projects"><div class="wrap prose">
  <h2>Student projects</h2>
  {students}
</div></section>
"""
    return page("research.html", "Research", "Current and completed research projects at the California Plug Load Research Center.", body, site)


def build_publications(site, pubs):
    labels = PUB_LABELS
    items = pubs["publications"]
    for p in items:
        need(p, ["type", "year", "title", "authors"], "publications.json")
    buttons = '<button aria-pressed="true" data-filter="all">All</button>' + "".join(
        f'<button aria-pressed="false" data-filter="{k}">{v}</button>' for k, v in labels.items())
    out = ""
    for y in sorted({p["year"] for p in items}, reverse=True):
        out += f'<section data-group><h2 class="year">{y}</h2><div class="list">'
        for p in [x for x in items if x["year"] == y]:
            out += pub_entry(p)
        out += "</div></section>"
    other_titles = {"affiliate_faculty_research": "Affiliate faculty research on plug loads", "articles": "Articles",
                    "conference_presentations": "Conference presentations", "case_studies": "Case studies",
                    "engineering_lab_reports": "Engineering lab reports", "patent_disclosures": "Patent disclosures"}
    archive = ""
    for k, t in other_titles.items():
        docs = pubs["other_documents"][k]
        archive += f'<details><summary>{t} ({len(docs)})</summary><ul class="plain">' + "".join(
            f'<li><a href="{e(url(i["url"]))}">{e(i["title"])}</a></li>' for i in docs) + "</ul></details>"
    body = head("Publications") + f"""
<section class="section"><div class="wrap" data-filter-scope>
  <div class="filters" role="group" aria-label="Filter by type">{buttons}</div>
  <p class="visually-hidden" data-count aria-live="polite"></p>
  {out}
</div></section>
<section class="section"><div class="wrap"><h2>Earlier documents</h2>{archive}</div></section>
"""
    return page("publications.html", "Publications", "Publications and technical reports from the California Plug Load Research Center.", body, site)


def build_people(site, people, partners):
    d = people["director"]
    for s in people["students"]:
        need(s, ["name", "program", "level"], "people.json students")

    def lead(p, title):
        bio = p.get("bio", "")
        parts = re.split(r"(?<=[a-z)][a-z)][.!?])\s+(?=[A-Z])", bio)  # not after initials such as "G. P."
        short, rest = " ".join(parts[:2]), " ".join(parts[2:])
        more = f'<details><summary>Full bio</summary><p>{e(rest)}</p></details>' if rest else ""
        return (f'<div class="lead-person">{img(p["photo"], "Portrait of " + p["name"])}<div><h3>{e(p["name"])}</h3>'
                f'<p class="meta">{e(title)}<a href="mailto:{e(p["email"])}">{e(p["email"])}</a></p><p>{e(short)}</p>{more}</div></div>')

    team = "".join(
        f'<div class="card"><div class="card-body"><h4>{e(a["name"])}</h4><p>{e(a["title"])}</p><p class="bottom"><a href="mailto:{e(a["email"])}">{e(a["email"])}</a></p></div></div>'
        for a in people["affiliated_team"])
    grid = lambda items, sub, tag="h3": '<ul class="grid c5">' + "".join(person(x, sub(x), tag) for x in items) + "</ul>"
    boardsub = lambda m: [m.get("role"), m.get("title"), m.get("org")]
    jump = [("team", "Team"), ("students", "Students"), ("faculty", "Faculty"), ("advisory-board", "Advisory Board"),
            ("technology-council", "Council"), ("alumni", "Alumni")]
    body = head("People", '<nav class="filters" aria-label="Sections of this page">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in jump) + "</nav>") + f"""
<section class="section" id="team"><div class="wrap">
  <h2>Team</h2>
  {lead(d, d['title'])}
  {''.join(lead(s, s['title']) for s in people['staff'])}
  <h3 class="sub">Affiliated team members</h3>
  <div class="grid c3 cards">{team}</div>
</div></section>
<section class="section" id="students"><div class="wrap">
  <h2>Student researchers</h2>
  {grid(people['students'], lambda s: [s['program'], s['level']])}
</div></section>
<section class="section" id="faculty"><div class="wrap">
  <h2>Affiliated faculty</h2>
  {grid(people['affiliated_faculty'], lambda f: [f['dept']])}
</div></section>
<section class="section" id="advisory-board"><div class="wrap">
  <h2>Advisory Board</h2>
  {grid(people['advisory_board'], boardsub)}
  <h3 class="sub">Board members emeriti</h3>{grid(people['advisory_board_emeriti'], boardsub, "h4")}
</div></section>
<section class="section" id="technology-council"><div class="wrap">
  <h2>Chief Technology Council</h2>
  {grid(people['technology_council'], boardsub)}
  <h3 class="sub">Council members emeriti</h3>{grid(people['technology_council_emeriti'], boardsub, "h4")}
</div></section>
<section class="section" id="alumni"><div class="wrap">
  <h2>Alumni</h2>
  {grid(people['alumni'], lambda s: [s['program'], s['level']])}
</div></section>
"""
    return page("people.html", "People", "The CalPlug team: director, researchers, students, affiliated faculty and advisory boards.", body, site)


def build_facilities(site, partners):
    """The old Facilities address. The labs are now on the Research page; this page sends visitors there."""
    body = head("Our labs") + """
<section class="section"><div class="wrap"><p>CalPlug's labs are now described on the Research page.</p>
<p><a class="more" href="research.html#labs">Go to Our labs</a></p></div></section>"""
    html = page("facilities.html", "Our labs", "CalPlug labs and demonstration facilities at UC Irvine.", body, site)
    return html.replace('<meta name="robots"', '<meta http-equiv="refresh" content="0; url=research.html#labs">\n<meta name="robots"', 1)


def build_news(site, events):
    evs = events["events"]
    for x in evs:
        need(x, ["id", "title"], "events.json")
        limit(x.get("summary"), 30, f"events.json {x['id']} summary")
    dated = sorted([x for x in evs if x.get("date")], key=lambda x: x["date"], reverse=True)
    undated = [x for x in evs if not x.get("date")]
    body = head("News & Events") + f"""
<section class="section"><div class="wrap"><h2 class="visually-hidden">All news and events</h2><div class="list">{''.join(news_item(x) for x in dated + undated)}</div>
<p class="after-list"><a class="more" href="events-archive.html">Events Archive: full agendas, speakers and recordings</a></p></div></section>
"""
    return page("news.html", "News & Events", "CalPlug workshops and events.", body, site)


def mentor_line(ms):
    pics = "".join(img(m["photo"], "") for m in ms if m.get("photo"))
    names = " and ".join(f'<a href="mailto:{e(m["email"])}">{e(m["name"])}</a>' for m in ms)
    return f'<div class="mentor"><div class="faces">{pics}</div><p>Mentor{"s" if len(ms) > 1 else ""}: {names}</p></div>'


def build_careers(site, c, projects):
    limit(c["intro"], 45, "careers.json intro")
    for p in c["positions"]:
        need(p, ["id", "title", "mentors", "description"], "careers.json positions")
        limit(p["description"], 30, f"careers.json {p['id']} description")
        if len(p.get("tasks", [])) > 3:
            ERRORS.append(f"careers.json {p['id']}: at most 3 tasks")
    pos = ""
    for p in c["positions"]:
        tasks = '<ul class="ticks">' + "".join(f"<li>{e(t)}</li>" for t in p.get("tasks", [])) + "</ul>" if p.get("tasks") else ""
        more = f'<p class="meta">More info: <a href="{e(p["link"]["url"])}">{e(p["link"]["label"])}</a></p>' if p.get("link") else ""
        if p.get("project"):
            pr = projects[p["project"]]
            more = f'<p class="meta">Project: {more_link(project_page_name(pr), pr.get("short_title") or pr["title"])}</p>'
        pos += (f'<article class="card position"><div class="card-body"><p><span class="pill">{e(p["id"])}</span></p><h3>{e(p["title"])}</h3>'
                f'<p>{e(p["description"])}</p>{tasks}{more}{mentor_line(p["mentors"])}</div></article>')
    steps = "".join(f'<li><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></li>' for s in c["apply"])
    lst = lambda xs: '<ul class="ticks">' + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"
    body = head(c["title"], f'<p class="intro">{e(c["intro"])}</p>') + f"""
<section class="section"><div class="wrap">
  <h2 class="visually-hidden">About the program</h2>
  <p class="notice"><strong>Deadline.</strong> {e(c['deadline'])}</p>
  <div class="grid c2 cards">
    <div class="card"><div class="card-body"><h3>What you get</h3>{lst(c['offer'])}</div></div>
    <div class="card"><div class="card-body"><h3>What we ask</h3>{lst(c['ask'])}</div></div>
  </div>
  <p class="meta areas">Calit2 research areas: {" · ".join(f'<span class="nw">{e(a)}</span>' for a in c['areas'])}</p>
</div></section>
<section class="section" id="positions"><div class="wrap">
  <h2>Open positions ({e(c['term'])})</h2>
  <div class="grid c2 cards">{pos}</div>
</div></section>
<section class="section" id="apply"><div class="wrap">
  <h2>How to apply</h2>
  <ol class="steps">{steps}</ol>
</div></section>
"""
    return page("careers.html", "Careers", "Student research opportunities at CalPlug.", body, site)


def logo_tile(x):
    inner = img(x["logo"], x["name"]) if x.get("logo") else f'<span>{e(x["name"])}</span>'
    return f'<li class="logo-tile" title="{e(x["name"])}">{inner}</li>'


def build_support(site, s):
    limit(s["intro"], 45, "support.json intro")
    tiers = s["tiers"]
    code = {t: t[0] for t in tiers}
    rows = [(cat["category"], it[0], it[1]) for cat in s["benefits"] for it in cat["items"]]
    base = [r for r in rows if code[tiers[0]] in r[2]]
    # Every level card has the same shape: a lead-in line, then a bullet list (DESIGN.md section 5)
    base_by_cat = [(cat["category"], sum(1 for it in cat["items"] if code[tiers[0]] in it[1])) for cat in s["benefits"]]
    tier_cards = (f'<div class="card"><div class="card-body"><p class="pill">{e(tiers[0])}</p><p>{len(base)} core benefits:</p>'
                  '<ul class="ticks">' + "".join(f"<li>{e(c)} ({n})</li>" for c, n in base_by_cat if n) + "</ul></div></div>")
    for i, t in enumerate(tiers[1:], 1):
        adds = [r[1] for r in rows if code[t] in r[2] and code[tiers[i - 1]] not in r[2]]
        tier_cards += (f'<div class="card"><div class="card-body"><p class="pill">{e(t)}</p><p>Everything in {e(tiers[i - 1])}, plus:</p>'
                       '<ul class="ticks">' + "".join(f"<li>{e(a)}</li>" for a in adds) + "</ul></div></div>")
    table = ""
    for cat in s["benefits"]:
        table += f'<tr class="cat"><th colspan="{len(tiers) + 1}" scope="colgroup">{e(cat["category"])}</th></tr>'
        for name, has in cat["items"]:
            table += f"<tr><td>{e(name)}</td>" + "".join(
                f'<td class="c">{"<span aria-label=\"Included\">✓</span>" if code[t] in has else "<span class=\"visually-hidden\">Not included</span>"}</td>' for t in tiers) + "</tr>"
    head_row = "<tr><th scope=\"col\">Benefit</th>" + "".join(f'<th scope="col" class="c">{e(t)}</th>' for t in tiers) + "</tr>"
    ways = ""
    for w in s["ways"]:
        act = f'<div class="links">{more_link(w["action"]["url"], w["action"]["label"])}</div>' if w.get("action") else ""
        ways += f'<div class="card" id="{"friends" if w["id"] == "gift" else e(w["id"])}"><div class="card-body"><h3>{e(w["title"])}</h3><p>{e(w["text"])}</p>{act}</div></div>'
    cmail = s["contact"]
    body = head(s["title"], f'<p class="intro">{e(s["intro"])}</p>') + f"""
<section class="section"><div class="wrap">
  <h2>Current members</h2>
  <ul class="logo-grid lg">{''.join(logo_tile(x) for x in s['members'])}</ul>
</div></section>
<section class="section"><div class="wrap">
  <h2>Ways to support</h2>
  <div class="grid c3 cards">{ways}</div>
</div></section>
<section class="section" id="members"><div class="wrap">
  <h2>Membership levels</h2>
  <div class="grid c3 cards tiers">{tier_cards}</div>
  <details class="compare"><summary>Compare all benefits</summary>
    <div class="table-wrap"><table class="benefits"><thead>{head_row}</thead><tbody>{table}</tbody></table></div>
  </details>
  <p class="after-list">To become a member, contact {e(cmail['name'])} at <a href="mailto:{e(cmail['email'])}">{e(cmail['email'])}</a>.</p>
</div></section>
<section class="section" id="affiliates"><div class="wrap">
  <h2>{e(s['affiliates_title'])}</h2>
  <ul class="logo-grid">{''.join(logo_tile(x) for x in s['affiliates'])}</ul>
</div></section>
"""
    return page("support.html", s["title"], "Support CalPlug as a member, with a gift, or with equipment.", body, site)


def build_404(site):
    """Shown by the host for any address that does not exist. Absolute base so it works at any depth."""
    unplugged = ring("mark", "ring unplugged")
    body = f"""
<section class="section notfound"><div class="wrap">
  {unplugged}
  <h1>This page is unplugged.</h1>
  <p class="intro">The address may have changed when the site moved. Try one of these:</p>
  <p class="textlinks"><a href="index.html">Home</a><a href="research.html">Research</a><a href="publications.html">Publications</a><a href="contact.html">Contact</a></p>
</div></section>
"""
    base = f'\n<base href="{e(site["site_url"].rstrip("/"))}/">'
    return page("404.html", "Page not found", "This page does not exist on the CalPlug website.", body, site, extra_head=base)


def contact_card(x):
    """One contact block: short title, then the same rows in the same order (Phone, Email, Web, Contact) so they line up across cards."""
    rows = [("Phone", e(x["phone"]))] if x.get("phone") else []
    if x.get("email"):
        rows.append(("Email", f'<a href="mailto:{e(x["email"])}">{e(x["email"])}</a>'))
    if x.get("url"):
        rows.append(("Web", f'<a href="{e(x["url"])}">{e(x["url"].split("//")[-1].strip("/"))}</a>'))
    if x.get("name"):
        rows.append(("Contact", e(x["name"])))
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    return f'<div class="card"><div class="card-body"><h3>{e(x["title"])}</h3><dl class="facts">{dl}</dl></div></div>'


def build_contact(site):
    c = site["contact"]
    maps = "https://www.google.com/maps/search/?api=1&query=Calit2+Building%2C+University+of+California%2C+Irvine%2C+CA+92697"
    body = head("Contact") + f"""
<section class="section"><div class="wrap">
  <div class="contact-top">
    <div>
      <p>{e(c['location_text'])}</p>
      <p class="address">{'<br>'.join(e(a) for a in c['address'])}</p>
      <p class="links"><a href="{maps}">Open in Google Maps</a></p>
      <p class="meta">Hours: {e(c['hours'])}</p>
    </div>
    <figure class="figure">{img('assets/site/calit2-building.jpg', 'The Calit2 Building at UC Irvine, home of CalPlug', eager=True)}</figure>
  </div>
  <h2 class="visually-hidden">Contacts</h2>
  <div class="grid c3 cards contacts">{contact_card(c['general'])}{contact_card(c['collaborations'])}{contact_card(c['calit2'])}</div>
</div></section>
"""
    return page("contact.html", "Contact", "How to reach the California Plug Load Research Center.", body, site)


def main():
    site, projects, pubs = load("site"), load("projects"), load("publications")
    people, events, partners = load("people"), load("events"), load("partners")
    pages = {
        "index.html": build_home(site, projects, pubs, events, people, partners),
        "about.html": build_about(site, load("about")),
        "research.html": build_research(site, projects, partners),
        "publications.html": build_publications(site, pubs),
        "people.html": build_people(site, people, partners),
        "facilities.html": build_facilities(site, partners),
        "news.html": build_news(site, events),
        "sim-home.html": legacy_page("sim-home.html", "SIM Home", "sim-home", site, "The Simulation, Integration, and Management (SIM) Home at CalPlug."),
        "sim-lab.html": legacy_page("sim-lab.html", "SIM Lab", "sim-lab", site, "CalPlug SIM Lab testing and demonstration labs."),
        "1-kwh-challenge.html": legacy_page("1-kwh-challenge.html", "1 kWh Challenge", "1-kwh-challenge", site, "The One Kilowatt-hour Challenge outreach program."),
        "events-archive.html": legacy_page("events-archive.html", "Events Archive", "events-archive", site, "Past CalPlug workshops with agendas, speakers and recordings."),
        "careers.html": build_careers(site, load("careers"), {p["id"]: p for p in projects["projects"]}),
        "support.html": build_support(site, load("support")),
        "contact.html": build_contact(site),
        "404.html": build_404(site),
    }
    for p in projects["projects"]:
        if paras(p):
            SECTION[project_page_name(p)] = "research.html"
            pages[project_page_name(p)] = build_project_page(p, projects["themes"], site)
    if ERRORS:
        print("Build stopped. Fix these data problems:\n  " + "\n  ".join(ERRORS))
        sys.exit(1)
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for name, html in pages.items():
        (DIST / name).write_text(html, encoding="utf-8")
    shutil.copytree(SRC / "css", DIST / "css")
    shutil.copytree(SRC / "js", DIST / "js")
    shutil.copytree(SRC / "fonts", DIST / "fonts")
    if ASSETS.exists():
        shutil.copytree(ASSETS, DIST / "assets")
    if (ROOT / "wp-content").exists():  # documents from the old site, served at their old address
        shutil.copytree(ROOT / "wp-content", DIST / "wp-content")
    (DIST / ".nojekyll").write_text("")
    print(f"Built {len(pages)} pages into dist/")
    if MISSING:
        print(f"Note: {len(set(MISSING))} files still point to the old site (run the import workflow): " + ", ".join(sorted(set(MISSING))[:5]) + (" ..." if len(set(MISSING)) > 5 else ""))


if __name__ == "__main__":
    main()
