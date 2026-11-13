# CalPlug Website Design Guide

Version 0.10, 2026-11-13. Status: built after Keven Zhuang's review of 0.9; waiting for his look.
Read this before changing any page, style or template. If a problem is not covered here, fix this guide first, then fix the page.

**Formats come first.** Every kind of content (a news item, a publication, a person, a project) has one format, defined here and in `MAINTAINING.md`. New content is built on these formats. When a format turns out to be wrong or incomplete, improve the format, record the change in the change log, and bring existing content up to it. No one-off exceptions on a page.

## 1. What the site is for

calplug.org is the public face of the California Plug Load Research Center (CalPlug) at UC Irvine: a research lab's site, not a company's.

| Reader | What they want | Where they go |
|---|---|---|
| Sponsors and partners | What CalPlug does, what it has delivered, who backs it, how to support it | Home, About, Projects, Support |
| People curious about CalPlug | A fast, trustworthy overview and recent news | Home, About, News & Events |
| Future students | Research, the team, how to join | Projects, People, Careers |

Simple and direct: the site exists so people can find information, not to impress. If a page feels heavy, remove something; do not add decoration. No call-to-action bands ("Get in touch", "Partner with us") at the bottom of pages.

## 2. Navigation and pages

### Header

One row: the logo on the left, the menu on the right. Ten items, no drop-down menus:

Home · About · People · Projects · Publications · Facilities · News & Events · Careers · Support · Contact

- The menu label is "Support"; the page title is "Support & Memberships".
- When the window is too narrow for one row, the menu collapses behind a Menu button. It never wraps onto two rows.
- The current page is marked with a short green line under its menu item.

### Pages

Every page starts the same way: the page title (h1) on the left, a short green line under it, then at most a two-sentence introduction (19px), then the content.

| Page | Content, top to bottom |
|---|---|
| Home | Welcome (see below) · Latest news (3 list rows) · Current projects (4 small cards) · Recent publications (3 list rows) |
| About | About CalPlug · Vision · Mission Statement · Organization Goal · Guidance · Facility (original text; small heading on the left, text on the right) |
| People | Jump links (Team · Students · Faculty · Advisory Board · Council · Alumni) · Director and staff (photo, first two sentences of the bio, "Full bio" to open the rest) · Affiliated team · Students · Affiliated faculty · Advisory Board (+ emeriti) · Chief Technology Council (+ emeriti) · Alumni |
| Projects | Intro · filter by research area (draft areas, see Open questions) · Current projects (cards, two per row) · Completed projects (list rows) · Student projects |
| Project page (`project-<id>.html`) | Title · years, sponsor, area · partners · full original description · image · reports · link back to Projects. One page per project that has a description |
| Publications | Filter by type · by year, newest first · Earlier documents, folded by category |
| Facilities | Original intro · floor plan · three cards linking to SIM Home, 1 kWh Challenge, SIM Lab (each an original page) |
| News & Events | All items, newest first · link to the Events Archive (original page with agendas and recordings) |
| Careers | Intro · deadline notice · "What you get" and "What we ask" cards · Open positions (cards: ID pill, title, one sentence, up to 3 tasks, mentors with photos) · How to apply (4 numbered steps). Content in `data/careers.json` |
| Support & Memberships | Intro · Current members (large logo tiles) · Ways to support (3 cards: member, gift, equipment) · Membership levels (3 cards: Gold, then what Platinum and Diamond add; full comparison table folded below) · Past members and current affiliates (logo tiles). Content in `data/support.json` |
| Contact | Original location text · photo of the Calit2 Building · address with an "Open in Google Maps" link · general, collaborations and Calit2 contacts · hours. No embedded map |

### Home welcome

- Text on the left, the group photo on the right, both aligned at the top. White background, a 1px line below.
- Text: "California Plug Load Research Center" (h1), the tagline from `data/site.json` (at most 40 words; says what CalPlug does in plain words), then three text links: About · Join us · Contact.
- About 300px high on a laptop, so the first news items are visible without scrolling.
- The photo is shown whole (not cropped), scaled to fit.

### Footer

Two short lines on the light footer background, with a green line on top:

1. On the left, the UC Irvine primary logo (`assets/brand/uci-logo.png`, 24px high, links to uci.edu), then 24px of space, then the Calit2 logo (`assets/brand/calit2-logo.png`, 40px high, links to calit2.uci.edu). The two logos stand apart, never joined into one lockup. On the right, LinkedIn and Facebook icons. The UC Irvine seal is not used (see 6. Images, Logo).
2. One line of small text: address · email · copyright.

No site map in the footer: every page not in the menu is reached from its parent page.

## 3. Visual standard

### Color and where it is used

Blue and green are sampled from the CalPlug logo. They are used in small, meaningful places only.

| Token | Value | Used for |
|---|---|---|
| `--blue` | `#005BAA` | Links, selected filter, menu hover, icon hover, left half of the top strip |
| `--green` | `#8BC53F` | Right half of the top strip; line under the current menu item; short line under page and section titles; line on top of the footer. Never for text (2.07:1 on white) |
| `--green-text` | `#4A7A1C` | Dates and years in lists (5.13:1 on white) |
| `--blue-tint` | `#EEF4FA` | Pills (position IDs, membership levels) and notice boxes (with a 3px blue left line) |
| `--tint` | `#F6F8FA` | Footer, image frames |
| `--ink` | `#1B2530` | Headings and body text |
| `--muted` | `#5B6875` | Authors, sponsors, summaries, small text |
| `--line` | `#E3E8EE` | Dividers and borders, always 1px |
| `--white` | `#FFFFFF` | Page background |

The top of every page has a 4px strip, blue on the left half and green on the right, echoing the logo ring.

Not used: large dark blocks, gradients, shadows, colored cards, green text on white.

### Type hierarchy

One family (the system UI font). Weights: 400 for text, 600 for headings, 500 for the menu.

| Level | Size | Color | Used for |
|---|---|---|---|
| Page title (h1) | 34px (28px on phones) | ink | One per page |
| Section title (h2) | 24px (21px on phones) | ink | "Latest news", a year, a People section |
| Item title (h3) | 17px | ink | A news item, project, publication, person |
| Lead | 19px | ink | The home tagline; at most one per page |
| Body | 16px, line height 1.65 | ink | Paragraphs |
| Small | 14px | muted | Authors, venues, sponsors, summaries, dates, menu, footer |

No uppercase labels above headings. No underlines except on hover.

### Line breaks

- Titles fit on one line on a laptop where possible. When a title must wrap, it breaks between phrases and the lines are of similar length (`text-wrap: balance`).
- A single word never sits alone on the last line of a title or a short paragraph (`text-wrap: pretty`).
- Names, dates and short fixed terms never split across lines: "UC Irvine", "CalPlug/ITAC", "May 5, 2026", "Calit2 Building". Use a non-breaking space or a no-wrap span.
- After any change to a title or layout, look at the page at 1440, 1024 and 390px wide and check each wrapped line by eye.

### Layout

- One page width: 1080px (wide enough for the ten-item menu). Everything starts at the same left edge. No page section has its own background.
- Running text is at most 720px wide. Lists use the full page width.
- Spacing scale (px): 4, 8, 12, 16, 24, 32, 48, 64. Between sections 48; between a section title and its content 16.
- Radius 6px. Borders 1px.

### Three building blocks

All content is shown with one of three blocks. The Publications list is the model: every entry has the same parts in the same places, and each part is short. Never paste long text into a page; if content does not fit a block, change the block here first.

**1. List row.** A narrow left column, then the title and details; rows separated by a 1px line. For long lists that people scan.

| List | Left column | Right column |
|---|---|---|
| News | Image, whole, in a 3:2 frame (180px wide) | Date · title · summary · links |
| Completed projects | Years (110px) | Title (links to the project page) · sponsor and area · summary · reports · Details |
| Publications | Thumbnail (72px) | Title · authors · venue · type · link |

**2. Card.** A bordered box: optional image on top (whole, in a 16:9 frame on the tint background), then a small meta line (years, sponsor), title, short text, and the link at the bottom. Cards in one row are the same height. For a few items that each deserve a look: current projects (2 per row; 4 small ones on Home), facilities (3), Careers positions (2), ways to support and membership levels (3). Two per row on tablets, one on phones.

**3. Logo tile.** Every logo in a white box of the same size (112px high; 168px for current members), fitted whole and centered. An organization without a usable logo file gets the same box with its name in text. For members and affiliates.

## 4. Components

| Component | Fields, in order | Notes |
|---|---|---|
| Header | Logo · menu | See section 2 |
| Footer | Logos · icons · address, email, copyright | See section 2 |
| Person | Photo · name · role or program · organization (boards only) | Grid of 5 (3 on tablets, 2 on phones) |
| List row | See section 3 | News, completed projects, publications |
| Card | See section 3 | Current projects, facilities, contact blocks, affiliated team, Careers, Support |
| Logo tile | See section 3 | Support |
| Pill | Short label on the light blue tint | Position IDs, membership levels |
| Notice | One sentence on the light blue tint with a blue left line | Deadlines. At most one per page |
| Steps | Numbered columns with a blue top line | How to apply |
| Filter | Round buttons | Publications by type, Projects by research area |
| More on demand | Closed by default ("Full bio", "Compare all benefits") | Long text that most readers skip |
| Social icon | Single-color icon with a hidden text label | LinkedIn, Facebook. Blue on hover |

Only things that can be clicked react to hover.

## 5. Writing

- **Short pieces, full text one click away.** Lists and cards show short text written for the site; the full original text stays on the item's own page or behind "Full bio" / "Details", word for word. Nothing is deleted.
- **Length limits** (the build stops when one is broken):

| Piece | Limit |
|---|---|
| Page introduction | 2 sentences, 45 words |
| Home tagline | 40 words |
| Project summary, news summary | 35 and 30 words |
| Careers position | 1 sentence of 30 words, at most 3 tasks |
| List bullets | One idea each, about one line |

- **Plain and direct.** Say what CalPlug does, for whom, with what result. No slogans ("leading enabler"), no repeated thanks, no italic or bold sentences used as headings.
- **Rewritten text is reviewed.** Every piece written or shortened for the new site is listed in `CONTENT-NOTES.md` for Arnold to check. About, mission, vision, bios and project descriptions stay as the center wrote them.
- English only.
- Every number, date, title and partner name needs a source. Unverified items are tracked in `CONTENT-NOTES.md` and stay off the site.
- Names: "CalPlug", "California Plug Load Research Center", "Calit2", "UC Irvine".

## 6. Images

### Logo

- Header: `assets/brand/calplug-logo-compact.png`, the icon and the CALPLUG wordmark cut from the original logo file. Lettering unchanged, nothing redrawn. About 44px high.
- Browser tab icon and default images: the icon alone (`assets/brand/calplug-mark.svg`).
- Replace these only with a higher-resolution or vector copy of the same artwork from the lab.
- UC Irvine logo: the primary logo file Keven Zhuang provided (`assets/brand/uci-logo.png`, 266×45). Keep the clear space around it; nothing locked up with it; not smaller than 3/16 inch (about 18px); never redrawn or recolored. A larger or vector copy from the UC Irvine brand asset library (UCInetID login) would look sharper on high-resolution screens; swap it in when available.
- UC Irvine seal: not used. UC Irvine's brand rules say the seal should not be used on the web and cannot be modified; questions go to graphicservices@uci.edu.
- Calit2 logo: the file Keven Zhuang provided (`assets/brand/calit2-logo.png`, square). Shown as is, at 40px high, with a little space from the UC Irvine name; never recolored or redrawn.

### No cropping

- Photos, flyers, diagrams and first pages are never cropped. Each kind has one frame shape; the whole image is fitted inside it on a neutral background.
- The welcome photo, the Contact building photo (`assets/site/calit2-building.jpg`), and the director and staff photos are shown at their own proportions.

### People photos

- The people grid uses square frames so it stays even. The square is taken from the top of the photo so the head and shoulders are always fully visible.
- Every photo is checked by eye after it is added. If a face is cut, set `photo_position` for that person in `data/people.json` (for example `"center 20%"`) instead of changing the rule.
- Best: people supply square portraits, at least 600 by 600 pixels.
- No photo: one uniform placeholder with the person's initials.

### News images

- Every item has one image, fitted whole into a 3:2 frame.
- Order of preference: a photo from the event, the event flyer, then the default `assets/brand/news-default.svg`.
- New images: at least 1200 by 800 pixels, JPEG, under 400 KB, in `assets/news/`.

### Publication thumbnails

- `tools/make_pub_thumbs.py` tries, in order: the first page of the linked PDF; the first page of a PDF named on the linked page; the linked page's preview image.
- Otherwise the one default image `assets/brand/pub-default.svg`. No colored tiles.

## 7. Motion

- Hover feedback only: a 0.2s color change. No entrance animations, carousels or auto-play.
- Off when the visitor's system asks for reduced motion.
- All content is visible without JavaScript.

## 8. Responsive and accessibility

- Checked widths: 1440, 1024, 820, 390, 320. No horizontal scroll at any width.
- Every link, button and icon is reachable by keyboard and has a visible focus ring and a text label.
- One h1 per page; headings do not skip levels. Every image has alt text; decorative images use empty alt.
- Text contrast at least 4.5:1.

## 9. Checks before publishing

1. `python tools/build.py` builds without errors.
2. `python tools/check.py` passes (links, alt text, placeholder text, empty sections, one h1).
3. Screenshots at 1440, 1024 and 390 look right, including line breaks (section 3) and people photos (section 6). A passing script does not mean the page looks good.
4. Anything new that this guide does not cover has been added to this guide.

## 10. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-12 | First draft: purpose, pages, tokens from the logo, components, writing and image rules. |
| 0.2 | 2026-11-12 | Home redesigned as a lab home page (welcome + news first). Original tagline restored. |
| 0.3 | 2026-11-12 | News image standard; publication thumbnails; "formats come first" rule. |
| 0.4 | 2026-11-12 | Original logo restored; no-cropping standard; entrance animations removed. |
| 0.5 | 2026-11-12 | Welcome text left, photo right; compact header logo; default images; wider thumbnail search. |
| 0.6 | 2026-11-12 | About page; original wording kept everywhere. |
| 0.7 | 2026-11-12 | Navigation copied from the previous site with drop-downs; original pages restored. Reviewed as too heavy. |
| 0.8 | 2026-11-12 | Lighter version: one-row menu, stacked welcome, one list format, type hierarchy. Reviewed: news too low, logo too small, colors unused, Careers hidden. |
| 0.10 | 2026-11-13 | After Keven's review ("too much text, no standard; Publications is the cleanest"): three building blocks (list row, card, logo tile) and length limits for every piece of text, checked by the build. Home welcome is white with a new plain tagline; Home projects as cards. Projects: research-area filter (draft), current projects as cards, completed projects as list rows, one page per project with the full text. Careers and Support rebuilt from data files with cards, pills, a deadline notice, numbered steps, membership levels (benefits table retyped from the old image) and logo tiles. People bios shortened with "Full bio". About logo removed. |
| 0.9.3 | 2026-11-13 | Footer: UC Irvine primary logo (file from Keven Zhuang) replaces the "UC Irvine" text, set apart from the Calit2 logo. |
| 0.9.2 | 2026-11-13 | Footer: Calit2 logo added (file from Keven Zhuang) next to the "UC Irvine" text. UC Irvine seal not used, following UC Irvine's rule that the seal is not for the web. |
| 0.9.1 | 2026-11-12 | Built. Page width 1080px so the ten-item menu fits; menu collapses below 1080px. Footer follows UC Irvine's rule: one UC Irvine logo plus "Calit2" in text, not two logos. |
| 0.9 | 2026-11-12 | Agreed plan after a point-by-point review: welcome band text left and photo right at about 300px so news shows on the first screen; 10-item menu including Careers and Support; compact logo; blue and green used in a top strip, title lines, current-menu line, welcome band and footer line; two-line footer with UC Irvine and Calit2 logos and social icons; line-break rules; people photos squared from the top and checked by eye; project filter removed; Contact with building photo and map link, no embedded map. |

## Open questions

- A larger or vector copy of the UC Irvine primary logo, for sharper display (optional).
- Research areas for the Projects filter are a draft (`data/projects.json`, `themes`), for Arnold to approve.
- All text written or shortened for 0.10 (see `CONTENT-NOTES.md`), for Arnold to approve.
