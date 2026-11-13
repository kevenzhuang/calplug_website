# CalPlug Website Design Guide

Version 0.8 (draft), 2026-11-12. Read this before changing any page, style or template.
If a problem is not covered here, fix this guide first, then fix the page.

**Formats come first.** Every kind of content (a news item, a publication, a person, a project) has one format, defined here and in `MAINTAINING.md`. New content is built on these formats. When a format turns out to be wrong or incomplete, improve the format, record the change in the change log, and bring existing content up to it. Do not make one-off exceptions on a page.

## 1. What the site is for

calplug.org is the public showcase of the California Plug Load Research Center (CalPlug) at UC Irvine. It is not a paper registry or an intranet.

| Reader | What they want | Where they go |
|---|---|---|
| Sponsors and partners (utilities, agencies, companies) | What CalPlug does, what it has delivered, who backs it, how to work together | Home, Research, Partner |
| People curious about CalPlug (peers, media, UCI) | A fast, trustworthy overview and recent news | Home, News & Events |
| Future students | Research areas, the team, how to join | Research, People |

Simple and direct: the site exists so people can find information, not to impress. Tone: a research lab's site, not a company's. Modern, simple, credible, with the life of a working lab. The home page leads with people and news, not with marketing: no statistics strip, no call-to-action bands, text links instead of large buttons. Every page answers one question and offers one next step.

## 2. Pages and navigation

**Menu: one row, eight items, no drop-down menus.** Home · About · People · Projects · Publications · Facilities · News & Events · Contact.

Pages that are not in the menu are reached from their parent page and from the footer. Nothing from the previous site is dropped.

| Page | In menu | Reached from | Content |
|---|---|---|---|
| Home `index.html` | yes | | Welcome (photo on top, then name, tagline, three text links) · Latest news (3) · Current projects (titles) · Recent publications (3) |
| About `about.html` | yes | | Logo · About CalPlug · Vision · Mission Statement · Organization Goal · Guidance · Facility |
| People `people.html` | yes | | Director · Staff · Affiliated team · Students · Alumni · Affiliated faculty · Advisory Board · Chief Technology Council |
| Projects `research.html` | yes | | Current · Completed (filter by area) · Student projects |
| Publications `publications.html` | yes | | By year, newest first, filter by type · Earlier documents |
| Facilities `facilities.html` | yes | | Overview, floor plan, three cards |
| SIM Home, SIM Lab, 1 kWh Challenge | no | Facilities, footer | Original pages |
| News & Events `news.html` | yes | | All items, newest first |
| Events Archive `events-archive.html` | no | News & Events, footer | Original page with agendas and recordings |
| Careers `careers.html` | no | Home, footer | Original page |
| Support & Memberships `support.html` | no | Home, footer | Original three pages as sections, members and affiliates |
| Contact `contact.html` | yes | | Location, phones, emails, hours |

No call-to-action bands at the bottom of pages. CalPlug is a research center, not a company.

Pages copied whole from the old site live in `content/legacy/*.html` (made by `tools/import_pages.py`) and are shown word for word.

Rules:
- A page or section with no content is not published. No "coming soon", no placeholder text.
- All items of one kind use the same component with the same fields in the same order. A missing optional field is left out, never filled with "N/A".
- Old URLs redirect to the new pages. The PDFs under `/wp-content/uploads/` keep their URLs.

## 3. Visual standard

The look is light and quiet: white background, one text column, thin dividers, few boxes. If a page feels heavy, remove something; do not add decoration. Only the values below may appear in CSS (they are variables at the top of `src/css/site.css`).

### Color

| Token | Value | Use |
|---|---|---|
| `--blue` | `#005BAA` | Links, the selected filter, the current menu item |
| `--green` | `#8BC53F` | The line under the current menu item only. Never for text (2.07:1 on white) |
| `--green-text` | `#4A7A1C` | Dates and years in lists (5.13:1) |
| `--ink` | `#1B2530` | Headings and body text |
| `--muted` | `#5B6875` | Secondary text: authors, sponsors, summaries, footer |
| `--line` | `#E3E8EE` | Dividers and borders, always 1px |
| `--tint` | `#F6F8FA` | Footer and image frames only. Sections do not alternate background colors |
| `--white` | `#FFFFFF` | Page background |

Blue and green are sampled from the logo. No other colors, no gradients, no shadows.

### Type hierarchy

One family: the system UI font. Two weights only: 400 (text) and 600 (headings); the menu uses 500.

| Level | Token | Size | Weight | Color | Used for |
|---|---|---|---|---|---|
| Page title (h1) | `--fs-h1` | 34px (28px on phones) | 600 | ink | One per page |
| Section title (h2) | `--fs-h2` | 24px (21px on phones) | 600 | ink | "Latest news", "Completed projects", a year |
| Item title (h3) | `--fs-h3` | 17px | 600 | ink | A news item, project, publication, person |
| Lead | `--fs-lead` | 19px | 400 | ink | One opening paragraph at most per page |
| Body | `--fs-body` | 16px, line height 1.65 | 400 | ink | Paragraphs |
| Small | `--fs-small` | 14px | 400 | muted | Authors, venues, sponsors, summaries, dates, links under an item, menu, footer |

No uppercase labels above headings, no bold inside running text except what the original text has, no underlines except on hover.

### Layout

- One page width: 1000px (`--page`). Titles, lists and text all start at the same left edge. Nothing is centered except the home welcome block.
- Running text is at most 720px wide (`--text`). Lists (news, projects, publications) use the full page width.
- Spacing scale (px): 4, 8, 12, 16, 24, 32, 48, 64. Between sections: 48. Between a section title and its content: 16.
- Radius 6px. Borders 1px `--line`.

### The list format

News, projects and publications all use the same row: a narrow left column, then title and details, separated by a 1px divider.

| List | Left column | Right column |
|---|---|---|
| News | Image in a 3:2 frame (180px) | Date · title · summary · links |
| Projects | Years (110px) | Title · sponsor · first sentence · "Full description" · links |
| Publications | Thumbnail (72px) | Title · authors · venue · type and link |

## 4. Components

| Component | Fields, in order | Notes |
|---|---|---|
| Header | Original logo · menu | One row. Under 900px the menu opens from a Menu button |
| Footer | Address · Site · More (pages not in the menu) · Connect · copyright | Tint background |
| Person | Photo · name · role or program · organization (boards) | Grid of 5 (3 on tablets, 2 on phones). Initials when there is no photo |
| Card | Image (optional) · title · text | Only for facilities, contact blocks and the affiliated team |
| Filter | Pills | Projects by area, publications by type |
| Full description | Closed by default | Holds long original text so lists stay scannable |

Only things that can be clicked react to hover.

## 5. Writing

- **Keep the original wording.** Text that the center or a person wrote (About, mission, bios, project descriptions, facility descriptions) is published as written. Fix spelling only. Do not shorten, summarize or rephrase it; if a short version is needed, use the first sentence word for word. Rewording is a separate, approved task.

- English only.
- Lead with the point. Short sentences. Few adjectives.
- Every number, date, title and partner name needs a source (a report, a paper, an official page). No source, no claim. Unverified items are tracked in `CONTENT-NOTES.md` and stay off the site.
- Words like "leading", "first" or "premier" are not used in new text unless a third party said so and is cited. Exception: the center's own long-standing tagline on the home page.
- Names: "CalPlug" (not Calplug); "California Plug Load Research Center" on first use per page; "Calit2"; "UC Irvine".
- Sponsor names are written out on first use, with the abbreviation in parentheses: "California Energy Commission (CEC)".

## 6. Images

- People: square crop, face centered, same framing. Use a photo only with the person's consent.
- Partner and sponsor logos and other images already used on the previous calplug.org may be reused. New logos need the organization's agreement.
- New images are copied into `assets/`, not hot-linked from other websites. No AI-generated people.
- Every image has alt text that describes it. Decorative images use empty alt.
- Provide images at 1x and 2x; the hero at 1600px wide or more.

### Logo

- Use the existing CalPlug logo file unchanged (`assets/legacy/calpluglogo-small.png`). Do not redraw it, change its lettering, recolor or stretch it. Replace it only with a higher-resolution or vector copy of the same artwork from the lab.
- Header (48px high) and About page: the full original logo.
- `assets/brand/calplug-logo-compact.png` (icon and CALPLUG wordmark cut from the original file) is available for small spaces.
- `assets/brand/calplug-mark.svg` is the icon alone (no lettering), used for the browser tab icon and inside the default images.
- UC Irvine and Calit2 logos go in the footer once official files are supplied. Use only official files and follow each owner's rules; never redraw them.

### No cropping (standard)

- Content images (photos, flyers, diagrams, first pages) are never cropped. Each kind has one frame shape; the whole image is fitted inside it on a neutral background.
- The welcome photo and the director and staff photos are shown at their own proportions.
- The only exception is the grid of people: portraits are cropped to a square from the top so the grid stays even. Supply square portraits to avoid any crop.

### News images (standard)

- Every news or event item has exactly one image, fitted whole inside a 3:2 frame.
- Order of preference: a photo from the event, then the event flyer, then the one default image `assets/brand/news-default.svg` (used automatically when `image` is empty).
- New images: at least 1200 by 800 pixels, JPEG, under 400 KB, in `assets/news/`.

### Publication thumbnails (standard)

- Every publication has a thumbnail in a portrait slot (letter-page proportion).
- `tools/make_pub_thumbs.py` looks for an image in this order: first page of the linked PDF; first page of a PDF named on the linked page; the linked page's own preview image.
- If none is found, the slot shows the one default image `assets/brand/pub-default.svg`. No colored tiles, no hand-made exceptions.

## 7. Motion

- Hover feedback only, 0.2s color change. No entrance animations, no carousels, no auto-playing anything.
- Off when the visitor's system asks for reduced motion.
- All content is visible without JavaScript.

## 8. Responsive and accessibility

- Checked widths: 1440, 1024, 820, 390, 320. No horizontal scroll at any of them.
- People grid: 5 columns on desktop, 3 on tablets, 2 on phones.
- Every link and button is reachable by keyboard and shows a visible focus ring.
- One `h1` per page; headings do not skip levels.

## 9. Checks before publishing

1. `python tools/build.py` builds without errors (data format, missing files).
2. `python tools/check.py` passes (broken links, placeholder text, empty sections, missing alt text).
3. Screenshots at 1440 and 390 look right. A script passing does not mean the page looks good.
4. Anything new that this guide does not cover has been added to this guide.

## 10. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-12 | First draft: purpose, 7 pages, tokens from the logo, components, writing and image rules. Images from the previous site may be reused (decision: Keven). |
| 0.2 | 2026-11-12 | Home redesigned as a lab home page (welcome + news first), after review: the first version read like a company site. Original tagline restored at Keven's request. |
| 0.3 | 2026-11-12 | SVG logo; news image standard (every item has an image, with a default); publication thumbnails (first page of the PDF, or a type tile); 'formats come first' rule. |
| 0.4 | 2026-11-12 | Original logo restored (no redrawn lettering); no-cropping standard; entrance animations removed; welcome section simplified. |
| 0.5 | 2026-11-12 | Welcome: text left, photo right. Compact header logo cut from the original artwork. One default image each for news and publications; thumbnail finder also tries PDFs and preview images on linked pages. |
| 0.6 | 2026-11-12 | About page added. Original wording kept everywhere (bios, projects, facilities); imported by `tools/import_text.py`. |
| 0.7 | 2026-11-12 | Navigation follows the previous site (with sub-menus); Facilities sub-pages, Careers, Contact, Support and Events Archive restored with original content; call-to-action bands removed; full logo in a two-row header. |
| 0.8 | 2026-11-12 | Lighter redesign after review (0.7 was heavy and cluttered): one-row menu without drop-downs, stacked welcome, one page width, one list format, written type hierarchy, light footer. |

## Open questions

- Official UC Irvine and Calit2 logo files for the footer are needed from the lab.
- UC Irvine and Calit2 brand and web requirements (logo use, footer statements, accessibility policy) have not been checked yet.
- Research themes on the Research page are a draft grouping and need Arnold's approval.
