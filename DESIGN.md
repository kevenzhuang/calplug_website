# CalPlug Website Design Guide

Version 0.17, 2026-11-13. Status: built after Keven Zhuang approved the top bar (B), share image, 404 page, page-title arcs and brand kit.
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

Two rows:

1. **Top bar** (32px, navy): "University of California, Irvine › Calit2" on the left (links to uci.edu and calit2.uci.edu; "UC Irvine › Calit2" on phones), "Contact" on the right. Light gray text, white on hover. It tells every visitor at once that CalPlug is a UC Irvine research center, and pairs with the navy footer.
2. **Main row**: the logo on the left, six menu items, then one button. No drop-down menus:

**Logo** · About · People · Research · Publications · News · Careers · **[Support CalPlug]**

- The logo is the link to Home; there is no "Home" item.
- "Support CalPlug" is the only filled button in the header (blue, white text). On phones it reads "Support" and stays next to the Menu button.
- Contact is not in the menu: it is in the top bar, the footer line and at the bottom of About. Facilities is part of Research ("Our labs").
- Below 1000px wide the six items collapse behind a Menu button. The menu never wraps onto two rows.
- The current page is marked with a short green line under its menu item (on the button: a green line inside its bottom edge).

### Pages

Every page starts the same way: the page title (h1) on the left, a short green line under it, then at most a two-sentence introduction (19px), then the content.

| Page | Content, top to bottom |
|---|---|
| Home | Welcome (see below) · Latest news (3 list rows) · Current projects (4 small cards) · Recent publications (3 list rows) |
| About | About CalPlug · Vision · Mission Statement · Organization Goal · Guidance · Facility · Our logo (current and earlier logo side by side, each whole in the same white frame, with a caption) · Contact (address, phone, email, link to Contact) (original text; small heading on the left, text on the right) |
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

0. CalPlug's Vision in one line ("Energy-conscious plug and process loads for how people work, live, and play"), white Montserrat, with a faint line below.
1. On the left, the UC Irvine primary logo in white (`assets/brand/uci-logo-white.png`, 24px high), then 24px of space, then the Calit2 logo (`assets/brand/calit2-logo.png`, 40px high). The footer logos are a signature only and are not links: the top bar is the one place that links to UC Irvine and Calit2, so visitors are not sent away twice. The two logos stand apart, never joined into one lockup. On the right, LinkedIn and Facebook icons in light gray, white on hover. The UC Irvine seal is not used (see 6. Images, Logo).
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
| `--navy` | `#0E2A47` | Top bar and footer backgrounds; pill text; notice and step lines; About side headings; line icons inside rings |
| `--on-navy` | `#C5D0DC` | Text on the footer (10:1 on navy) |
| `--tint` | `#F6F8FA` | Image frames, pills, notice boxes, table group rows |
| `--ink` | `#1B2530` | Headings and body text |
| `--muted` | `#5B6875` | Authors, sponsors, summaries, small text |
| `--line` | `#E3E8EE` | Dividers and borders, always 1px |
| `--white` | `#FFFFFF` | Page background |

The page is framed by navy: the top bar above, the footer below. (Until 0.11 the top had a 4px blue and green strip; it was replaced because it only repeated the logo's colors right next to the logo.)

Not used: gradients, shadows, colored cards, green text on white. The footer is the only dark block.

### Type hierarchy

Two families, both stored on this site (`src/fonts/`, SIL Open Font License; no Google Fonts, no tracking):

- **Montserrat 600** for the page title (h1) and section titles (h2). It is UC Irvine's primary typeface, so the site matches the university.
- **Inter** (400 text, 500 menu, 600 item titles and labels) for everything else. Clear on screens at small sizes.

If the fonts do not load, the system font is used.

| Level | Size | Color | Used for |
|---|---|---|---|
| Page title (h1) | 34px (28px on phones), Montserrat, green line below | ink | One per page |
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

### Bullets, numbers, labels or sentences

Choose by what the content is, never by habit. `tools/check.py` stops the build on the two most common mistakes (marked ✓).

| Content | Format | Example on the site |
|---|---|---|
| A thought, an explanation, anything whose parts depend on each other | Sentences in a paragraph. No bullets | About CalPlug, project descriptions, bios |
| Three or more parallel items, each short and read on its own | Bullet list | What you get / What we ask (Careers), tasks of a position, Vision |
| Steps that happen in order | Numbered steps | How to apply |
| Facts with a name and a value (phone, date, room, audience) | Label / value rows, no bullets, no colons | Contact cards, 1 kWh Challenge design |
| Two items | A sentence ("A and B"), not a list | — |
| One item | A sentence. ✓ Never a one-item list | — |
| Items that are links to documents | A plain list with lines between rows (no bullets) | Student projects, Earlier documents |

Rules inside a bullet list:
- Every item has the same grammar: all short phrases or all full sentences. ✓ Never mixed.
- Phrases: capital first letter, no period at the end ("Workspace, supplies and equipment"). Full sentences: a period at the end of each.
- One idea per item, about one line; at most about six items. Longer lists become a table or are split under small headings.
- A list is introduced by a heading or a short lead-in, not by a colon after a sentence fragment ("Why:"); copied pages are corrected to a small heading.
- No bullets inside cards that hold a single sentence, no nested lists except in copied agendas.

## 6. Images

### Logo

- Vector logo files (`assets/brand/`, copies in `brand-kit/logos/`):
  - `calplug-logo.svg`: the current full logo, traced with `tools/trace_logo.py` from the largest copy on the old site (`calpluglogo2022.jpg`, 1187 px). Lettering is the original's shapes, not a font.
  - `calplug-logo-compact.svg`: the icon (`calplug-mark.svg`) and the traced CALPLUG wordmark, laid out like the earlier `calplug-logo-compact.png`. Used in the header (about 40px high).
  - `calplug-logo-earlier.svg`: the earlier logo, traced from a 700 px screenshot (`calplug-logo-earlier-source.png`). The large letters are faithful; the small text is approximate.
  - When the designer's original vector files are found, they replace these files under the same names.
- The icon alone (`assets/brand/calplug-mark.svg`): redrawn as a vector by measuring the original logo file (ring outer and inner radius, horizontal split, the three arcs' centers, radii and widths, the plug's prongs and body); checked against the original pixel by pixel, differences are only at anti-aliased edges. Used for the browser tab icon, the 404 page and the default news and publication images. Never altered (no "unplugged" variant, no recoloring).
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
| Link on navy (top bar, footer) | Light gray or white | White, underline | 2px white ring | — | Top bar "Contact": white on the Contact page |
| Menu item | Ink | Blue | Ring | — | Blue text, green line under it (on phones: green bar on the left) |
| Header button "Support CalPlug" | Blue fill, white text, 40px high | Darker blue (`--blue-dark`) | Ring | Navy | Green line inside the bottom edge |
| Menu button (phones) | Gray border, "Menu" | Blue border and text | Ring | Blue border and text, reads "Close" | — |
| Filter button | Gray border, muted text, round, at least 32px high | Blue border and text | Ring | Light blue fill, blue border, blue bold text (`aria-pressed`) | — |
| Card with a link | Gray border | Blue border, image grows 2% (only on devices with a mouse) | Ring on the title link | — | — |
| Disclosure ("Full bio", "Compare all benefits", Earlier documents) | Blue label, chevron pointing right | Underline | Ring | Chevron points down, content below | — |
| Logo tile, person, Active dot, pill | No reaction | — | — | — | — |

Visited links look the same as unvisited ones. Disabled states do not exist: an action that cannot be used is not shown.

### Links

- Links open in the same tab, including links to other sites and PDFs; the visitor decides. No `target="_blank"`.
- After a link that leaves the site: a small "↗". After a link to a PDF: a small outlined "PDF". Both are added by CSS from the address, never typed into data, and never added to buttons or to "→" links.
- "→" links (`.more`): moves to another page of this site ("All news and events", "Details"). The arrow is part of the link.
- Link text says where it goes ("Read", "Slides", "Open in Google Maps"), never "click here".
- UC Irvine and Calit2 are linked once, in the top bar. The footer logos are not links.

### Navigation

- Wide screens: six menu items and the header button in one row. Below 1000px: the items move behind the Menu button; the header button stays visible ("Support" on phones).
- The open menu drops below the header, full width, one item per row, each row about 48px high. It closes with the Close button, the Escape key (focus returns to the button), or a click outside it.
- Every page starts with a hidden "Skip to content" link that appears on keyboard focus.
- Jump links (People: Team, Students, ...) and "#labs"-style links jump straight to the section, without smooth scrolling.

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

- The designer's original vector files of the current and earlier logos (the SVGs here are traced from bitmaps).
- Top bar: the navy bar feels abrupt to Keven; options under discussion (keep navy, light gray, or remove).

- A larger or vector copy of the UC Irvine primary logo, for sharper display (optional).
- Research areas for the Research filter are a draft (`data/projects.json`, `themes`), for Arnold to approve.
- All text written or shortened for 0.10 (see `CONTENT-NOTES.md`), for Arnold to approve.
