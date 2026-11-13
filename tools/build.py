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

# One row, ten items, no drop-down menus (DESIGN.md section 2). Sub-pages are reached from their parent page.
NAV = [
    ("index.html", "Home"), ("about.html", "About"), ("people.html", "People"), ("research.html", "Projects"),
    ("publications.html", "Publications"), ("facilities.html", "Facilities"), ("news.html", "News & Events"),
    ("careers.html", "Careers"), ("support.html", "Support"), ("contact.html", "Contact"),
]
# which top-level item is "current" for each page
SECTION = {"sim-home.html": "facilities.html", "sim-lab.html": "facilities.html",
           "1-kwh-challenge.html": "facilities.html", "events-archive.html": "news.html"}
OLD_LINKS = {"/sim-home": "sim-home.html", "/sim-lab": "sim-lab.html", "/1-kwh-challenge": "1-kwh-challenge.html",
             "/friends": "support.html#friends", "/members-2": "support.html#members", "/support": "support.html",
             "/affiliations": "support.html#affiliates", "/about/careers": "careers.html", "/about/contact": "contact.html",
             "/eventsarchive": "events-archive.html", "/projects": "research.html", "/publications": "publications.html",
             "/about/team": "people.html#team", "/about": "about.html", "/facilities": "facilities.html", "/": "index.html", "": "index.html"}


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


NOBREAK = ["UC Irvine", "Calit2 Building", "CalPlug/ITAC", "Calit2 UCI Division", "Dr. Shuoyu (Arnold) Wang", "Dr. G. P. Li"]


def nobreak(html):
    """Keep names and fixed terms on one line (DESIGN.md section 3, Line breaks)."""
    for term in NOBREAK:
        html = html.replace(term, term.replace(" ", "\u00a0"))
    return html


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


def page(filename, title, description, body, site):
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
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/brand/calplug-logo-compact.png" alt="CalPlug" width="517" height="96"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-row">
      <p class="affil"><a href="https://www.uci.edu/">UC&nbsp;Irvine</a><span aria-hidden="true">\u00b7</span><a href="https://www.calit2.uci.edu/">Calit2</a></p>
      <p class="social">{social}</p>
    </div>
    <p class="legal">{e(", ".join(c["address"])).replace("UC Irvine", "UC&nbsp;Irvine")} \u00b7 <a href="mailto:{e(c['general']['email'])}">{e(c['general']['email'])}</a> \u00b7 &copy;&nbsp;{date.today().year} {e(site['full_name'])}</p>
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
    body = head(title) + f'<section class="section"><div class="wrap prose">{legacy(slug)}</div></section>'
    return page(filename, title, description, body, site)


def head(title, extra=""):
    """Every page starts the same way: title, green line (CSS), then content (DESIGN.md section 2)."""
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
    kind = "PDF" if (u or "").split("?")[0].lower().endswith(".pdf") else "View"
    link = f'<a href="{e(url(u))}">{kind}</a>' if u else ""
    meta = f'<div class="links">{f"<span class=\"tag\">{PUB_LABELS[p["type"]]}</span>" if tag else ""}{link}</div>'
    return (f'<article class="pub" data-tags="{p["type"]}">{pub_thumb(p)}<div><h3>{title}</h3><p>{e(p["authors"])}</p>'
            f'<p>{e(p.get("venue", ""))}{"" if tag else ", " + str(p["year"])}</p>{meta}</div></article>')


def person(p, sub):
    pos = f' style="object-position: {e(p["photo_position"])}"' if p.get("photo_position") else ""
    pic = img(p["photo"], f'Portrait of {p["name"]}').replace("<img ", f"<img{pos} ", 1) if p.get("photo") else f'<div class="ph" aria-hidden="true">{e(initials(p["name"]))}</div>'
    name = e(p["name"])
    link = p.get("linkedin") or p.get("url")
    if link:
        name = f'<a href="{e(link)}">{name}</a>'
    return f'<li class="person">{pic}<h3>{name}</h3>{"".join(f"<p>{e(s)}</p>" for s in sub if s)}</li>'


# ---------- pages ----------

def news_item(ev):
    thumb = f'<div class="thumb">{img(ev.get("image") or NEWS_DEFAULT, "")}</div>'
    return (f'<article class="news">{thumb}<div><div class="when">{e(fmt_date(ev))}</div>'
            f'<h3>{e(ev["title"])}</h3>'
            f'{f"<p>{e(ev.get("summary") or ev.get("theme") or "")}</p>" if ev.get("summary") or ev.get("theme") else ""}'
            f'{links(ev.get("links"))}</div></article>')


def project_row(p, mode="list"):
    """One format for every project (DESIGN.md section 3, One list format).
    mode "title": years, title, sponsor (home page). "list": plus first sentence and the full text on demand.
    "full": all original paragraphs and the image (current projects on the Projects page)."""
    sponsor = f'<p class="meta">{e(p["sponsor"])}</p>' if p.get("sponsor") else ""
    pic = f'<figure class="figure">{img(p["image"], p.get("image_alt", ""))}</figure>' if p.get("image") else ""
    body = ""
    if mode == "full":
        body = "".join(f"<p>{e(x)}</p>" for x in paras(p)) + pic + links(p.get("links"))
    elif mode == "list":
        more = (f'<details><summary>Full description</summary>{"".join(f"<p>{e(x)}</p>" for x in paras(p))}{pic}</details>'
                if paras(p) else "")
        body = (f"<p>{e(first_sentence(p))}</p>" if paras(p) else "") + more + links(p.get("links"))
    return (f'<article class="item{" full" if mode == "full" else ""}" id="{e(p["id"])}"><div class="when">{years(p) or "Ongoing"}</div>'
            f'<div><h3>{e(p["title"])}</h3>{sponsor}{body}</div></article>')


def build_home(site, projects, pubs, events, people, partners):
    P = projects["projects"]
    active = [p for p in P if p["status"] == "active"]
    news = sorted([x for x in events["events"] if x.get("date")], key=lambda x: x["date"], reverse=True)[:3]
    recent = sorted([x for x in pubs["publications"] if x["type"] != "press"], key=lambda x: x["year"], reverse=True)[:3]
    body = f"""
<section class="welcome"><div class="wrap">
  <div class="welcome-text">
    <h1>California Plug Load Research Center</h1>
    <p class="lead">The California Plug Load Research Center (CalPlug) is the Leading Enabler for Energy Efficiency Solutions in the Use and Design of Appliances and Consumer Products.</p>
    <p class="textlinks"><a href="about.html">About</a><a href="careers.html">Careers</a><a href="contact.html">Contact</a></p>
  </div>
  <figure>{img('/wp-content/uploads/zotwatt-2.jpg', 'CalPlug student researchers in front of the CalPlug sign')}</figure>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Latest news</h2><a class="more" href="news.html">All news and events</a></div>
  <div class="list">{''.join(news_item(x) for x in news)}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Current projects</h2><a class="more" href="research.html">All projects</a></div>
  <div class="list">{''.join(project_row(p, 'title') for p in active)}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Recent publications</h2><a class="more" href="publications.html">All publications</a></div>
  <div class="list">{''.join(pub_entry(x, tag=False) for x in recent)}</div>
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
    body = (head("About", img("/wp-content/uploads/calpluglogo-small.png",
                              "CalPlug, California Plug Load Research Center, University of California, Irvine", "about-logo"))
            + f'<div class="wrap about">{out}</div>')
    return page("about.html", "About", about["sections"][0]["paragraphs"][0][:155], body, site)


def build_research(site, projects):
    P = projects["projects"]
    for p in P:
        need(p, ["id", "title", "status"], "projects.json")
    active = [p for p in P if p["status"] == "active"]
    done = sorted([p for p in P if p["status"] == "completed"], key=lambda p: (p.get("end") or 0, p.get("start") or 0), reverse=True)
    students = ""
    for g in projects["student_projects"]:
        students += f'<h3>{e(g["group"])}</h3><ul class="plain">' + "".join(
            f'<li><a href="{e(url(i["url"]))}">{e(i["title"])}</a></li>' for i in g["items"]) + "</ul>"
    body = head("Projects") + f"""
<section class="section"><div class="wrap">
  <h2>Current projects</h2>
  <div class="list">{''.join(project_row(p, 'full') for p in active)}</div>
</div></section>
<section class="section" id="completed"><div class="wrap">
  <h2>Completed projects</h2>
  <div class="list">{''.join(project_row(p) for p in done)}</div>
</div></section>
<section class="section" id="student-projects"><div class="wrap prose">
  <h2>Student projects</h2>
  {students}
</div></section>
"""
    return page("research.html", "Projects", "Current and completed research projects at the California Plug Load Research Center.", body, site)


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
        return (f'<div class="lead-person">{img(p["photo"], "Portrait of " + p["name"])}<div><h3>{e(p["name"])}</h3>'
                f'<p class="meta">{e(title)} \u00b7 <a href="mailto:{e(p["email"])}">{e(p["email"])}</a></p><p>{e(p.get("bio", ""))}</p></div></div>')

    team = "".join(
        f'<div class="card"><h3>{e(a["name"])}</h3><p>{e(a["title"])}</p><p><a href="mailto:{e(a["email"])}">{e(a["email"])}</a></p></div>'
        for a in people["affiliated_team"])
    grid = lambda items, sub: '<ul class="grid c5">' + "".join(person(x, sub(x)) for x in items) + "</ul>"
    boardsub = lambda m: [m.get("role"), m.get("title"), m.get("org")]
    jump = [("team", "Team"), ("students", "Students"), ("faculty", "Faculty"), ("advisory-board", "Advisory Board"),
            ("technology-council", "Council"), ("alumni", "Alumni")]
    body = head("People", '<p class="jump">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in jump) + "</p>") + f"""
<section class="section" id="team"><div class="wrap">
  <h2>Team</h2>
  {lead(d, d['title'])}
  {''.join(lead(s, s['title']) for s in people['staff'])}
  <h3 class="sub">Affiliated team members</h3>
  <div class="grid c3">{team}</div>
</div></section>
<section class="section" id="students"><div class="wrap">
  <h2>Student researchers</h2>
  {grid(people['students'], lambda s: [s['program'], s['level']])}
</div></section>
<section class="section" id="faculty"><div class="wrap">
  <h2>Affiliated Faculty Leadership</h2>
  {grid(people['affiliated_faculty'], lambda f: [f['dept']])}
</div></section>
<section class="section" id="advisory-board"><div class="wrap">
  <h2>Advisory Board</h2>
  {grid(people['advisory_board'], boardsub)}
  <h3 class="sub">Board members emeriti</h3>{grid(people['advisory_board_emeriti'], boardsub)}
</div></section>
<section class="section" id="technology-council"><div class="wrap">
  <h2>Chief Technology Council</h2>
  {grid(people['technology_council'], boardsub)}
  <h3 class="sub">Council members emeriti</h3>{grid(people['technology_council_emeriti'], boardsub)}
</div></section>
<section class="section" id="alumni"><div class="wrap">
  <h2>Alumni</h2>
  {grid(people['alumni'], lambda s: [s['program'], s['level']])}
</div></section>
"""
    return page("people.html", "People", "The CalPlug team: director, researchers, students, affiliated faculty and advisory boards.", body, site)


def build_facilities(site, partners):
    pages = {"sim-home": "sim-home.html", "sim-lab": "sim-lab.html", "1-kwh-challenge": "1-kwh-challenge.html"}
    cards = ""
    for f in partners["facilities"]:
        cards += (f'<a class="card" href="{pages[f["id"]]}" id="{e(f["id"])}"><div class="thumb">{img(f["images"][0], f["name"])}</div>'
                  f'<h3>{e(f["name"])}</h3><p>{e(f["blurb"])}</p><div class="links"><span>Read more \u2192</span></div></a>')
    body = head("Facilities") + f"""
<section class="section"><div class="wrap">
  <p>{e(partners['facility_intro'])}</p>
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
    body = head("News & Events") + f"""
<section class="section"><div class="wrap"><div class="list">{''.join(news_item(x) for x in dated + undated)}</div>
<p class="after-list"><a class="more" href="events-archive.html">Events Archive: full agendas, speakers and recordings</a></p></div></section>
"""
    return page("news.html", "News & Events", "CalPlug workshops and events.", body, site)


def build_careers(site):
    """Original Careers page; the open positions are shown as cards of one format (DESIGN.md section 2)."""
    html = legacy("careers")
    html = re.sub(r"<p>\s*(?=<img)", "", html)
    html = re.sub(r"<p>\s*$", "", html.strip())
    m1 = re.search(r"<h2>(?:<strong>)?Open Positions.*?</h2>", html)
    m2 = re.search(r"<h2>(?:<strong>)?How to Apply", html)
    if not (m1 and m2):
        ERRORS.append("careers: could not find the 'Open Positions' and 'How to Apply' headings")
        return legacy_page("careers.html", "Careers", "careers", site, "Student research opportunities at CalPlug.")
    pre, part, post = html[:m1.end()], html[m1.end():m2.start()], html[m2.start():]
    mentors = [(m.start(), m.group(1), m.group(2)) for m in
               re.finditer(r"(<img [^>]*>)\s*<p><strong>(Mentors?:.*?)</strong></p>", part, re.S)]
    heads = list(re.finditer(r"<h3>(.*?)</h3>", part, re.S))
    cards = ""
    for i, h in enumerate(heads):
        stops = [x.start() for x in heads[i + 1:i + 2]] + [s for s, _, _ in mentors if s > h.end()] + [len(part)]
        body = part[h.end():min(stops)].strip()
        mentor = [x for x in mentors if x[0] < h.start()]
        who = f'<div class="mentor">{mentor[-1][1]}<p>{mentor[-1][2]}</p></div>' if mentor else ""
        cards += f'<article class="card position">{who}<h3>{h.group(1)}</h3>{body}</article>'
    body = head("CalPlug Careers") + f"""
<section class="section"><div class="wrap prose">{pre}</div>
<div class="wrap"><div class="grid c2 positions">{cards}</div></div>
<div class="wrap prose">{post}</div></section>
"""
    return page("careers.html", "Careers", "Student research opportunities at CalPlug.", body, site)


def build_support(site, partners):
    chips = lambda xs: "".join(f'<span class="tag">{e(x)}</span>' for x in xs)
    body = head("Support & Memberships") + f"""
<section class="section"><div class="wrap prose">{legacy('support')}</div></section>
<section class="section" id="friends"><div class="wrap prose"><h2>Support</h2>{legacy('friends')}</div></section>
<section class="section" id="members"><div class="wrap prose"><h2>Become A Member</h2>{legacy('members')}</div></section>
<section class="section" id="affiliates"><div class="wrap">
  <h2>Members &amp; Affiliates</h2>
  <h3 class="sub">Current CalPlug Members</h3><div class="chips">{chips(partners['members'])}</div>
  <h3 class="sub">Current affiliates</h3><div class="chips">{chips(partners['affiliates'])}</div>
  <div class="logos" style="margin-top:var(--s-32)">{''.join(img(l['src'], l['name']) for l in partners.get('logos', []))}</div>
</div></section>
"""
    return page("support.html", "Support & Memberships", "Support CalPlug as a friend or corporate member.", body, site)


def build_contact(site):
    c = site["contact"]
    maps = "https://www.google.com/maps/search/?api=1&query=Calit2+Building%2C+University+of+California%2C+Irvine%2C+CA+92697"
    body = head("Contact") + f"""
<section class="section"><div class="wrap">
  <div class="contact-top">
    <div>
      <p>CalPlug is located on the main campus of UC Irvine, in the Calit2 building, at the intersection of East Peltason Road and Los Trancos Drive, adjacent to the University Club. The CalPlug main office is located on the fourth floor in suite 4300. CalIt2 administrative offices are in suite 4100.</p>
      <p><strong>{'<br>'.join(e(a) for a in c['address'])}</strong></p>
      <p><a class="more" href="{maps}">Open in Google Maps</a></p>
      <p class="meta">Our hours: {e(c['hours'])}</p>
    </div>
    <figure class="figure">{img('assets/site/calit2-building.jpg', 'The Calit2 Building at UC Irvine, home of CalPlug')}</figure>
  </div>
  <div class="grid c3 contacts">
    <div class="card"><h3>General Information, Directions &amp; Parking</h3><p>Phone: {e(c['general']['phone'])}</p><p><a href="mailto:{e(c['general']['email'])}">{e(c['general']['email'])}</a></p></div>
    <div class="card"><h3>CalPlug Collaborations</h3><p>Phone: {e(c['collaborations']['phone'])}</p><p><a href="mailto:{e(c['collaborations']['email'])}">{e(c['collaborations']['email'])}</a></p></div>
    <div class="card"><h3>General / Calit2 Information</h3><p>Phone: {e(c['calit2']['phone'])}</p><p><a href="mailto:{e(c['calit2']['email'])}">{e(c['calit2']['email'])}</a></p><p><a href="{e(c['calit2']['url'])}">www.calit2.uci.edu</a></p></div>
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
        "careers.html": build_careers(site),
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
