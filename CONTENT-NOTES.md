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
| `data/partners.json` | Facilities | n/a |
| `data/careers.json` | Careers page, rewritten into short pieces | 4 positions |
| `data/support.json` | Support page, rewritten; membership benefits retyped from the old image | 2 members, 10 affiliates, 26 benefits |

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
11. Careers: positions and deadline are for Spring 2026 (deadline April 3, 2026, now past). Need the current term's positions. The old page also gives no application form or address: is applying by emailing the mentor right?
12. Advisory board and council lists: are titles and affiliations current?
13. Research areas: draft grouping in `data/projects.json` (`themes`), now used as the Projects filter.
14. Membership benefits: retyped from the table image; "specific terms TBD" written as "specific terms to be agreed". Is the table still current?
15. Mentor photo for Chelsea Choudhary is hot-linked from calit2.uci.edu.

## Text written or shortened for the new site (version 0.10, for Arnold to review)

The full original text is still on the site wherever it existed (project pages, "Full bio"); only the short pieces below are new.

| Where | New text | Based on |
|---|---|---|
| Home tagline (`site.json`) | "CalPlug studies how energy is used in homes, offices and data centers, and builds data, sensing and AI tools that help people use less of it. Founded in 2011 at Calit2, UC Irvine." | About text and current projects; replaces "the Leading Enabler for Energy Efficiency Solutions..." |
| Projects intro | Two sentences on who CalPlug works with | About text |
| Project short titles (Home cards) | "SIGNAL: Net-load Forecasting", "AI-TES: Thermal Energy Storage", "Edge Data Center Smart Retrofit", "Occupancy-based Smart Lighting" | Full titles |
| Project summaries | One sentence each (already in the data since 0.1) | Original descriptions |
| Careers | Intro, deadline notice, "What you get", "What we ask", one-sentence position descriptions, tasks, 4 apply steps | Old Careers page, same facts |
| Support | Intro, three ways to support, membership level cards | Old Support, Friends and Members pages, same facts |
| News: CalPlug/ITAC 2026 Annual Workshop | Summary shortened to 25 words | Old summary |
| Share image line (`assets/brand/share.png`) | "How homes, offices and data centers use energy, and tools that help people use less of it." | Home tagline |
| 404 page | "This page is unplugged." and one sentence | New |

## Permissions needed before launch

- Photos and LinkedIn links of students and alumni: each person confirms.
- Photos of advisory board and council members: source unknown.

## Images carried over from the old site (decision 2026-11-12: reuse is fine for now)

| Image | Note |
|---|---|
| AI-TES figure (f1000research-files.f1000.com) | Still hot-linked from a journal site; will break if that site moves it |
| Edge Data Center image (assets.belden.com) | Still hot-linked from a company site |
| `pexels-singkham-...jpg`, `solar-energy.png` (Freepik) | Stock images; Freepik asks for attribution |
| Member and affiliate logos | All 12 have a logo. CPUC, PG&E, ComEd, DIRECTV and Embertec logos were provided by Keven Zhuang on 2026-11-13 (`assets/logos/`) |

## Images to replace when better ones arrive

- Hero photo (`zotwatt-2.jpg`, 647px wide): needs a recent photo at 1600px or wider.
- Logo (`calpluglogo-small.png`, 600px): needs the original vector file.
- Event photos: all under 530px wide.

## Not migrated yet

- Full agendas and speaker lists of past workshops.
- Arnold Wang's bio: last sentences.
