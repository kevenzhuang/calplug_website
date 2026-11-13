# CalPlug Website Design Guide

Version 0.9, 2026-11-12. Status: agreed with Keven Zhuang, not yet built into the pages.
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

Every page starts the same way: the page title (h1) on the left, a short green line under it, then the content. No introductory paragraph unless the original text has one.

| Page | Content, top to bottom |
|---|---|
| Home | Welcome band (see below) · Latest news · Current projects · Recent publications |
| About | Full original logo · About CalPlug · Vision · Mission Statement · Organization Goal · Guidance · Facility (original text; small heading on the left, text on the right) |
| People | Jump links (Team · Students · Faculty · Advisory Board · Council · Alumni) · Director and staff (photo and original bio) · Affiliated team · Students · Affiliated faculty · Advisory Board (+ emeriti) · Chief Technology Council (+ emeriti) · Alumni |
| Projects | Current projects (full original text and image) · Completed projects (list) · Student projects. No filter for now: the research areas are not yet approved |
| Publications | Filter by type · by year, newest first · Earlier documents, folded by category |
| Facilities | Original intro · floor plan · three cards linking to SIM Home, 1 kWh Challenge, SIM Lab (each an original page) |
| News & Events | All items, newest first · link to the Events Archive (original page with agendas and recordings) |
| Careers | Original page; the open positions shown as cards of one format |
| Support & Memberships | Original text of Support, Become A Member, Members & Affiliates |
| Contact | Original location text · photo of the Calit2 Building · address with an "Open in Google Maps" link · general, collaborations and Calit2 contacts · hours. No embedded map |

### Home welcome band

- Text on the left, the group photo on the right, both aligned at the top.
- Text: "California Plug Load Research Center" (h1), the original tagline, then three text links: About · Careers · Contact.
- The band is about 300px high on a laptop, so the first one or two news items are visible without scrolling.
- The photo is shown whole (not cropped), scaled to fit.
- The band has the light blue background (`--blue-tint`); everything below is white.

### Footer

Two short lines on the light footer background, with a green line on top:

1. UC Irvine and Calit2 logos on the left; LinkedIn and Facebook icons on the right.
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
| `--blue-tint` | `#EEF4FA` | Home welcome band only |
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

- One page width: 1000px. Everything starts at the same left edge. Only the home welcome band has its own background.
- Running text is at most 720px wide. Lists use the full page width.
- Spacing scale (px): 4, 8, 12, 16, 24, 32, 48, 64. Between sections 48; between a section title and its content 16.
- Radius 6px. Borders 1px.

### One list format

News, projects and publications use the same row: a narrow left column, then the title and details, rows separated by a 1px line.

| List | Left column | Right column |
|---|---|---|
| News | Image, whole, in a 3:2 frame (180px wide) | Date · title · summary · links |
| Projects | Years (110px) | Title · sponsor · first sentence of the original description · "Full description" · links |
| Publications | Thumbnail (72px) | Title · authors · venue · type · link |

## 4. Components

| Component | Fields, in order | Notes |
|---|---|---|
| Header | Logo · menu | See section 2 |
| Footer | Logos · icons · address, email, copyright | See section 2 |
| Person | Photo · name · role or program · organization (boards only) | Grid of 5 (3 on tablets, 2 on phones) |
| Card | Image (optional) · title · text | Facilities, contact blocks, affiliated team, Careers positions |
| Filter | Pills | Publications by type |
| Full description | Closed by default | Long original text inside lists |
| Social icon | Single-color icon with a hidden text label | LinkedIn, Facebook. Blue on hover |

Only things that can be clicked react to hover.

## 5. Writing

- **Keep the original wording.** Text the center or a person wrote (About, mission, bios, project descriptions, facility pages, Careers, Support) is published as written. Fix spelling only. Do not shorten, summarize or rephrase it; where a short version is needed, use the first sentence word for word. Rewording is a separate, approved task.
- English only.
- Every number, date, title and partner name needs a source. Unverified items are tracked in `CONTENT-NOTES.md` and stay off the site.
- Names: "CalPlug", "California Plug Load Research Center", "Calit2", "UC Irvine".

## 6. Images

### Logo

- Header: `assets/brand/calplug-logo-compact.png`, the icon and the CALPLUG wordmark cut from the original logo file. Lettering unchanged, nothing redrawn. About 44px high.
- About page: the full original logo with all three lines (`assets/legacy/calpluglogo-small.png`).
- Browser tab icon and default images: the icon alone (`assets/brand/calplug-mark.svg`).
- Replace these only with a higher-resolution or vector copy of the same artwork from the lab.
- UC Irvine and Calit2 logos: official files only, used according to each owner's rules. Never redraw them.

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
| 0.9 | 2026-11-12 | Agreed plan after a point-by-point review: welcome band text left and photo right at about 300px so news shows on the first screen; 10-item menu including Careers and Support; compact logo; blue and green used in a top strip, title lines, current-menu line, welcome band and footer line; two-line footer with UC Irvine and Calit2 logos and social icons; line-break rules; people photos squared from the top and checked by eye; project filter removed; Contact with building photo and map link, no embedded map. |

## Open questions

- Official UC Irvine and Calit2 logo files and their usage rules (to be looked up on their official brand pages).
- Whether UC Irvine requires specific footer links (privacy, accessibility) on unit websites.
- Research areas for the Projects page, for Arnold to approve before a filter returns.
- A higher-resolution group photo for the welcome band (the current file is 400 by 225 pixels).
