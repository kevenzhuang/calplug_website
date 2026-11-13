# Content notes

Working notes for maintainers. Not published. Source: calplug.org as read on 2026-11-12.

## What was extracted

| File | Content | Count |
|---|---|---|
| `data/site.json` | Name, mission, vision, facility, contact | n/a |
| `data/projects.json` | Projects | 4 active, 18 completed, 9 student project documents |
| `data/publications.json` | Publications | 20 journal, 13 conference, 21 reports, 7 press; 30 older undated documents |
| `data/people.json` | People | Director, 1 staff, 3 affiliated team, 17 students, 3 alumni, 9 affiliated faculty, 13 + 14 advisory board, 8 + 4 technology council |
| `data/events.json` | Events | 12 |
| `data/partners.json` | Members, affiliates, support, join us, facilities | n/a |

## Corrections already applied

| Where | On the current site | In the data | Why it is safe |
|---|---|---|---|
| Projects | "Opimization", "Sponser", "Edision", "Commision", "adopption" | Spelled correctly | Typos |
| Team: Daniel Ceja / Aryaman Tyagi | Photos swapped | Each name uses the photo file that carries that name | File names `Daniel-Ceja.jpg` and `Aryaman-Tyagi-scaled.jpeg` |
| Team: Chelsea Choudhary email | Same address as Sergio Gago-Masague | `ccchoudh@uci.edu` | That address is on the site's own Careers page |
| Team: Shelly Nazarenus email | Text says calit2.uci.edu, link says calit.uci.edu | `snaz@calit2.uci.edu` | Link typo |
| Team: G. P. Li | "serves as director of Calit2 from 2007 to 2025" | "served as director ... from 2007 to 2025" | Calit2 announced a new director effective July 1, 2025 |
| Affiliates | "emebrtec", "Emebrtec" | "Embertec" | Typo; logo file is named embertech |
| Events | Better Buildings webinar listed twice | Listed once | Duplicate |
| Publications | 2021 DOE survey report listed under Journal | Moved to reports | It is a prepared-for report |

## To confirm with Arnold (kept off the site until confirmed)

1. LADWP COVID-19 project: the description is a copy of the CESMII survey text. Need the right description.
2. Computer Power Management Usage Survey: the report link opens the Set-Top Box report. Need the right file (the CEC link is marked 404 on the site).
3. Workshop #19 and 10th Anniversary: shown as October 18, 2021, the same date as Workshop #18; the slides page is dated May 2022. Need the real date.
4. Workshop Series #24, Battery Plugin Workshop, Earth Day Workshop: no dates or descriptions.
5. PLETICS report: cited as 2026, but the CEC number is CEC-500-2025-018. Which year?
6. ACEEE Industry Summer Study paper: listed as "forthcoming" with a 2018 link; the event was July 2021.
7. Student posters: "Experimental Test of Energy Annoyance Thresholds" opens the PMUI 5.0 poster file.
8. AI-TES and Occupancy-based Lighting: no sponsor or years shown.
9. Edge Data Center project: the current text states "25-35% total facility energy savings". Left out of the new summary because it is a target, not a measured result.
10. 1 kWh Challenge: "on hold due to Covid restrictions". Still on hold, or ended?
11. Join us: positions and deadline are for Spring 2026.
12. Advisory board and council lists: are titles and affiliations current?
13. Research themes: draft grouping in `data/projects.json`.

## Permissions needed before launch

- Photos and LinkedIn links of students and alumni: each person confirms.
- Photos of advisory board and council members: source unknown.

## Images carried over from the old site (decision 2026-11-12: reuse is fine for now)

| Image | Note |
|---|---|
| AI-TES figure (f1000research-files.f1000.com) | Still hot-linked from a journal site; will break if that site moves it |
| Edge Data Center image (assets.belden.com) | Still hot-linked from a company site |
| `pexels-singkham-...jpg`, `solar-energy.png` (Freepik) | Stock images; Freepik asks for attribution |
| Member and affiliate logos | 7 of 12 logos are used; `images.png`, `images-3.png`, `california-utilities-logo.jpg`, PG&E and Embertec logos were left out because the file-to-organization match is unclear |

## Images to replace when better ones arrive

- Hero photo (`zotwatt-2.jpg`, 647px wide): needs a recent photo at 1600px or wider.
- Logo (`calpluglogo-small.png`, 600px): needs the original vector file.
- Event photos: all under 530px wide.

## Not migrated yet

- Full descriptions of the 18 completed projects (the data has a one-line summary and links).
- Full agendas and speaker lists of past workshops.
- Membership benefits (an image on the current site; text must be retyped).
- Arnold Wang's bio: last sentences.
