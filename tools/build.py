#!/usr/bin/env python3
"""Build the CalPlug site: data/*.json + templates below -> dist/*.html.

Usage: python tools/build.py
Standard library only. Fails with a clear message when data is missing a required field.
"""
import hashlib
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
# Version stamp so browsers fetch new CSS/JS after a change (DESIGN.md: cache and versions)
STAMP = hashlib.sha1(b"".join(f.read_bytes() for f in sorted((SRC).rglob("*.*")))).hexdigest()[:8]

NEWS_DEFAULT = "assets/brand/news-default.svg"
PUB_LABELS = {"journal": "Journal", "conference": "Conference", "report": "Report", "press": "In the press"}

# Navigation follows the structure of the previous calplug.org. (href, label, [sub-items])
NAV = [
    ("index.html", "Home", []),
    ("about.html", "About", []),
    ("people.html", "People", [("people.html#team", "CalPlug Team"), ("people.html#affiliated-faculty", "Affiliated Faculty Leadership"),
                                ("people.html#advisory-board", "Advisory Board"), ("people.html#technology-council", "Chief Technology Council")]),
    ("facilities.html", "Facilities", [("sim-home.html", "SIM Home"), ("1-kwh-challenge.html", "1 kWh Challenge"), ("sim-lab.html", "SIM Lab")]),
    ("research.html", "Projects & Publications", [("research.html", "Projects"), ("publications.html", "Publications")]),
    ("support.html", "Support & Memberships", [("support.html#friends", "Support"), ("support.html#members", "Become a Member"),
                                                ("support.html#affiliates", "Members & Affiliates")]),
    ("news.html", "Events", [("news.html", "News & Events"), ("events-archive.html", "Events Archive")]),
    ("careers.html", "CalPlug Careers", []),
    ("contact.html", "Contact", []),
]
# which top-level item is "current" for each page
SECTION = {"publications.html": "research.html", "sim-home.html": "facilities.html", "sim-lab.html": "facilities.html",
           "1-kwh-challenge.html": "facilities.html", "events-archive.html": "news.html"}
OLD_LINKS = {"/sim-home": "sim-home.html", "/sim-lab": "sim-lab.html", "/1-kwh-challenge": "1-kwh-challenge.html",
             "/friends": "support.html#friends", "/members-2": "support.html#members", "/support": "support.html",
             "/affiliations": "support.html#affiliates", "/about/careers": "careers.html", "/about/contact": "contact.html",
             "/eventsarchive": "events-archive.html", "/projects": "research.html", "/publications": "publications.html",
             "/about/team": "people.html", "/about": "about.html", "/facilities": "facilities.html", "/": "index.html", "": "index.html"}


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def need(item, fields, where):
    for f in fields:
        if not item.get(f):
            ERRORS.append(f"{where}: '{item.get('id') or item.get('name') or item.get('title')}' is missing '{f}'")


def url(path):
    """Images imported into assets/legacy are served locally; everything else stays on the old site."""
    if not path:
        return ""
    if path.startswith("/wp-content/uploads/"):
        local = ASSETS / "legacy" / path[len("/wp-content/uploads/"):]
        return f"assets/legacy/{path[len('/wp-content/uploads/'):]}" if local.exists() else OLD_SITE + path
    return path


def img(path, alt="", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{e(url(path))}" alt="{e(alt)}" loading="lazy"{c}>'


def links(items):
    if not items:
        return ""
    return '<div class="links">' + "".join(
        f'<a href="{e(url(l["url"]))}">{e(l["label"])}</a>' for l in items) + "</div>"


def paras(p):
    """Original description as a list of paragraphs (data may hold a string or a list)."""
    d = p.get("description") or []
    return [d] if isinstance(d, str) else d


def first_sentence(p):
    """First sentence of the original description, word for word."""
    ps = paras(p)
    return re.split(r"(?<=[.!?])\s+(?=[A-Z\u201c\"])", ps[0], maxsplit=1)[0] if ps else ""


def years(p):
    s, en = p.get("start"), p.get("end")
    if not s:
        return ""
    return str(s) if s == en or not en else f"{s}–{en}"


def fmt_date(ev):
    if not ev.get("date"):
        return ""
    d = date.fromisoformat(ev["date"])
    out = f"{d.strftime('%b')} {d.day}, {d.year}"
    if ev.get("end_date"):
        d2 = date.fromisoformat(ev["end_date"])
        out = f"{d.strftime('%b')} {d.day}–{d2.day}, {d.year}"
    return out


def initials(name):
    parts = re.sub(r"\(.*?\)|,.*", "", name).split()
    return (parts[0][0] + parts[-1][0]).upper() if parts else ""


def page(filename, title, description, body, site):
    cur = SECTION.get(filename, filename)
    nav = ""
    for h, label, subs in NAV:
        sub = ('<ul class="sub">' + "".join(f'<li><a href="{sh}">{e(sl)}</a></li>' for sh, sl in subs) + "</ul>") if subs else ""
        nav += (f'<li{" class=\"has-sub\"" if subs else ""}><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{e(label)}</a>{sub}</li>')
    c = site["contact"]
    full_title = "CalPlug – California Plug Load Research Center" if filename == "index.html" else f"{title} – CalPlug"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/brand/calplug-mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/site.css?v={STAMP}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap top">
    <a class="brand" href="index.html"><img src="{e(url('/wp-content/uploads/calpluglogo-small.png'))}" alt="CalPlug, California Plug Load Research Center, University of California, Irvine" width="600" height="166"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
  <nav class="nav" id="nav" aria-label="Main"><div class="wrap"><ul>{nav}</ul></div></nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <h2>{e(site['full_name'])}</h2>
        <p>{'<br>'.join(e(a) for a in c['address'])}</p>
        <p>{e(c['general']['phone'])}<br><a href="mailto:{e(c['general']['email'])}">{e(c['general']['email'])}</a></p>
      </div>
      <div>
        <h2>Site</h2>
        <ul>{''.join(f'<li><a href="{h}">{e(lbl)}</a></li>' for h, lbl, _ in NAV[1:])}</ul>
      </div>
      <div>
        <h2>Connect</h2>
        <ul>
          <li><a href="{e(site['social']['linkedin'])}">LinkedIn</a></li>
          <li><a href="{e(site['social']['facebook'])}">Facebook</a></li>
          <li><a href="https://www.calit2.uci.edu/">Calit2</a></li>
          <li><a href="https://www.uci.edu/">UC Irvine</a></li>
        </ul>
      </div>
    </div>
    <p class="legal">&copy; {date.today().year} {e(site['full_name'])}, {e(site['institution'])}.</p>
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
            return f'href="{OLD_SITE}{path}"'
        key = path.rstrip("/")
        return f'href="{OLD_LINKS[key]}"' if key in OLD_LINKS else f'href="{OLD_SITE}{path}"'

    html = re.sub(r'src="(?:https?://(?:www\.)?calplug\.org)?(/wp-content/uploads/[^"]+)"', src, html)
    html = re.sub(r'href="(?:https?://(?:www\.)?calplug\.org)?(/[^"]*|)"', href, html)
    return html


def legacy_page(filename, title, slug, site, description):
    body = head(title, "") + f'<section class="section"><div class="wrap prose">{legacy(slug)}</div></section>'
    return page(filename, title, description, body, site)


def head(title, lead):
    return f'<div class="page-head"><div class="wrap"><h1>{e(title)}</h1>{f"<p class=\"lead\">{e(lead)}</p>" if lead else ""}</div></div>'


def cta(title, text, label="Partner with us", href="partner.html"):
    return (f'<section class="cta"><div class="wrap"><div><h2>{e(title)}</h2><p>{e(text)}</p></div>'
            f'<a class="btn" href="{href}">{e(label)}</a></div></section>')


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
    kind = "PDF" if (u or "").split("?")[0].lower().endswith(".pdf") else "View"
    link = f'<a href="{e(url(u))}">{kind}</a>' if u else ""
    meta = f'<div class="links">{f"<span class=\"tag\">{PUB_LABELS[p["type"]]}</span>" if tag else ""}{link}</div>'
    return (f'<article class="pub" data-tags="{p["type"]}">{pub_thumb(p)}<div><h3>{title}</h3><p>{e(p["authors"])}</p>'
            f'<p>{e(p.get("venue", ""))}{"" if tag else ", " + str(p["year"])}</p>{meta}</div></article>')


def project_card(p):
    meta = " · ".join(x for x in [years(p), p.get("sponsor")] if x)
    thumb = f'<div class="thumb">{img(p["image"], p.get("image_alt", ""))}</div>' if p.get("image") else ""
    return (f'<article class="card reveal" id="{e(p["id"])}">{thumb}'
            f'{f"<div class=\"meta\">{e(meta)}</div>" if meta else ""}'
            f'<h3>{e(p["title"])}</h3>{"".join(f"<p>{e(x)}</p>" for x in paras(p))}{links(p.get("links"))}</article>')


def event_row(ev):
    when = fmt_date(ev)
    bits = " · ".join(x for x in [ev.get("location"), "Online" if ev.get("format") == "online" else ""] if x)
    return (f'<article class="row reveal"><div class="when">{e(when)}</div><div><h3>{e(ev["title"])}</h3>'
            f'{f"<p>{e(ev["theme"])}</p>" if ev.get("theme") else ""}'
            f'{f"<p>{e(ev["summary"])}</p>" if ev.get("summary") else ""}'
            f'{f"<p class=\"meta\">{e(bits)}</p>" if bits else ""}</div>{links(ev.get("links"))}</article>')


def person(p, sub):
    pic = img(p["photo"], f'Portrait of {p["name"]}') if p.get("photo") else f'<div class="ph" aria-hidden="true">{e(initials(p["name"]))}</div>'
    name = e(p["name"])
    link = p.get("linkedin") or p.get("url")
    if link:
        name = f'<a href="{e(link)}">{name}</a>'
    return f'<li class="person reveal">{pic}<h3>{name}</h3>{"".join(f"<p>{e(s)}</p>" for s in sub if s)}</li>'


def board(members):
    return '<ul class="grid c5">' + "".join(
        person(m, [m.get("role"), m.get("title"), m.get("org")]) for m in members) + "</ul>"


# ---------- pages ----------

def news_item(ev):
    thumb = f'<div class="thumb">{img(ev.get("image") or NEWS_DEFAULT, "")}</div>'
    return (f'<article class="news reveal">{thumb}<div><div class="when">{e(fmt_date(ev))}</div>'
            f'<h3>{e(ev["title"])}</h3>'
            f'{f"<p>{e(ev.get("summary") or ev.get("theme") or "")}</p>" if ev.get("summary") or ev.get("theme") else ""}'
            f'{links(ev.get("links"))}</div></article>')


def build_home(site, projects, pubs, events, people, partners):
    P = projects["projects"]
    active = [p for p in P if p["status"] == "active"]
    news = sorted([x for x in events["events"] if x.get("date")], key=lambda x: x["date"], reverse=True)[:4]
    recent = sorted([x for x in pubs["publications"] if x["type"] != "press"], key=lambda x: x["year"], reverse=True)[:4]
    proj = "".join(
        f'<article class="row reveal"><div class="when">{years(p) or "Ongoing"}</div><div><h3>{e(p["title"])}</h3>'
        f'<p>{e(first_sentence(p))}</p>{f"<p class=\"meta\">{e(p["sponsor"])}</p>" if p.get("sponsor") else ""}</div></article>'
        for p in active)
    pub = "".join(pub_entry(x, tag=False) for x in recent)
    body = f"""
<section class="welcome"><div class="wrap">
  <div>
    <h1>California Plug Load Research Center</h1>
    <p class="lead">The California Plug Load Research Center (CalPlug) is the Leading Enabler for Energy Efficiency Solutions in the Use and Design of Appliances and Consumer Products.</p>
    <p>Our mission: {e(site['mission'][0].lower() + site['mission'][1:])}</p>
    <p>Interested in working with us? See <a href="careers.html">student research opportunities</a> or <a href="support.html">support and memberships</a>.</p>
    <p><a href="about.html"><strong>About CalPlug \u2192</strong></a></p>
  </div>
  <figure>{img('/wp-content/uploads/zotwatt-2.jpg', 'CalPlug student researchers in front of the CalPlug sign')}</figure>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Latest news</h2><a class="more" href="news.html">See all news and events \u2192</a></div>
  <div class="newslist">{''.join(news_item(x) for x in news)}</div>
</div></section>
<section class="section tint"><div class="wrap">
  <div class="section-head"><h2>Current projects</h2><a class="more" href="research.html">All {len(P)} projects \u2192</a></div>
  <div class="rows">{proj}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Recent publications</h2><a class="more" href="publications.html">All publications \u2192</a></div>
  <div class="read">{pub}</div>
</div></section>
"""
    return page("index.html", "Home", site["about"][:155], body, site)


def build_about(site, about):
    out = ""
    for s in about["sections"]:
        inner = f'<blockquote>\u201c{e(s["quote"])}\u201d</blockquote>' if s.get("quote") else ""
        inner += "".join(f"<p>{e(x)}</p>" for x in s.get("paragraphs", []))
        if s.get("bullets"):
            inner += '<ul class="bullets">' + "".join(f"<li>{e(x)}</li>" for x in s["bullets"]) + "</ul>"
        if s.get("link"):
            inner += f'<p><a href="{s["link"]["href"]}">{e(s["link"]["label"])} \u2192</a></p>'
        out += f'<section class="about-row"><h2>{e(s["title"])}</h2><div>{inner}</div></section>'
    body = (f'<div class="page-head"><div class="wrap"><h1>About</h1>'
            f'{img("/wp-content/uploads/calpluglogo-small.png", "CalPlug, California Plug Load Research Center, University of California, Irvine", "about-logo")}'
            f'</div></div><div class="wrap about">{out}</div>')
    return page("about.html", "About", about["sections"][0]["paragraphs"][0][:155], body, site)


def build_research(site, projects):
    P, themes = projects["projects"], projects["themes"]
    for p in P:
        need(p, ["id", "title", "status", "themes"], "projects.json")
    active = [p for p in P if p["status"] == "active"]
    done = sorted([p for p in P if p["status"] == "completed"], key=lambda p: (p.get("end") or 0, p.get("start") or 0), reverse=True)
    buttons = '<button aria-pressed="true" data-filter="all">All</button>' + "".join(
        f'<button aria-pressed="false" data-filter="{k}">{e(v)}</button>' for k, v in themes.items())
    rows = ""
    for p in done:
        full = "".join(f"<p>{e(x)}</p>" for x in paras(p)[0:])
        more = f'<details><summary>Full description</summary>{full}</details>' if paras(p) else ""
        rows += (f'<article class="row" id="{e(p["id"])}" data-tags="{" ".join(p["themes"])}"><div class="when">{years(p)}</div>'
                 f'<div><h3>{e(p["title"])}</h3>{f"<p class=\"meta\">{e(p["sponsor"])}</p>" if p.get("sponsor") else ""}'
                 f'{f"<p>{e(first_sentence(p))}</p>" if paras(p) else ""}{more}</div>{links(p.get("links"))}</article>')
    students = ""
    for g in projects["student_projects"]:
        students += f'<div class="card reveal"><h3>{e(g["group"])}</h3><ul class="plain">' + "".join(
            f'<li><a href="{e(url(i["url"]))}">{e(i["title"])}</a></li>' for i in g["items"]) + "</ul></div>"
    body = head("Research", "CalPlug studies how plug loads, buildings and the grid use energy, and how technology, behavior and policy can reduce it.") + f"""
<section class="section"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Active</div><h2>Current projects</h2></div></div>
  <div class="grid c2">{''.join(project_card(p) for p in active)}</div>
</div></section>
<section class="section tint" id="projects"><div class="wrap" data-filter-scope>
  <div class="section-head"><div><div class="eyebrow">Completed</div><h2>{len(done)} completed projects</h2></div><span class="meta" data-count aria-live="polite"></span></div>
  <div class="filters" role="group" aria-label="Filter by research area">{buttons}</div>
  <div class="rows">{rows}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Students</div><h2>Student projects</h2></div></div>
  <div class="grid c3">{students}</div>
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
        out += f'<section data-group><h2 class="year">{y}</h2>'
        for p in [x for x in items if x["year"] == y]:
            out += pub_entry(p)
        out += "</section>"
    other_titles = {"affiliate_faculty_research": "Affiliate faculty research on plug loads", "articles": "Articles",
                    "conference_presentations": "Conference presentations", "case_studies": "Case studies",
                    "engineering_lab_reports": "Engineering lab reports", "patent_disclosures": "Patent disclosures"}
    archive = ""
    for k, t in other_titles.items():
        archive += f'<h3 class="sub">{t}</h3><ul class="plain">' + "".join(
            f'<li><a href="{e(url(i["url"]))}">{e(i["title"])}</a></li>' for i in pubs["other_documents"][k]) + "</ul>"
    body = head("Publications", "Journal articles, conference papers, technical reports and press coverage from CalPlug researchers.") + f"""
<section class="section"><div class="wrap read" data-filter-scope>
  <div class="filters" role="group" aria-label="Filter by type">{buttons}</div>
  <span class="meta" data-count aria-live="polite"></span>
  {out}
</div></section>
<section class="section tint"><div class="wrap read"><div class="eyebrow">Archive</div><h2>Earlier documents</h2>{archive}</div></section>
"""
    return page("publications.html", "Publications", "Publications and technical reports from the California Plug Load Research Center.", body, site)


def build_people(site, people, partners):
    d = people["director"]
    for s in people["students"]:
        need(s, ["name", "program", "level"], "people.json students")
    staff = "".join(
        f'<div class="lead-person reveal">{img(s["photo"], "Portrait of " + s["name"])}<div><h3>{e(s["name"])}</h3>'
        f'<p class="meta">{e(s["title"])} · <a href="mailto:{e(s["email"])}">{e(s["email"])}</a></p><p>{e(s.get("bio", ""))}</p></div></div>'
        for s in people["staff"])
    team = "".join(
        f'<div class="card reveal"><h3>{e(a["name"])}</h3><p>{e(a["title"])}</p><div class="links"><a href="mailto:{e(a["email"])}">{e(a["email"])}</a></div></div>'
        for a in people["affiliated_team"])
    body = head("People", "Faculty, researchers, students and advisors behind CalPlug.") + f"""
<section class="section" id="team"><div class="wrap">
  <div class="eyebrow">Director</div>
  <div class="lead-person reveal">{img(d['photo'], 'Portrait of ' + d['name'])}<div><h2>{e(d['name'])}</h2>
    <p class="meta">{e(d['title'])} · <a href="mailto:{e(d['email'])}">{e(d['email'])}</a></p><p>{e(d['bio'])}</p></div></div>
  <div class="eyebrow">Research staff</div>{staff}
  <h2 class="sub">Affiliated team</h2><div class="grid c3">{team}</div>
</div></section>
<section class="section tint"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Students</div><h2>Student researchers</h2></div></div>
  <ul class="grid c5">{''.join(person(s, [s['program'], s['level']]) for s in people['students'])}</ul>
  <h3 class="sub">Alumni</h3>
  <ul class="grid c5">{''.join(person(s, [s['program'], s['level']]) for s in people['alumni'])}</ul>
</div></section>
<section class="section" id="affiliated-faculty"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">UC Irvine</div><h2>Affiliated Faculty Leadership</h2></div></div>
  <ul class="grid c5">{''.join(person(f, [f['dept']]) for f in people['affiliated_faculty'])}</ul>
</div></section>
<section class="section tint" id="advisory-board"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Guidance</div><h2>Advisory Board</h2></div></div>
  {board(people['advisory_board'])}
  <h3 class="sub">Board members emeriti</h3>{board(people['advisory_board_emeriti'])}
</div></section>
<section class="section" id="technology-council"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Guidance</div><h2>Chief Technology Council</h2></div></div>
  {board(people['technology_council'])}
  <h3 class="sub">Council members emeriti</h3>{board(people['technology_council_emeriti'])}
</div></section>
"""
    return page("people.html", "People", "The CalPlug team: director, researchers, students, affiliated faculty and advisory boards.", body, site)


def build_facilities(site, partners):
    pages = {"sim-home": "sim-home.html", "sim-lab": "sim-lab.html", "1-kwh-challenge": "1-kwh-challenge.html"}
    cards = ""
    for f in partners["facilities"]:
        cards += (f'<a class="card" href="{pages[f["id"]]}" id="{e(f["id"])}"><div class="thumb">{img(f["images"][0], f["name"])}</div>'
                  f'<h3>{e(f["name"])}</h3><p>{e(f["blurb"])}</p><div class="links"><span>Read more \u2192</span></div></a>')
    body = head("Facilities", "") + f"""
<section class="section"><div class="wrap">
  <p class="lead">{e(partners['facility_intro'])}</p>
  <figure class="plan">{img('/wp-content/uploads/clplg_space.jpg', 'Floor plan of the CalPlug space on the fourth floor of the Calit2 Building')}</figure>
  <div class="grid c3">{cards}</div>
</div></section>
"""
    return page("facilities.html", "Facilities", "CalPlug labs and demonstration facilities at UC Irvine.", body, site)


def build_news(site, events):
    evs = events["events"]
    for x in evs:
        need(x, ["id", "title"], "events.json")
    dated = sorted([x for x in evs if x.get("date")], key=lambda x: x["date"], reverse=True)
    undated = [x for x in evs if not x.get("date")]
    body = head("News & Events", "Workshops, talks and announcements from CalPlug.") + f"""
<section class="section"><div class="wrap"><div class="newslist">{''.join(news_item(x) for x in dated + undated)}</div>
<p style="margin-top:var(--s-32)"><a href="events-archive.html"><strong>Events archive: full agendas, speakers and recordings \u2192</strong></a></p></div></section>
"""
    return page("news.html", "News & Events", "CalPlug workshops and events.", body, site)


def build_support(site, partners):
    chips = lambda xs: "".join(f'<span class="tag">{e(x)}</span>' for x in xs)
    body = head("Support & Memberships", "") + f"""
<section class="section"><div class="wrap prose">{legacy('support')}</div></section>
<section class="section tint" id="friends"><div class="wrap prose"><h2>Support</h2>{legacy('friends')}</div></section>
<section class="section" id="members"><div class="wrap prose"><h2>Become A Member</h2>{legacy('members')}</div></section>
<section class="section tint" id="affiliates"><div class="wrap">
  <h2>Members &amp; Affiliates</h2>
  <h3 class="sub">Current CalPlug Members</h3><div class="chips">{chips(partners['members'])}</div>
  <h3 class="sub">Current affiliates</h3><div class="chips">{chips(partners['affiliates'])}</div>
  <div class="logos" style="margin-top:var(--s-32)">{''.join(img(l['src'], l['name']) for l in partners.get('logos', []))}</div>
</div></section>
"""
    return page("support.html", "Support & Memberships", "Support CalPlug as a friend or corporate member.", body, site)


def build_contact(site):
    c = site["contact"]
    body = head("Contact", "") + f"""
<section class="section"><div class="wrap">
  <p class="read">CalPlug is located on the main campus of UC Irvine, in the Calit2 building, at the intersection of East Peltason Road and Los Trancos Drive, adjacent to the University Club. The CalPlug main office is located on the fourth floor in suite 4300. CalIt2 administrative offices are in suite 4100.</p>
  <div class="grid c2" style="margin-top:var(--s-32)">
    <div class="card"><h3>Location</h3><p>{'<br>'.join(e(a) for a in c['address'])}</p><p>Our hours: {e(c['hours'])}</p></div>
    <div class="card"><h3>General Information, Directions &amp; Parking</h3><p>Phone: {e(c['general']['phone'])}</p><div class="links"><a href="mailto:{e(c['general']['email'])}">{e(c['general']['email'])}</a></div></div>
    <div class="card"><h3>CalPlug Collaborations</h3><p>Phone: {e(c['collaborations']['phone'])}</p><div class="links"><a href="mailto:{e(c['collaborations']['email'])}">{e(c['collaborations']['email'])}</a></div></div>
    <div class="card"><h3>General / Calit2 Information</h3><p>Phone: {e(c['calit2']['phone'])}</p><div class="links"><a href="mailto:{e(c['calit2']['email'])}">{e(c['calit2']['email'])}</a><a href="{e(c['calit2']['url'])}">www.calit2.uci.edu</a></div></div>
  </div>
</div></section>
"""
    return page("contact.html", "Contact", "How to reach the California Plug Load Research Center.", body, site)


def main():
    site, projects, pubs = load("site"), load("projects"), load("publications")
    people, events, partners = load("people"), load("events"), load("partners")
    pages = {
        "index.html": build_home(site, projects, pubs, events, people, partners),
        "about.html": build_about(site, load("about")),
        "research.html": build_research(site, projects),
        "publications.html": build_publications(site, pubs),
        "people.html": build_people(site, people, partners),
        "facilities.html": build_facilities(site, partners),
        "news.html": build_news(site, events),
        "sim-home.html": legacy_page("sim-home.html", "SIM Home", "sim-home", site, "The Simulation, Integration, and Management (SIM) Home at CalPlug."),
        "sim-lab.html": legacy_page("sim-lab.html", "SIM Lab", "sim-lab", site, "CalPlug SIM Lab testing and demonstration labs."),
        "1-kwh-challenge.html": legacy_page("1-kwh-challenge.html", "1 kWh Challenge", "1-kwh-challenge", site, "The One Kilowatt-hour Challenge outreach program."),
        "events-archive.html": legacy_page("events-archive.html", "Events Archive", "events-archive", site, "Past CalPlug workshops with agendas, speakers and recordings."),
        "careers.html": legacy_page("careers.html", "CalPlug Careers", "careers", site, "Student research opportunities at CalPlug."),
        "support.html": build_support(site, partners),
        "contact.html": build_contact(site),
    }
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
    if ASSETS.exists():
        shutil.copytree(ASSETS, DIST / "assets")
    (DIST / ".nojekyll").write_text("")
    print(f"Built {len(pages)} pages into dist/")


if __name__ == "__main__":
    main()
