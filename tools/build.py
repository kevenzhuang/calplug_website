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

NAV = [("index.html", "Home"), ("research.html", "Research"), ("publications.html", "Publications"),
       ("people.html", "People"), ("facilities.html", "Facilities"), ("news.html", "News & Events"),
       ("partner.html", "Partner")]


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
    nav = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == filename else ""}>{e(t)}</a></li>' for h, t in NAV)
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
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/brand/calplug-logo.svg" alt="CalPlug, California Plug Load Research Center, University of California, Irvine" width="616" height="160"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <img class="footer-logo" src="assets/brand/calplug-logo-reversed.svg" alt="CalPlug" width="616" height="160" loading="lazy">
        <p>{'<br>'.join(e(a) for a in c['address'])}</p>
        <p>{e(c['general']['phone'])}<br><a href="mailto:{e(c['general']['email'])}">{e(c['general']['email'])}</a></p>
      </div>
      <div>
        <h2>Site</h2>
        <ul>{''.join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in NAV[1:])}</ul>
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


def head(title, lead):
    return f'<div class="page-head"><div class="wrap"><h1>{e(title)}</h1><p class="lead">{e(lead)}</p></div></div>'


def cta(title, text, label="Partner with us", href="partner.html"):
    return (f'<section class="cta"><div class="wrap"><div><h2>{e(title)}</h2><p>{e(text)}</p></div>'
            f'<a class="btn" href="{href}">{e(label)}</a></div></section>')


def pub_thumb(p):
    """First page of the PDF when we have it, otherwise the standard tile for the publication type."""
    u = p.get("url") or ""
    f = f"assets/pubs/{hashlib.sha1(u.encode()).hexdigest()[:12]}.jpg"
    if u and (ROOT / f).exists():
        return f'<div class="pubthumb"><img src="{f}" alt="" loading="lazy"></div>'
    return f'<div class="pubthumb tile t-{p["type"]}" aria-hidden="true"><span>{PUB_LABELS[p["type"]]}</span></div>'


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
            f'<h3>{e(p["title"])}</h3><p>{e(p.get("description") or p["summary"])}</p>{links(p.get("links"))}</article>')


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
        f'<p>{e(p["summary"])}</p>{f"<p class=\"meta\">{e(p["sponsor"])}</p>" if p.get("sponsor") else ""}</div></article>'
        for p in active)
    pub = "".join(pub_entry(x, tag=False) for x in recent)
    body = f"""
<section class="welcome"><div class="wrap">
  <figure class="reveal">{img('/wp-content/uploads/zotwatt-2.jpg', 'CalPlug student researchers in front of the CalPlug sign')}</figure>
  <div>
    <h1>California Plug Load Research Center</h1>
    <p class="lead">The California Plug Load Research Center (CalPlug) is the Leading Enabler for Energy Efficiency Solutions in the Use and Design of Appliances and Consumer Products.</p>
    <p>Join us in our journey towards improving energy efficiency and cross collaboration.</p>
    <p class="textlinks"><a href="research.html">Our research \u2192</a><a href="people.html">Meet the team \u2192</a><a href="people.html#join">Join the lab \u2192</a></p>
  </div>
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
        rows += (f'<article class="row" id="{e(p["id"])}" data-tags="{" ".join(p["themes"])}"><div class="when">{years(p)}</div>'
                 f'<div><h3>{e(p["title"])}</h3>{f"<p>{e(p["summary"])}</p>" if p.get("summary") else ""}'
                 f'{f"<p class=\"meta\">{e(p["sponsor"])}</p>" if p.get("sponsor") else ""}</div>{links(p.get("links"))}</article>')
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
{cta('Have a research question for us?', 'We work with utilities, agencies and manufacturers on testing, evaluation and field studies.', 'Get in touch')}
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
    j = partners["join"]
    positions = "".join(
        f'<div class="card reveal"><div class="meta">{e(p["id"])}</div><h3>{e(p["area"])}</h3><p>{e(p["description"])}</p>'
        f'<p>Mentor: {e(p["mentor"])}</p><div class="links"><a href="mailto:{e(p["email"])}">{e(p["email"])}</a></div></div>'
        for p in j["positions"])
    body = head("People", "Faculty, researchers, students and advisors behind CalPlug.") + f"""
<section class="section"><div class="wrap">
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
<section class="section"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">UC Irvine</div><h2>Affiliated faculty</h2></div></div>
  <ul class="grid c5">{''.join(person(f, [f['dept']]) for f in people['affiliated_faculty'])}</ul>
</div></section>
<section class="section tint" id="advisory-board"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Guidance</div><h2>Advisory Board</h2></div></div>
  {board(people['advisory_board'])}
  <h3 class="sub">Board members emeriti</h3>{board(people['advisory_board_emeriti'])}
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Guidance</div><h2>Chief Technology Council</h2></div></div>
  {board(people['technology_council'])}
  <h3 class="sub">Council members emeriti</h3>{board(people['technology_council_emeriti'])}
</div></section>
<section class="section tint" id="join"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Join us</div><h2>Student research opportunities</h2><p class="lead">{e(j['program'])}</p></div></div>
  <div class="grid c2">
    <div class="card"><h3>Requirements</h3><ul class="plain">{''.join(f'<li>{e(x)}</li>' for x in j['requirements'])}</ul></div>
    <div class="card"><h3>Benefits</h3><ul class="plain">{''.join(f'<li>{e(x)}</li>' for x in j['benefits'])}</ul></div>
  </div>
  <h3 class="sub">Positions</h3><div class="grid c2">{positions}</div>
  <p class="read" style="margin-top:var(--s-24)">{e(j['apply'])}</p>
</div></section>
"""
    return page("people.html", "People", "The CalPlug team: director, researchers, students, affiliated faculty and advisory boards.", body, site)


def build_facilities(site, partners):
    cards = ""
    for f in partners["facilities"]:
        pics = "".join(f'<div class="thumb">{img(f["images"][0], f["name"])}</div>' if i == 0 else "" for i, _ in enumerate(f["images"]))
        note = f'<p class="meta">{e(f["status_note"])}</p>' if f.get("status_note") else ""
        cards += f'<article class="card reveal" id="{e(f["id"])}">{pics}<h3>{e(f["name"])}</h3><p>{e(f["summary"])}</p>{note}</article>'
    body = head("Facilities", "Labs and demonstration rooms on the fourth floor of the Calit2 Building at UC Irvine.") + f"""
<section class="section"><div class="wrap">
  <div class="grid c2"><div><h2>Where we work</h2><p style="margin-top:var(--s-16)">{e(site['facility'])}</p>
  <p>{e(partners['facility_rooms_note'].split(' Floor plan')[0])}</p></div>
  <figure style="margin:0">{img('/wp-content/uploads/clplg_space.jpg', 'Floor plan of the CalPlug space on the fourth floor of the Calit2 Building')}</figure></div>
</div></section>
<section class="section tint"><div class="wrap"><div class="grid c3">{cards}</div></div></section>
{cta('Need a device tested?', 'CalPlug provides power consumption testing for manufacturers and utilities.', 'Contact us')}
"""
    return page("facilities.html", "Facilities", "CalPlug labs and demonstration facilities at UC Irvine.", body, site)


def build_news(site, events):
    evs = events["events"]
    for x in evs:
        need(x, ["id", "title"], "events.json")
    dated = sorted([x for x in evs if x.get("date")], key=lambda x: x["date"], reverse=True)
    undated = [x for x in evs if not x.get("date")]
    body = head("News & Events", "Workshops, talks and announcements from CalPlug.") + f"""
<section class="section"><div class="wrap"><div class="newslist">{''.join(news_item(x) for x in dated + undated)}</div></div></section>
"""
    return page("news.html", "News & Events", "CalPlug workshops and events.", body, site)


def build_partner(site, partners):
    s, c = partners["support"], site["contact"]
    ways = "".join(f'<div class="card reveal"><h3>{e(w["name"])}</h3><p>{e(w["how"])}</p></div>' for w in s["ways"])
    li = lambda xs: "".join(f'<span class="tag">{e(x)}</span>' for x in xs)
    body = head("Partner with CalPlug", "CalPlug invites all interested groups to join the effort as members and partners.") + f"""
<section class="section"><div class="wrap">
  <p class="lead">{e(s['intro'])}</p>
  <h2 class="sub">Ways to support</h2><div class="grid c2">{ways}</div>
</div></section>
<section class="section tint"><div class="wrap">
  <h2>Members</h2><div class="chips" style="margin:var(--s-16) 0 var(--s-32)">{li(partners['members'])}</div>
  <h2>Affiliates</h2><div class="chips" style="margin:var(--s-16) 0 var(--s-32)">{li(partners['affiliates'])}</div>
  <div class="logos reveal">{''.join(img(l['src'], l['name']) for l in partners.get('logos', []))}</div>
</div></section>
<section class="section" id="contact"><div class="wrap"><h2>Contact</h2>
  <div class="grid c3" style="margin-top:var(--s-24)">
    <div class="card"><h3>Collaborations</h3><p>{e(c['collaborations']['name'])}<br>{e(c['collaborations']['phone'])}</p><div class="links"><a href="mailto:{e(c['collaborations']['email'])}">{e(c['collaborations']['email'])}</a></div></div>
    <div class="card"><h3>General information</h3><p>{e(c['general']['phone'])}<br>{e(c['hours'])}</p><div class="links"><a href="mailto:{e(c['general']['email'])}">{e(c['general']['email'])}</a></div></div>
    <div class="card"><h3>Location</h3><p>{'<br>'.join(e(a) for a in c['address'])}</p><p>{e(c['location_note'])}</p></div>
  </div>
</div></section>
"""
    return page("partner.html", "Partner", "Support CalPlug as a member, friend or research partner.", body, site)


def main():
    site, projects, pubs = load("site"), load("projects"), load("publications")
    people, events, partners = load("people"), load("events"), load("partners")
    pages = {
        "index.html": build_home(site, projects, pubs, events, people, partners),
        "research.html": build_research(site, projects),
        "publications.html": build_publications(site, pubs),
        "people.html": build_people(site, people, partners),
        "facilities.html": build_facilities(site, partners),
        "news.html": build_news(site, events),
        "partner.html": build_partner(site, partners),
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
