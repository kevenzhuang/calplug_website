# CalPlug Website Design Guide

Version 0.3 (draft), 2026-11-12. Read this before changing any page, style or template.
If a problem is not covered here, fix this guide first, then fix the page.

**Formats come first.** Every kind of content (a news item, a publication, a person, a project) has one format, defined here and in `MAINTAINING.md`. New content is built on these formats. When a format turns out to be wrong or incomplete, improve the format, record the change in the change log, and bring existing content up to it. Do not make one-off exceptions on a page.

## 1. What the site is for

calplug.org is the public showcase of the California Plug Load Research Center (CalPlug) at UC Irvine. It is not a paper registry or an intranet.

| Reader | What they want | Where they go |
|---|---|---|
| Sponsors and partners (utilities, agencies, companies) | What CalPlug does, what it has delivered, who backs it, how to work together | Home, Research, Partner |
| People curious about CalPlug (peers, media, UCI) | A fast, trustworthy overview and recent news | Home, News & Events |
| Future students | Research areas, the team, how to join | Research, People |

Tone: a research lab's site, not a company's. Modern, simple, credible, with the life of a working lab. The home page leads with people and news, not with marketing: no statistics strip, no call-to-action bands, text links instead of large buttons. Every page answers one question and offers one next step.

## 2. Pages

Seven pages, one navigation level. No drop-down menus.

| Page | Question it answers | Sections, in order | Next step |
|---|---|---|---|
| Home | What is CalPlug and what is new? | Welcome (group photo, name, short intro, text links) · Latest news (4, with photos) · Current projects (compact list) · Recent publications (4) | Read the news / See research / Meet the team |
| Research | What has CalPlug worked on, and with whom? | Intro · Active projects (large cards) · Completed projects (compact rows, all shown, filter by theme and sponsor) · Student projects | Read a report / Contact |
| Publications | What has CalPlug published? | Filter (type, year) · List by year, newest first · Archive (older undated documents) | Open the PDF or DOI |
| People | Who is CalPlug and how do I join? | Director · Staff · Students · Affiliated faculty · Advisory Board · Technology Council · Alumni · Join us | Apply / Email |
| Facilities | What can CalPlug test and demonstrate? | Intro and floor plan · SIM Lab · SIM Home · 1 kWh Challenge | Contact about testing |
| News & Events | What happened recently? | Upcoming (only if any) · Past events by date, newest first | Read the recap |
| Partner | How do I support or join CalPlug? | Why support · Membership · Friends of CalPlug · Members and affiliates · Contact details and location | Email the contact |

Rules:
- A page or section with no content is not published. No "coming soon", no placeholder text.
- All items of one kind use the same component with the same fields in the same order. A missing optional field is left out, never filled with "N/A".
- Old URLs redirect to the new pages. The PDFs under `/wp-content/uploads/` keep their URLs.

## 3. Design tokens

Only these values may appear in CSS. They are defined once as CSS variables in `css/tokens.css`.

### Color

Taken from the CalPlug logo (sampled from the logo file; confirm against the original artwork).

| Token | Value | Use | Contrast |
|---|---|---|---|
| `--blue` | `#005BAA` | Links, primary buttons, headings accents | 6.83:1 on white |
| `--green` | `#8BC53F` | Accents, icons, rules, highlights on dark. Never for text on white. | 2.07:1 on white (fails for text) |
| `--green-text` | `#4A7A1C` | Green text or small labels on white | 5.13:1 on white |
| `--navy` | `#0B2A4A` | Footer and dark bands | white on navy 14.54:1 |
| `--ink` | `#16212B` | Body text | 16.32:1 on white |
| `--muted` | `#566473` | Secondary text, meta lines | 6.06:1 on white |
| `--line` | `#DCE3EA` | Borders, dividers | n/a |
| `--tint` | `#F3F7FA` | Alternate section background | blue on tint 6.34:1 |
| `--white` | `#FFFFFF` | Page background | n/a |

The magenta link color on the current site is dropped. Body text and background must reach at least 4.5:1.

### Type

- One family for everything: the system UI stack (`system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`). No web font download in v0.1.
- Sizes (px): 13, 15, 17, 20, 26, 34, 46. Body is 17. No other sizes.
- Weights: 400 and 650 only. Line height 1.6 for body, 1.2 for headings.
- Line length: 60 to 75 characters for body text.

### Space, radius, shadow

- Spacing scale (px): 4, 8, 12, 16, 24, 32, 48, 72, 104.
- Content width 1120px; reading width 720px. Page gutter 24px (16px under 480px).
- Radius: 6px for cards and buttons, 999px for tags. Photos of people are square with 6px radius.
- One shadow only, for cards that can be clicked, on hover: `0 6px 20px rgba(11, 42, 74, 0.10)`.

## 4. Components

| Component | Fields, in order | Notes |
|---|---|---|
| Header | Logo · 7 nav links | Collapses to a menu button under 820px |
| Footer | CalPlug name and address · nav · UCI and Calit2 names · social links · copyright year | On every page |
| Button | Label | Primary (blue fill) and secondary (blue outline) only |
| Active project card | Title · years and sponsor · description · image (optional) · links | Large |
| Project row | Years · title · sponsor · one-line summary · report link (optional) | Compact, one per completed project |
| Publication entry | Thumbnail · title · authors · venue and year · type tag · link | Every entry has a thumbnail (section 6) |
| Person card | Photo · name · role or program · organization (boards) · link | One uniform placeholder when there is no photo |
| News/event item | Image · date · title · one or two sentences · links | Every item has an image (section 6). Items without a date sort last and show no date |
| Tag | Label | For themes and types |

Only things that can be clicked react to hover.

## 5. Writing

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

- Files in `assets/brand/`: `calplug-logo.svg` (full, for light backgrounds), `calplug-logo-reversed.svg` (for the navy footer), `calplug-mark.svg` (icon only, also the favicon).
- The SVG is a redraw of the existing logo: same icon, same blue and green, lettering set in Montserrat (open font licence) and converted to outlines. It needs the director's approval before it replaces the logo anywhere outside this site. The original PNG stays in `assets/legacy/`.
- Do not recolor, stretch or add effects. Keep clear space around it equal to the thickness of the ring.

### News images (standard)

- Every news or event item has exactly one image, shown at 3:2.
- Order of preference: a photo from the event, then the event flyer, then the default image `assets/brand/news-default.svg` (used automatically when `image` is empty).
- New images: at least 1200 by 800 pixels, JPEG, under 400 KB, in `assets/news/`.

### Publication thumbnails (standard)

- Every publication has a thumbnail in a portrait slot (letter-page proportion).
- If the entry links to a PDF, the thumbnail is the first page of that PDF, made by `tools/make_pub_thumbs.py`.
- Otherwise the slot shows the standard tile for its type (Journal, Conference, Report, In the press). No hand-made exceptions.

## 7. Motion

- Entrance: fade and 16px rise over 0.6s, once, when a section scrolls into view.
- Feedback: 0.2s for hover and press.
- Nothing else. All motion is off when the visitor's system asks for reduced motion.
- All content is visible without JavaScript.

## 8. Responsive and accessibility

- Checked widths: 1440, 1024, 820, 390, 360, 320. No horizontal scroll at any of them.
- People grid: 4 columns on desktop, 3 on tablet, 2 on phones.
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

## Open questions

- UC Irvine and Calit2 brand and web requirements (logo use, footer statements, accessibility policy) have not been checked yet.
- Research themes on the Research page are a draft grouping and need Arnold's approval.
