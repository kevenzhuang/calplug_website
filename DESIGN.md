# CalPlug Website Design Guide

Version 0.24, 2026-11-13. Status: built with Keven Zhuang, change by change; waiting for review by Arnold Wang.
Read this before changing any page, style or template. If a problem is not covered here, fix this guide first, then fix the page.

**Formats come first.** Every kind of content (a news item, a publication, a person, a project) has one format, defined here and in `MAINTAINING.md`. New content is built on these formats. When a format turns out to be wrong or incomplete, improve the format, record the change in the change log, and bring existing content up to it. No one-off exceptions on a page.

## 1. What the site is for

calplug.org is the public face of the California Plug Load Research Center (CalPlug) at UC Irvine: a research lab's site, not a company's.

| Reader | What they want | Where they go |
|---|---|---|
| Sponsors and partners | What CalPlug does, what it has delivered, who backs it, how to support it | Home, About, Research, Support |
| People curious about CalPlug | A fast, trustworthy overview and recent news | Home, About, News |
| Future students | Research, the team, how to join | Research, People, Careers |

Simple and direct: the site exists so people can find information, not to impress. If a page feels heavy, remove something; do not add decoration. No call-to-action bands ("Get in touch", "Partner with us") at the bottom of pages.

## 2. Navigation and pages

### Header

One row: the logo on the left, seven menu items, then one button. No top bar, no drop-down menus:

**Logo** · About · People · Research · Publications · News · Careers · Contact · **[Support CalPlug]**

- The logo is the link to Home; there is no "Home" item. The CalPlug icon in the footer links to Home too.
- "Support CalPlug" is the only filled button in the header (blue, white text). On phones it reads "Support" and stays next to the Menu button.
- Facilities is part of Research ("Our labs"). Contact is the last menu item, and also in the footer line and at the bottom of About.
- Below 1000px wide the seven items collapse behind a Menu button. The menu never wraps onto two rows.
- The current page is marked as in section 7 (green line on the header's bottom edge).
- There is no bar above the header. (0.12 to 0.19 had one naming UC Irvine and Calit2, first navy, then light gray; both looked like an extra strip. UC Irvine and Calit2 are named by their logos in the footer.)

### Pages

Every page starts the same way: the page title (h1) on the left, a short green line under it, then at most a two-sentence introduction (19px), then the content.

| Page | Content, top to bottom |
|---|---|
| Home | Welcome (see below) · Latest news (3 list rows) · Current projects (4 small cards) · Recent publications (3 list rows) |
| About | About CalPlug · Vision · Mission Statement · Organization Goal · Guidance · Facility · Contact. Under the About CalPlug text: the full current logo (`calplug-logo.svg`, about 360px wide), with no caption |
| People | Jump links (Team · Students · Faculty · Advisory Board · Council · Alumni) · Director and staff (photo, first two sentences of the bio, "Full bio" to open the rest) · Affiliated team · Students · Affiliated faculty · Advisory Board (+ emeriti) · Chief Technology Council (+ emeriti) · Alumni |
| Research (`research.html`) | Intro · filter by research area (draft areas, see Open questions) · Current projects (cards, two per row) · Completed projects (list rows) · Student projects |
| Research page, Our labs | Former Facilities page: intro · three cards linking to SIM Home, 1 kWh Challenge, SIM Lab (each an original page) · floor plan, folded. `facilities.html` now sends visitors here |
| Project page (`project-<id>.html`) | Title · years, sponsor, area · partners · full original description · image · reports · link back to Research. One page per project that has a description |
| Publications | Filter by type · by year, newest first · Earlier documents, folded by category |
| News (page title "News & Events") | All items, newest first · link to the Events Archive (original page with agendas and recordings) |
| Careers | Intro · deadline notice · "What you get" and "What we ask" cards · Open positions (cards: ID pill, title, one sentence, up to 3 tasks, mentors with photos) · How to apply (4 numbered steps). Content in `data/careers.json` |
| Support & Memberships | Intro · Current members (large logo tiles) · Ways to support (3 cards: member, gift, equipment) · Membership levels (3 cards: Gold, then what Platinum and Diamond add; full comparison table folded below) · Past members and current affiliates (logo tiles). Content in `data/support.json` |
| Contact (reached from the footer and About) | Original location text · photo of the Calit2 Building · address with an "Open in Google Maps" link · general, collaborations and Calit2 contacts · hours. No embedded map |

### Home welcome

- Text on the left, the group photo on the right, both aligned at the top. White background, a 1px line below.
- Text: "California Plug Load Research Center" (h1), the tagline from `data/site.json` (at most 40 words; says what CalPlug does in plain words), then three text links: About · Join us · Contact.
- About 300px high on a laptop, so the first news items are visible without scrolling.
- The photo is shown whole (not cropped), scaled to fit.

### Footer

The vision line and two short lines on the deep navy background (`--navy`), with a 3px green line on top:

0. The CalPlug icon (30px, on a 40px white disc so its blue stays visible on navy; the icon itself is unchanged), which links to Home like the header logo, then CalPlug's Vision in one line ("Energy-conscious plug and process loads for how people work, live, and play"), white Montserrat, with a faint line below.
1. On the left, the UC Irvine primary logo in white (`assets/brand/uci-logo-white.png`, 24px high, links to uci.edu), then 24px of space, then the Calit2 logo (`assets/brand/calit2-logo.png`, 40px high, links to calit2.uci.edu). This is the one place on the site that links to UC Irvine and Calit2. The two logos stand apart, never joined into one lockup. On the right, LinkedIn and Facebook icons in light gray, white on hover. The UC Irvine seal is not used (see 6. Images, Logo).
2. One line of small text in light gray: address · email · Contact · copyright. Links are white.

No site map in the footer: every page not in the menu is reached from its parent page.

## 3. Visual standard

### Color and where it is used

Blue and green are sampled from the CalPlug logo, and each has one meaning. A visitor learns it without being told:

- **Blue means "you can click this."** Nothing that cannot be clicked is blue.
- **Green means "active now" or "when".** The Active dot, dates and years, the current menu item.
- **Navy is the ground.** The footer, and quiet structure (pill text, notice line, step numbers).

| Token | Value | Used for |
|---|---|---|
| `--blue` | `#005BAA` | Links, buttons, selected filter, card border on hover, top half of ring icons |
| `--blue-dark` | `#004A8C` | Button hover |
| `--green` | `#8BC53F` | Line under the current menu item; short line under the page title; line on top of the footer; Active dot; bottom half of ring icons. Never for text (2.07:1 on white) |
| `--blue-tint` | `#EEF4FA` | Selected filter button background (with blue border and blue text) |
| `--green-text` | `#4A7A1C` | Dates and years, the word "Active", check marks in the benefits table (5.13:1 on white) |
| `--navy` | `#0E2A47` | Footer background; pill text; notice and step lines; About side headings; line icons inside rings |
| `--on-navy` | `#C5D0DC` | Text on the footer (10:1 on navy) |
| `--line-on-navy` | `#2B445D` | The divider line inside the footer |
| `--tint` | `#F6F8FA` | Image frames, pills, notice boxes, table group rows |
| `--ink` | `#1B2530` | Headings and body text |
| `--muted` | `#5B6875` | Authors, sponsors, summaries, small text |
| `--line` | `#E3E8EE` | Dividers and borders, always 1px |
| `--white` | `#FFFFFF` | Page background |

The page is white at the top and grounded at the bottom by the navy footer. (Until 0.11 the top had a 4px blue and green strip, which only repeated the logo's colors; in 0.12 to 0.18 the top bar was navy, which felt abrupt.)

Not used: gradients, shadows, colored cards, green text on white. The footer is the only dark block.

### Type

Two families, both stored on this site (`src/fonts/`, SIL Open Font License; no Google Fonts, no tracking). If they do not load, the system font is used.

| Family | Used for | Why |
|---|---|---|
| Montserrat 600 | Page title (h1), section titles (h2), step numbers, the footer vision line | UC Irvine's primary typeface, so the site matches the university; used only large, where its character shows |
| Inter 400 / 500 / 600 | Everything else | Drawn for screens; stays clear at 14px |

**Sizes.** Seven sizes, each with one job. A new size is never added for one element; pick the closest job.

| Token | Size | Job | Why this size |
|---|---|---|---|
| `--fs-h1` | 34px (28px on phones) | Page title, one per page | Clearly the largest thing on the page, still one line for most titles |
| `--fs-h2` | 24px (21px on phones) | Section title; step numbers | About 1.4 times the body, enough to scan sections |
| `--fs-lead` | 19px | The home tagline, page introductions, the footer vision line, the About quote | One step above body for the single sentence a visitor should read first |
| `--fs-h3` | 17px | Item title: a news item, project, publication, person, card | Just above body: weight, not size, makes it a title, so long lists stay calm |
| `--fs-body` | 16px | Paragraphs | Browser default; comfortable for long reading |
| `--fs-nav` | 15px | Menu items only | Between body and small so seven items fit one row down to 1000px |
| `--fs-small` | 14px | Supporting text: authors, venues, sponsors, summaries, dates, card text, buttons, footer | Clearly secondary but still readable |
| `--fs-mark` | 11px | The "PDF" mark only | A label inside a tiny box; never for sentences |

**Weights.** Three weights, by role. Weight never changes between states (section 7).

| Token | Weight | Role | Examples |
|---|---|---|---|
| `--w-text` | 400 | Running text: anything read as a sentence | Paragraphs, summaries, authors |
| `--w-label` | 500 | Labels: short text that is not a sentence and not a title | Menu items, filter buttons, Menu button, disclosure labels, dates, "About → Join us → Contact" links |
| `--w-title` | 600 | Titles and the few things that must stand out | h1 to h3, names, the Support button, pills, "Active", table headings, the address on Contact |

No 700 or heavier, no italics for emphasis, no uppercase labels, no underlines except on hover.

**Line heights.**

| Token | Value | Used for | Why |
|---|---|---|---|
| `--lh-title` | 1.25 | h1, h2 | Large text needs less space between lines |
| `--lh-snug` | 1.4 | h3, small text in cards and grids, the vision line | Short blocks of two or three lines |
| `--lh-lead` | 1.55 | Lead text | Between snug and body |
| `--lh-body` | 1.65 | Paragraphs | Generous for long reading at 720px wide |

Colors of text: ink for titles and body, muted for supporting text, blue only for links, green-text only for dates and "Active" (see Color).

### Line breaks

- Titles fit on one line on a laptop where possible. When a title must wrap, it breaks between phrases and the lines are of similar length (`text-wrap: balance`).
- A single word never sits alone on the last line of a title or a short paragraph (`text-wrap: pretty`).
- Names, dates and short fixed terms never split across lines: "UC Irvine", "CalPlug/ITAC", "May 5, 2026", "Calit2 Building". Use a non-breaking space or a no-wrap span.
- After any change to a title or layout, look at the page at 1440, 1024 and 390px wide and check each wrapped line by eye.

### Layout, spacing and shape

| Token | Value | Used for | Why |
|---|---|---|---|
| `--page` | 1080px | Page width; everything starts at the same left edge | Wide enough for the seven-item menu and three cards |
| `--text` | 720px | Maximum width of running text and list titles | About 80 characters a line, the comfortable limit |
| `--s-4` … `--s-64` | 4, 8, 12, 16, 24, 32, 48, 64px | All padding, margins and gaps | One scale, so distances repeat and things line up |
| `--header-h` | 72px | Header row height | Room for a 40px control with 16px above and below |
| `--control-h` | 40px | Height of buttons (Support, Menu) | Comfortable to tap |
| `--control-h-s` | 32px | Height of filter buttons | Smaller because they come in rows |
| `--radius` | 6px | Cards, images, buttons, notices | Soft but not round; one radius for all boxes |
| `--radius-s` | 3px | Small things: thumbnails, the PDF mark, accent lines, focus ring | 6px would look like a blob at this size |
| `--radius-pill` | fully round | Filter buttons and pills | Marks them as tags, different from buttons |
| `--t-fast`, `--t-slow` | 0.2s, 0.3s | Color changes; image zoom | Fast enough to feel instant |

How the spacing scale is used:

| Distance | Token |
|---|---|
| Between sections | 48 |
| Section title to its content | 24 |
| Between cards in a grid; between columns | 24 |
| Inside a card | 24 (16 in the small Home cards) |
| Between rows of a list | 24 above and below the line |
| Title to the text under it; between paragraphs | 4 to 16 |
| Icon to its label | 8 |

Lines: 1px `--line` for all borders and dividers; 3px for accent lines (green under the page title and current menu item, navy on notices and steps, green on top of the footer); 2px for the focus ring. Values up to 3px may be written directly (hairlines and optical nudges); everything from 4px up must be a spacing token.

Breakpoints (fixed; do not add others):

| Width | What changes |
|---|---|
| 1000px and below | Menu collapses behind the Menu button |
| 900px | Grids of 4 and 3 cards become 2; people grid 5 becomes 3; steps 4 become 2 |
| 760px | Home welcome and Contact top stack into one column |
| 600px | Phone layout: one column, smaller titles, 16px page margin |
| 480px | Header button reads "Support" |
| 360px | Smaller logo and tighter header |

### Buttons and controls

There are exactly four clickable shapes, and the same job always gets the same shape on every page. A new one is not added; a new action uses one of these.

| Control | Look | Use | Limit |
|---|---|---|---|
| Filled button | Blue fill, white 14px text at weight 600, 40px high, 6px radius, 16px side padding | The one main action of the site: "Support CalPlug" | One per page, in the header |
| Outline button | White, 1px gray border, 14px text at weight 500, 40px high, 6px radius | Menu / Close on phones | Header only |
| Pill button | Pill, 1px gray border, 14px muted text at weight 500, 32px high; may carry a ring icon | Any row of choices under a page title: filters that narrow a list (Research, Publications) and section links that jump down a long page (People) | Only in that row. A row of choices is never plain text links, so the three pages look alike |
| Text link | Blue text; "→" for a link to another page of the site, "↗" or "PDF" marks added automatically | Everything else | — |

States for each are in section 7.

### Where each rule is enforced

| Rule | Enforced by |
|---|---|
| Colors, sizes, weights, line heights, radii, durations and spacing come from tokens | `tools/check.py` reads the stylesheet and stops the build on a raw value |
| Text length limits | `tools/build.py` stops the build |
| Bullet rules; cards in a row have one shape | `tools/check.py` |
| Links, image alt text, one h1, no placeholder text, no empty sections | `tools/check.py` |
| Alignment, line breaks, photos, overall look | A person, with the checklist in section 9 |

**Tracing a change.** Every visual decision has a row in this guide: the token tables above (what value and why), section 4 (which component), section 5 (how text is written and formatted), section 7 (how it reacts). A change that cannot point to a row adds the row first, with its reason, and a line in the change log.

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
| Pill | Short navy label on the tint, thin border | Position IDs, membership levels |
| Notice | One sentence on the tint with a 3px navy left line | Deadlines. At most one per page |
| Steps | Numbered columns with a navy top line | How to apply |
| Filter | Round buttons | Publications by type, Research by research area |
| Disclosure | Blue label with a chevron, closed by default (section 7) | "Full bio", "Compare all benefits", Earlier documents, floor plan |
| Social icon | Single-color icon with a hidden text label | LinkedIn, Facebook, in the footer. White on hover |
| Header button | Blue fill, white text | "Support CalPlug" only |
| Footer vision line | CalPlug's Vision from About, in quotes, Montserrat, white, above the logos with a faint line below | Every page. Text comes from `vision` in `data/site.json`; never replaced by a slogan |
| Ring icon | A ring with the logo's own proportions (inner radius 74% of the outer, split on the horizontal, blue above, green below) around a line icon in the logo's blue with round ends, the same weight as the logo's arcs (22px; 20px on filter buttons) | Research areas: on the filter buttons and on project cards. Icons: plug (plug loads), person (user behavior), factory (smart manufacturing), bolt (grid and storage), building (buildings and data centers), calendar (default news image). Drawn in `tools/build.py` (`LINE_ICONS`); never add a second icon style |
| Active dot | Green dot + "Active" in green text | Meta line of active projects |
| Link marks | "PDF" in a small outlined box after links to PDF files; "↗" after links that leave the site | Lists, cards, copied pages. Added by CSS from the link address, never typed into data |

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

### Headings and link words

- Page titles and menu items: title case, as names of pages ("News & Events", "Support & Memberships").
- Section titles and card titles: sentence case ("Latest news", "Student researchers", "Affiliated faculty"). Names of bodies keep their capitals ("Advisory Board", "Chief Technology Council").
- Headings go down one level at a time (h1, h2, h3). Where a page has cards directly under its title, a section title is still present for screen readers. Copied pages keep their own headings.
- One word per action, everywhere: "Read" for a publication, "Details" for a project page, "Read more" for a lab page, "All ..." for a full list. The mark after the word (→, ↗, PDF) says where it leads.

### Bullets, numbers, labels or sentences

The format follows from what the content is, never from habit or from what looks busy. Before writing any text, ask these questions in order and stop at the first "yes":

1. **Do the parts happen in a fixed order?** → numbered steps.
2. **Is each part a name with a value** (phone, date, room, audience, sponsor)? → label / value rows. No bullets, no colons.
3. **Is each part a link to a document?** → a plain list, one link per row, a line between rows. No bullets.
4. **Are there three or more parts that are parallel, short (about one line each) and make sense on their own**, so a reader scans them and might use only one? → a bullet list.
5. **Otherwise** (one or two items, or ideas that lean on each other with "because", "so", "which") → sentences in a paragraph.

Two rules make the site look consistent rather than random:

- **Same kind of content, same format, everywhere.** If one position card lists its tasks as bullets, every position card does. If one membership level is a lead-in line and a list, every level is. Cards side by side never mix a list in one with plain text in another.
- **A list never stands alone.** It is introduced by a heading ("What you get") or a lead-in line ending in a colon ("Everything in Gold, plus:"), never by a sentence fragment like "Why:".

Inside a bullet list:
- Every item has the same grammar: all short phrases or all full sentences.
- Phrases: capital first letter, no period ("Workspace, supplies and equipment"). Full sentences: each ends with a period.
- One idea per item, about one line; at most about six items. More than six: split under small headings or use a table.
- No nested lists, except agendas copied from the old site.
- Size: bullets inside cards use the small text size (14px); bullets in page text use the body size (16px). The marker is always a plain dot.

**Where each format is used now** (keep it this way; a new page copies the closest row):

| Place | Format | Why |
|---|---|---|
| About: About CalPlug, Mission, Goal, Guidance, Facility | Paragraphs | Explanations whose sentences depend on each other |
| About: Vision | Quote, then 3 bullets (full sentences) | Three separate goals, each stands alone |
| Project pages, bios | Paragraphs | Original descriptions, continuous text |
| Project cards, news, publications | One sentence or none, no bullets | A list row or card carries one summary |
| Careers: What you get / What we ask | Bullets (phrases) | Parallel conditions, scanned and compared |
| Careers: each position | One sentence, then 3 task bullets (phrases), then mentors | Same shape in every position card |
| Careers: How to apply | Numbered steps | Done in order |
| Support: Ways to support | One or two sentences per card, no bullets | Each card is a single action |
| Support: Membership levels | A lead-in line, then bullets (phrases), in every level | Same shape in every level card |
| Support: full benefits table | Table with check marks | Many items compared across three levels |
| Contact cards, 1 kWh Challenge design, webinar details | Label / value rows | Names with values |
| Student projects, Earlier documents | Plain link list | Each row is a document |
| Events Archive agendas (copied) | Bullets, nested where the original nests | Time-ordered program, kept as published |

`tools/check.py` stops the build when a list has one item, when a list mixes sentences and phrases, and when cards in one row mix lists and plain text.

## 6. Images

### Logo

- Vector logo files (`assets/brand/`, copies in `brand-kit/logos/`):
  - `calplug-logo.svg`: the current full logo, traced with `tools/trace_logo.py` from the largest copy on the old site (`calpluglogo2022.jpg`, 1187 px). Lettering is the original's shapes, not a font.
  - `calplug-logo-compact.svg`: the icon (`calplug-mark.svg`) and the traced CALPLUG wordmark, laid out like the earlier `calplug-logo-compact.png`. Used in the header (about 40px high).
  - When the designer's original vector files are found, they replace these files under the same names.
- The icon alone (`assets/brand/calplug-mark.svg`): redrawn as a vector by measuring the original logo file (ring outer and inner radius, horizontal split, the three arcs' centers, radii and widths, the plug's prongs and body); checked against the original pixel by pixel, differences are only at anti-aliased edges. Used for the browser tab icon, the 404 page and the default news and publication images. Never altered (no "unplugged" variant, no recoloring).
- Replace these only with a higher-resolution or vector copy of the same artwork from the lab.
- UC Irvine logo: the primary logo file Keven Zhuang provided (`assets/brand/uci-logo.png`, 266×45). Keep the clear space around it; nothing locked up with it; not smaller than 3/16 inch (about 18px); never redrawn or recolored. A larger or vector copy from the UC Irvine brand asset library (UCInetID login) would look sharper on high-resolution screens; swap it in when available.
- UC Irvine seal: not used. UC Irvine's brand rules say the seal should not be used on the web and cannot be modified; questions go to graphicservices@uci.edu.
- Calit2 logo: the file Keven Zhuang provided (`assets/brand/calit2-logo.png`, square). Shown as is, at 40px high, with a little space from the UC Irvine name; never recolored or redrawn.

### File size and loading

- No image on a page is over 400 KB (the build stops otherwise). `tools/optimize_images.py` writes a smaller copy of every large image to `assets/opt/` (longest side 1000px); originals are kept and the site serves the copy.
- Images hosted on other sites are copied into `assets/ext/` by the "Import images only" workflow; the site never depends on another site's image address.
- Every image tag carries its pixel width and height, written by the build, so the page does not jump while images load.
- Images below the first screen load only when scrolled to.

### No cropping

- Photos, flyers, diagrams and first pages are never cropped. Each kind has one frame shape; the whole image is fitted inside it on a neutral background.
- The welcome photo, the Contact building photo (`assets/site/calit2-building.jpg`), and the director and staff photos are shown at their own proportions.

### People photos

- The people grid uses square frames so it stays even. The square is taken from the top of the photo so the head and shoulders are always fully visible.
- Every photo is checked by eye after it is added. If a face is cut, set `photo_position` for that person in `data/people.json` (for example `"center 20%"`) instead of changing the rule.
- Best: people supply square portraits, at least 600 by 600 pixels.
- No photo: one uniform placeholder with the person's initials.

### Share image

- When a page is shared (WeChat, LinkedIn, Slack, email), the preview shows `assets/brand/share.png` (1200×630): the full CalPlug logo, one line on what CalPlug does, a large ring, and the navy band with the UC Irvine and Calit2 logos and "calplug.org".
- A project page shares its own image instead.
- Source: `tools/share/share.html`; rebuild with `python tools/make_share_image.py` after changing it.
- Share links are absolute, built from `site_url` in `data/site.json`. Change `site_url` when the site moves to calplug.org.

### 404 page

- `404.html`: the CalPlug icon, "This page is unplugged.", one sentence, and links to Home, Research, Publications and Contact. It uses `site_url` as its base so it works at any address.

### Ring icons and default images

- The default news image (`assets/brand/news-default.svg`) is the CalPlug icon on the tint background; the default publication image carries it small.
- Large ring decorations (share image, slide and flyer templates) use the logo's ring with its own thickness, never a thinner look-alike.
- The UC Irvine logo on the navy footer is the white one-color version (`assets/brand/uci-logo-white.png`), made from the provided file by turning its color white without changing its shape. Replace with the official reversed file when available.

### News images

- Every item has one image, fitted whole into a 3:2 frame.
- Order of preference: a photo from the event, the event flyer, then the default ring image.
- New images: at least 1200 by 800 pixels, JPEG, under 400 KB, in `assets/news/`.

### Publication thumbnails

- `tools/make_pub_thumbs.py` tries, in order: the first page of the linked PDF; the first page of a PDF named on the linked page; the linked page's preview image.
- Otherwise the one default image `assets/brand/pub-default.svg`. No colored tiles.

## 7. Interaction and motion

The rules for how the site responds to people. Every interactive element below has one look per state; a new element reuses one of these patterns or this section is changed first.

### Principles

1. **Looks clickable only if it is.** Blue text, a button shape, an underline on hover or a pointer cursor only on things that do something. Nothing else reacts to the mouse.
2. **One pattern per job.** Going somewhere is a link; showing more on the same page is a disclosure; narrowing a list is a filter button; the one call to action is the header button. They never swap roles.
3. **Quiet feedback.** Changes of color and border, at most a 2% image zoom. No pop-ups, carousels, auto-play, parallax, entrance or scroll animations.
4. **Everything works without a mouse and without JavaScript.** Keyboard reaches everything in reading order; with JavaScript off all content is visible, the menu shows as a wrapped row and filters show everything.

### States

| Element | Default | Hover | Keyboard focus | Pressed / open | Current |
|---|---|---|---|---|---|
| Text link | Blue | Underline (3px below the text) | 2px blue ring, 3px gap | — | — |
| Link on navy (footer) | Light gray or white | White, underline | 2px white ring | — | — |
| Menu item | Ink | Blue | Ring | — | Blue text and a 3px green line on the header's bottom edge (the link fills the header height, so the line sits on the edge, not under the word). Phones: blue text and a short green bar in the left margin; the text does not move |
| Header button "Support CalPlug" | Blue fill, white text, 40px high, text centered on the same line as the menu | Darker blue (`--blue-dark`) | Ring | Navy | Navy fill (flat; nothing added around it) |
| Menu button (phones) | Gray border, "Menu" | Blue border and text | Ring | Blue border and text, reads "Close" | — |
| Filter button | Gray border, muted text (weight 500), round, at least 32px high | Blue border and text | Ring | Light blue fill, blue border, blue text, same weight (`aria-pressed`) | — |
| Card with a link | Gray border | Blue border, image grows 2% (only on devices with a mouse) | Ring on the title link | — | — |
| Disclosure ("Full bio", "Compare all benefits", Earlier documents) | Blue label, chevron pointing right | Underline | Ring | Chevron points down, content below | — |
| Logo tile, person, Active dot, pill | No reaction | — | — | — | — |

Visited links look the same as unvisited ones. Disabled states do not exist: an action that cannot be used is not shown.

**Nothing changes size between states.** Hover, pressed and current states change color, fill or border only, never font weight, padding or text position, so a row of buttons or menu items never shifts when one is selected.

### Links

- Links open in the same tab, including links to other sites and PDFs; the visitor decides. No `target="_blank"`.
- After a link that leaves the site: a small "↗". After a link to a PDF: a small outlined "PDF". Both are added by CSS from the address, never typed into data, and never added to buttons or to "→" links.
- "→" links (`.more`): moves to another page of this site ("All news and events", "Details"). The arrow is part of the link.
- Link text says where it goes ("Read", "Slides", "Open in Google Maps"), never "click here".
- UC Irvine and Calit2 are linked once, by their logos in the footer.

### Navigation

- Wide screens: seven menu items and the header button in one row. Below 1000px: the items move behind the Menu button; the header button stays visible ("Support" on phones).
- The open menu drops below the header, full width, one item per row, each row about 48px high. It closes with the Close button, the Escape key (focus returns to the button), or a click outside it.
- Every page starts with a hidden "Skip to content" link that appears on keyboard focus.
- Section links (People: Team, Students, ...) are pill buttons like filters, but they jump to a section instead of hiding items, so they have no selected state. They jump straight there, without smooth scrolling.

### Filters

- Filter buttons narrow a list on the same page; "All" is first and selected at the start. One selection at a time.
- Hidden items are hidden whole; a group (a year, "Completed projects") whose items are all hidden is hidden too.
- The number of items shown is announced to screen readers ("2 shown").
- Phones: the buttons stay on one line and scroll sideways instead of wrapping.

### Disclosures

- For text most readers skip: the rest of a bio, the full benefits table, old document lists, the floor plan. Closed by default.
- The label says what opens ("Full bio", "Compare all benefits", "Floor plan of the CalPlug space").
- Built on the HTML `details` element, so it works without JavaScript and with the keyboard (Enter or Space).

### Touch and sizes

- Anything tappable is at least 32px high (buttons 40px); text links inside sentences are the exception.
- No action depends on hover: hover only adds feedback. Image zoom on cards is turned off on touch screens.

### Motion

- Color, border and background changes: 0.2s. Card image zoom: 0.3s. Chevron turn: 0.2s.
- All of it is off when the visitor's system asks for reduced motion.
- Nothing moves on its own: no carousels, tickers, auto-playing video or animated counters.

## 8. Responsive and accessibility

- Checked widths: 1440, 1024, 820, 390, 320. No horizontal scroll at any width.
- Every link, button and icon is reachable by keyboard and has a visible focus ring and a text label (section 7).
- Icons that only decorate are hidden from screen readers (`aria-hidden`); icons that act (social links) have a hidden text label.
- Language of the page is set (`lang="en"`); the current menu item carries `aria-current="page"`; the menu button carries `aria-expanded`; filter buttons carry `aria-pressed`.
- One h1 per page; headings do not skip levels. Every image has alt text; decorative images use empty alt.
- Text contrast at least 4.5:1.

## 9. Checks before publishing

1. `python tools/build.py` builds without errors.
2. `python tools/check.py` passes (links, alt text, placeholder text, empty sections, one h1).
3. Screenshots at 1440, 1024 and 390 look right, including line breaks (section 3) and people photos (section 6). A passing script does not mean the page looks good. Look at every page, and check in particular:
   - **Alignment across cards.** Cards side by side have the same parts in the same order, so their rows line up (Contact: Phone, Email, Web, Contact; team cards: email at the bottom). Titles short enough to fit one line.
   - **Labels and values.** Facts are shown as label / value rows with one fixed label width, not as sentences ("Phone: ...").
   - **Separators.** A " · " never starts a line: keep separated items in no-wrap pieces, or put them on their own lines on phones.
   - **No half sentences.** Text is never cut with "..." to fit a box; shorten it or leave it out.
   - **Copied pages.** No one-item bullet lists holding a paragraph, no line breaks inside links, spelling fixed, a link back to the parent page.
   - **Circles.** The ring appears only where it means something (the logo, research areas). Do not add it as page decoration.
4. Anything new that this guide does not cover has been added to this guide.

## 10. Brand kit

Everything CalPlug shows outside the website (slides, flyers, posters) follows the same rules, so the lab looks like one place everywhere. The kit is the folder `brand-kit/`, with a one-page guide (`brand-kit/README.md`):

- `calplug-slides-template.pptx`: cover (logo, title, large ring, navy band with UC Irvine and Calit2), section divider (navy), content slide (title, text, small logo, slide number).
- `calplug-flyer-template.pptx`: US Letter portrait event flyer (label, title, date and place, one picture, two or three sentences, navy band).
- Logos (CalPlug full, compact, icon; UC Irvine blue and white; Calit2), the share image, and the fonts (Montserrat, Inter; SIL Open Font License).
- Rules: same colors and meanings as section 3; titles Montserrat bold, text Inter (Arial if missing); logos never redrawn, recolored, stretched or joined; the ring is the only decoration, once per page; real photos, no stock.
- `brand-kit/source/make_templates.js` rebuilds the templates. Change the templates there, not by hand, so this guide and the files stay in step.

## 11. Change log

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
| 0.24 | 2026-11-13 | Footer: the CalPlug icon before the vision line, linking to Home. |
| 0.23 | 2026-11-13 | Second audit. Performance: People page images cut from 18 MB to 3.7 MB with optimized copies; three images hot-linked from other sites are now stored here; image tags carry width and height. Structure: no skipped heading levels on built pages. Wording: one capitalization rule for headings ("Affiliated faculty"), one word per action ("Read" for every publication; "Details →" in project rows). Build checks added for heading order and image size. |
| 0.22 | 2026-11-13 | People: the section links under the title were plain blue links while Research and Publications had pill buttons in the same place; they are now pill buttons too (rule: a row of choices under a page title is always pills). Director and staff: email on its own line, so a " · " no longer starts a line on phones. Filter buttons without an icon have even padding. |
| 0.21 | 2026-11-13 | Full audit of the stylesheet against this guide. Every font size, weight, line height, radius, duration and spacing value is now a named token with a stated job and reason (section 3: Type; Layout, spacing and shape; Buttons and controls). Found and removed: two unnamed font sizes, three unnamed line heights, two radii, 6px / 10px / 22px gaps outside the scale, a translucent line color, an unused style. `tools/check.py` now reads the stylesheet and stops the build on any raw value. Added the table of where each rule is enforced and the rule for tracing a change. |
| 0.20 | 2026-11-13 | Top bar removed. Contact back in the menu as the last item; the footer logos link to UC Irvine and Calit2 again (the only place). Bullet standard rewritten as five questions in order, two consistency rules, and a table of every place on the site and its format. Membership levels: the Gold card now has the same lead-in and list as Platinum and Diamond. The build also stops when cards in one row mix lists and plain text. |
| 0.19 | 2026-11-13 | Top bar changed to option B: light gray with a line below, muted text, blue on hover; navy stays only in the footer. About shows one full current logo, no captions. Earlier logo dropped (the trace was too rough and its typeface could not be identified). |
| 0.18 | 2026-11-13 | Filter buttons keep one font weight when selected, so the row no longer jumps. Current menu item: the green line now sits on the header's bottom edge; phones mark it with a bar in the margin instead of indenting the text; the header button's current state is a flat navy fill instead of a green edge that looked raised. Rule added: states never change size. Logos on About moved under the About CalPlug text. Earlier wordmark-only SVG added. |
| 0.17 | 2026-11-13 | Bullet standard (section 5): when to use paragraphs, bullets, numbered steps, label / value rows or plain link lists, and the grammar inside a list; the build checks one-item lists and mixed lists. Fixed: About Vision endings, 1 kWh Challenge ("Why:" and the design list), the webinar details in the Events Archive (now label / value rows). Vector logos: current full logo, compact header logo and earlier logo, traced with the new `tools/trace_logo.py`; the header uses the SVG. About shows the current and earlier logo. Fixed: the header button had lost the space in "Support CalPlug". |
| 0.16 | 2026-11-13 | Section 7 rewritten as the interaction standard: principles, a state table for every interactive element, and rules for links, navigation, filters, disclosures, touch sizes and motion. Code brought in line: one disclosure style with a chevron (Earlier documents are blue like other disclosures), Menu button reads Close when open and closes with Escape or a click outside, pressed states for buttons, filter results announced to screen readers, card zoom only on devices with a mouse, minimum target sizes. |
| 0.15 | 2026-11-13 | Page icons removed (too many circles: the logo, then a ring by every title). Full visual review: Contact cards rebuilt as short titles with aligned label / value rows (Phone, Email, Web, Contact) and the Calit2 spelling fixed; footer address on its own line and no separator at a line start; affiliated team emails aligned; Home project cards without cut-off summaries; Careers research areas never split; copied pages: one-item lists turned into paragraphs, line breaks inside links removed, typos fixed, back links added; list titles kept to the text width; filter buttons scroll sideways on phones instead of wrapping into four rows. Review checklist added to section 9. |
| 0.14 | 2026-11-13 | CalPlug icon redrawn to the original logo's measurements; it replaces the look-alike in the tab icon, About, 404 and default images. Ring icons rebuilt with the logo's ring proportions and blue line icons. Selected filter is now light blue with a blue border so the ring stays visible. Footer logos are no longer links (the top bar is the one link out). Share image and templates use the true ring. |
| 0.13 | 2026-11-13 | Page icons: each page title has its ring icon on the left (fixed size and place on every page). CalPlug's Vision as one line at the top of the footer. |
| 0.12.1 | 2026-11-13 | Page-title arcs removed: the title areas differ in height, so each page showed a different, cut-off piece of the arcs and it looked like a broken image. |
| 0.12 | 2026-11-13 | Top color strip replaced by a navy top bar ("University of California, Irvine › Calit2", Contact). Faint signal arcs in page-title areas. Share image and share tags on every page (project pages use their own image); `site_url` added. 404 page "This page is unplugged." Brand kit (section 10): slide and flyer templates, logos, fonts, rules. |
| 0.11 | 2026-11-13 | Approved proposals 1, 2B, 3, 4, 7: menu cut from ten items to six plus a "Support CalPlug" button (logo goes home; Facilities becomes "Our labs" on Research; Contact moves to the footer and About; Projects renamed Research, News & Events shortened to News). Colors given meanings: blue = clickable, green = active / when, navy = ground; navy footer with white UC Irvine logo; green line only under page titles. Montserrat (titles) and Inter (text), self-hosted. Ring icons for research areas and the default news image; Active dot. PDF and external-link marks; card hover. |
| 0.10 | 2026-11-13 | After Keven's review ("too much text, no standard; Publications is the cleanest"): three building blocks (list row, card, logo tile) and length limits for every piece of text, checked by the build. Home welcome is white with a new plain tagline; Home projects as cards. Projects: research-area filter (draft), current projects as cards, completed projects as list rows, one page per project with the full text. Careers and Support rebuilt from data files with cards, pills, a deadline notice, numbered steps, membership levels (benefits table retyped from the old image) and logo tiles. People bios shortened with "Full bio". About logo removed. |
| 0.9.3 | 2026-11-13 | Footer: UC Irvine primary logo (file from Keven Zhuang) replaces the "UC Irvine" text, set apart from the Calit2 logo. |
| 0.9.2 | 2026-11-13 | Footer: Calit2 logo added (file from Keven Zhuang) next to the "UC Irvine" text. UC Irvine seal not used, following UC Irvine's rule that the seal is not for the web. |
| 0.9.1 | 2026-11-12 | Built. Page width 1080px so the ten-item menu fits; menu collapses below 1080px. Footer follows UC Irvine's rule: one UC Irvine logo plus "Calit2" in text, not two logos. |
| 0.9 | 2026-11-12 | Agreed plan after a point-by-point review: welcome band text left and photo right at about 300px so news shows on the first screen; 10-item menu including Careers and Support; compact logo; blue and green used in a top strip, title lines, current-menu line, welcome band and footer line; two-line footer with UC Irvine and Calit2 logos and social icons; line-break rules; people photos squared from the top and checked by eye; project filter removed; Contact with building photo and map link, no embedded map. |

## Open questions

- The designer's original vector files of the logo (the SVGs here are traced from bitmaps). The earlier logo is not used: its wordmark is custom lettering and its small text a serif in small capitals that could not be identified from the only copy (a 700 px screenshot), and a trace of it was too rough to publish.

- A larger or vector copy of the UC Irvine primary logo, for sharper display (optional).
- Research areas for the Research filter are a draft (`data/projects.json`, `themes`), for Arnold to approve.
- All text written or shortened for 0.10 (see `CONTENT-NOTES.md`), for Arnold to approve.
