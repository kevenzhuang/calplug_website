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
| Contact | "CalIt2 administrative offices" | "Calit2 administrative offices" | Typo |
| 1 kWh Challenge | "accessibble"; no period after "on hold" | "accessible"; period added | Typos |
| SIM Home | "(SIM)Home" | "(SIM) Home" | Missing space |
| 1 kWh Challenge | "The 1KWh Challenge"; "Why:" with a one-item list; "Design" with "Label: value" bullets | "The 1 kWh Challenge"; small headings; the design facts as label / value rows | Bullet standard |
| About, Vision | Two of three items end with a period | All three end with a period | Consistent list |
| Events | Better Buildings webinar listed twice | Listed once | Duplicate |
| Publications | 2021 DOE survey report listed under Journal | Moved to reports | It is a prepared-for report |

## To confirm with Arnold

Rewritten after the full audit of 2026-11-13 (DESIGN.md 0.28). Earlier numbers are gone; items are grouped by urgency.

### Before launch (the site should not replace calplug.org until these are answered)

1. **Careers is out of date and has no way to apply.** Positions and deadline are for Spring 2026 (deadline April 3, 2026, now past); one position still carries a Fall 2025 code (IAC-F25). The old page gives no form or address: is e-mailing the mentor the way to apply? Need the current term, positions and deadline.
2. **Copyright line.** The footer says "© 2026 California Plug Load Research Center". Should it be "© 2026 The Regents of the University of California", as on other UC Irvine sites?
3. **1 kWh Challenge.** The old page said "With Covid restrictions in place the 1 Kilowatt-hour Challenges are on hold." The new page says "The challenges are currently on hold." Still on hold, or ended? If ended, the sentence goes.
4. **Workshop #19 and 10th Anniversary.** The Events Archive gives it the same date as Workshop #18 (October 18, 2021); its slides page is dated May 2022. Need the real date. In News it is shown without a date for this reason.
5. **LADWP COVID-19 project.** No description or summary: the old site's description was a copy of the CESMII survey text. Need two or three sentences.
6. **Computer Power Management Usage Survey.** The old report link opens the Set-Top Box report, so the project has no report link. Need the right file.
7. **Home paragraph.** Home now opens with the group photo and one paragraph instead of a title. Is the new paragraph (below, "Text written or shortened") right, or should the old tagline be used? The old one is kept in `data/site.json` as `tagline_current_site`.
8. **Permissions.** See "Permissions needed before launch".

### Content questions (can be fixed after launch; the site shows what the old site showed)

Projects
- AI-TES and Occupancy-based Lighting: no sponsor or years. AI-TES's text still says "This research proposal introduces"; is it a funded project now?
- "Occupancy-based Lighting PPL Smart Management": "PPL" is not explained anywhere on the page (plug and process loads?).
- Smart Manufacturing in SMMs Survey (2019 to 2021): the text was in the present tense and called the study "(ongoing)". Changed to the past tense and "(ongoing)" removed. Correct?
- PLETICS: "that currently do not have Title 20 requirements" became "that did not have Title 20 requirements". Correct for 2021? The report is cited as 2026 but its CEC number is CEC-500-2025-018: which year?
- Edge Data Center: "25–35% total facility energy savings" is in the full text only, not in the summary, because it is a target, not a measured result.
- Research areas (`themes` in `data/projects.json`) are a draft; labels shortened in 0.28 to "Plug loads" and "Grid & storage".
- No completed project has a picture; 6 projects have no report link (the four current ones and the two surveys without a file); no project names a principal investigator or contact. Worth adding where the lab has them.
- Student posters: "Experimental Test of Energy Annoyance Thresholds" opens the PMUI 5.0 poster file.

Labs and archive
- SIM Lab: "SIM labs (Simulation Integration Majority)" was changed to "(Simulation, Integration, and Management)", the expansion used on the SIM Home page. Correct?
- Our labs introduction ("CalPlug encompasses various facilities that ensure the latest in Plug and Process load research is going on") reads awkwardly; left as written. A new sentence would be welcome.
- Events Archive, Workshop #19: the speaker line said "John Woosley", the agenda "John Woolsey"; both now say Woolsey. "Matthias Kurwing" (Enervee) may be "Kurwig". Please check both names.

People
- Advisory board order: co-chairs first, then alphabetical, except Armen Saiyan at the end. Intended?
- "Ph.D." follows the names of the team and faculty but not of board members who hold one. One rule?
- G. P. Li's departments differ between his bio (EECS, Biomedical Engineering, Materials and Manufacturing Technology) and the faculty list (EECS, Biomedical Engineering, Chemical Engineering & Materials Science).
- Students: level "Post-graduate" (meaning?) and the abbreviation "EECS" next to departments written in full.
- Chief Technology Council lists Amir Tabakh as "Former Assistant Director" among current members.
- Are board and council titles and affiliations current? Several photos are small or of unknown source.

Publications
- 8 entries have no link.
- Venue names are written several ways (EEDAL four ways, ACEEE three, BECC two); EEDAL papers are typed partly as Journal, partly as Conference. Which is right?
- "Journal of Manufacturing, Vol. 61" is probably "Journal of Manufacturing Systems".
- ACEEE Industry Summer Study paper: listed as "forthcoming" with a 2018 link; the event was July 2021.
- One report link uses `http://eedal2017.uci.edu/...` (not secure, and on a conference site that may disappear). A copy in `wp-content/uploads/` would be safer.

News
- Workshop Series #24, Battery Plugin Workshop and the CalPlug + IAC Earth Day Workshop have no dates or descriptions; four items have no summary.
- The third item of "Latest news" on Home is from 2021, because the undated items cannot be sorted. Dates would fix this.

Support
- The benefits table (retyped from an image) mentions a "Friends" level that the page does not offer, and uses "EE" without explaining it. "specific terms TBD" was written as "specific terms to be agreed". Is the table current?
- "Past members and current affiliates" puts two different groups under one title. Which organizations are which?
- "Give a gift" names Herumi Baylon as the contact. Still right?

About
- The page is titled "About" and its first section "About CalPlug".
- "CalPlug will address challenges ..." is in the future tense for a center founded in 2011; "plug loads related energy fields" and "best practices solutions" in the Organization goal were left as written.

## Text written or shortened for the new site (version 0.10, for Arnold to review)

The full original text is still on the site wherever it existed (project pages, "Full bio"); only the short pieces below are new.

| Where | New text | Based on |
|---|---|---|
| Home tagline (`site.json`) | "The California Plug Load Research Center (CalPlug) studies how appliances, buildings and data centers use energy, and develops ways to use less of it. We bring together researchers, utilities, manufacturers and policy makers. Founded in 2011 at Calit2, UC Irvine." | About text (founding year, focus, partners) and current projects; replaces "the Leading Enabler for Energy Efficiency Solutions... Join Us in our Journey towards Improving Energy Efficiency and Cross Collaboration". Show Arnold both |
| Projects intro | Two sentences on who CalPlug works with | About text |
| Project short titles (Home cards) | "SIGNAL: Net-load Forecasting", "AI-TES: Thermal Energy Storage", "Edge Data Center Smart Retrofit", "Occupancy-based Smart Lighting" | Full titles |
| Project summaries | One sentence each (already in the data since 0.1) | Original descriptions |
| Careers | Intro, deadline notice, "What you get", "What we ask", one-sentence position descriptions, tasks, 4 apply steps | Old Careers page, same facts |
| Support | Intro, three ways to support, membership level cards | Old Support, Friends and Members pages, same facts |
| News: CalPlug/ITAC 2026 Annual Workshop | Summary shortened to 25 words | Old summary |
| Share image line (`assets/brand/share.png`) | "How homes, offices and data centers use energy, and tools that help people use less of it." | Home tagline |
| 404 page | "This page is unplugged." and one sentence | New |
| Contact card titles | "General & directions", "Collaborations", "Calit2" | Old titles "General Information, Directions & Parking", "CalPlug Collaborations", "General / Calit2 Information" |
| Contact hours | "Monday to Friday, 8:00 am to 5:00 pm" | "Mon-Fri 8:00am - 5:00pm" |

## Changes inside original text (version 0.28, approved by Keven Zhuang on 2026-11-13, for Arnold to review)

Only three kinds of change were made: spelling and grammar, the tense of completed projects, and paragraph breaks. No meaning, number or name was changed on purpose; where a correction needed a judgment it says "please confirm".

| Where | Before | After |
|---|---|---|
| SIGNAL | uniquely assembles multi-disciplinary team | uniquely assembles a multi-disciplinary team |
| SIGNAL | a state-of-art multi-horizon | a state-of-the-art multi-horizon |
| SIGNAL | to ensure model’s seamless integration | to ensure the model’s seamless integration |
| SIGNAL | 300-500 households | 300–500 households |
| SIGNAL | at 2-3 selected substations | at 2–3 selected substations |
| SIGNAL | training documentations | training documentation |
| SIGNAL | critical 2024-2030 period | critical 2024–2030 period |
| SIGNAL | as national leader | as a national leader |
| AI-TES | Sensible Thermal Energy Storage (TES) have been demonstrated | Sensible Thermal Energy Storage (TES) systems have been demonstrated |
| Edge Data Center | small-scale edge datacenters | small-scale edge data centers |
| Edge Data Center | thus is often overlooked | and thus are often overlooked |
| Edge Data Center | if a cost-effective, easy-deployable technologies can be demonstrated | if cost-effective, easily deployable technologies can be demonstrated |
| Occupancy-based Lighting | from IoT-based sensor system | from an IoT-based sensor system |
| PLETICS (completed 2024) | The Energy Commission has tasked CalPlug | The Energy Commission tasked CalPlug |
| PLETICS (completed 2024) | that currently do not have Title 20 requirements | that did not have Title 20 requirements |
| PLETICS (completed 2024) | In this project, we will identify | In this project, the team set out to identify |
| SMM Survey (completed 2021) | The goal of the Smart Connected Workers project is to create | The goal of the Smart Connected Workers project was to create |
| SMM Survey (completed 2021) | The project aims to develop the smart manufacturing platform | The project aimed to develop the smart manufacturing platform |
| SMM Survey (completed 2021) | CalPlug contributes a state of the market review | CalPlug contributed a state of the market review |
| SMM Survey (completed 2021) | Participants of the study (ongoing) are owners | Participants of the study were owners |
| SMM Survey (completed 2021) | consultants who work with these SMEs | consultants who worked with these SMEs |
| SMM Survey (completed 2021) | CalPlug staff is also involved in development | CalPlug staff was also involved in development |
| ComEd | plug load devices , with | plug load devices, with |
| PMUI | randomized control trial at the University of California, Irvine | randomized controlled trial at the University of California, Irvine. |
| Behavioral Interventions | over 1400 sources | over 1,400 sources |
| Roadmap 2030 | California’s ZNE net energy efforts | California’s zero net energy (ZNE) efforts |
| Smart Meter Data on TV (completed 2014) | will be relayed from | is relayed from |
| Smart Meter Data on TV (completed 2014) | will embed the consumer home energy usage | embeds the consumer home energy usage |
| Smart Meter Data on TV (completed 2014) | Displaying this data will provide home owners with sufficient information that will help them manage | Displaying this data provides home owners with sufficient information to help them manage |
| Smart Meter Data on TV (completed 2014) | The user friendly interface has been designed to display customer’s energy usage | The user-friendly interface was designed to display customers’ energy usage |
| Computer PM Survey | Respondents were ask about | Respondents were asked about |
| Student projects | Annoyance Threshold Testing | Annoyance threshold testing |
| Student projects | Buddy Projects | Buddy projects |
| Student projects | SIM Home Projects | SIM Home projects |
| Student projects | Other Projects | Other projects |
| About, Vision | and education and motivating them to participate | and educating and motivating them to participate |
| About, Vision | users’ needs and usage patterns enabling user input | users’ needs and usage patterns, enabling user input |
| About, Facility | located on the building’s fourth floor | located on the fourth floor of the Calit2 Building |
| About | Mission Statement | Mission statement |
| About | Organization Goal | Organization goal |
| Our labs, SIM Home | while monitoring energy consumption monitoring | while monitoring energy consumption |
| Our labs, 1 kWh Challenge | designed as an Educational Program | designed as an educational program |
| Our labs, 1 kWh Challenge | how much energy a Kilowatt-hour is | how much energy a kilowatt-hour is |
| Our labs, SIM Lab | provides testing service | provides a testing service |
| Our labs, SIM Lab | obtain power consumption and savings report | obtain a power consumption and savings report |
| Our labs, SIM Lab | (Simulation Integration Majority) | (Simulation, Integration, and Management) |
| People, G. P. Li bio | which research and develop solutions | which researches and develops solutions |
| People, G. P. Li bio | with additional 11 patents pending | with an additional 11 patents pending |
| People, Shuoyu (Arnold) Wang bio | National Renewable Energy Laboratory(NREL) | National Renewable Energy Laboratory (NREL) |
| People, Shuoyu (Arnold) Wang bio | a M.S. in civil engineering | an M.S. in civil engineering |
| People, Shuoyu (Arnold) Wang bio | He has a diverse expertise | He has diverse expertise |
| People, Affiliated faculty | G.P. Li, Ph.D. | G. P. Li, Ph.D. |
| People, Council emeriti | Electric Power Research Institute (EPRI) | Electric Power Research Institute |
| Contact | in the Calit2 building, | in the Calit2 Building, |
| Careers | 5:00 PM PST | 5:00 pm PT |
| Careers | 5:00 PM PST | 5:00 pm PT |
| Our labs, SIM Home | or SIM-Home for short | or SIM Home for short |
| SIM Home page | can cause an HVAC system create | can cause an HVAC system to create |
| SIM Home page | (or higher)energy | (or higher) energy |
| SIM Home page | The four recommendations were four paragraphs | A bullet list after the lead-in line (same words) |
| SIM Lab page | provides testing service | provides a testing service |
| SIM Lab page | obtain power consumption and savings report | obtain a power consumption and savings report |
| SIM Lab page | (Simulation Integration Majority) | (Simulation, Integration, and Management), as on the SIM Home page. Please confirm |
| SIM Lab page | Bench-top Test / Field Trial (headings) | Bench-top test / Field trial (captions under the pictures) |
| 1 kWh Challenge page | designed as an Educational Program ... a Kilowatt-hour is | designed as an educational program ... a kilowatt-hour is |
| 1 kWh Challenge page | With Covid restrictions in place the 1 Kilowatt-hour Challenges are on hold. | The challenges are currently on hold. (The reason was out of date; see Before launch, item 3) |
| 1 kWh Challenge page | the 1 Kilowatt Challenge’s purpose was quantifying and defining what a kWh was | the 1 kWh Challenge’s purpose was to quantify and define what a kWh is |
| 1 kWh Challenge page | Heading "The 1 kWh Challenge" under the page title; "The Challenges"; "Key Outcomes" | Repeated heading removed; "The challenges"; "Key outcomes" |
| Events Archive, #19 | CalIt2’s own Auditorium; Climate Resiliency, Lowering greenhouse gas emissions | Calit2’s own auditorium; climate resiliency, lowering greenhouse gas emissions |
| Events Archive, #19 | Enrvee; National Renewable Energy Laboratory NREL; John Woosley (speaker line) | Enervee; National Renewable Energy Laboratory (NREL); John Woolsey (as in the agenda). Please confirm the spelling |
| Events Archive, #19 | Decabonization; Combine Heat & Power; in energy Resiliency | Decarbonization; Combined Heat & Power; in Energy Resiliency |
| Events Archive, #18 | CalPlug’s 18th was hosted on Webinar, and discussed the processes of Optimizing Energy Efficiency in Spaces, office commercial and in the home. | CalPlug’s 18th workshop was hosted as a webinar, and discussed the processes of optimizing energy efficiency in spaces, in commercial offices and in the home. |
| Events Archive, #18 | Calit2/CalPlug Research center; GP Li | Calit2/CalPlug Research Center; G.P. Li |
| Events Archive, ACEEE | presented about survey results | presented survey results |
| Events Archive, #17 | Luc Serveri; National Research Energy Laboratory; a bare YouTube address; the agenda as one run-on line | Luc Severi (as in the agenda and the slide file); National Renewable Energy Laboratory; a "Recording" link; the agenda as a list |
| Events Archive, webinar | The webinar appeared twice: a report, and further down the invitation ("Please join us on Wednesday, March 17 ...") | One entry: the report, with time, description and presenter from the invitation as label / value rows. The invitation sentence is dropped |
| Events Archive, 3 C's | Calplug Technical Director; the agenda as paragraphs | CalPlug Technical Director; the agenda as a list with its two sessions |
| Events Archive, #15 | Heading "CalPlug WorkShop & Earth Celebration Day" and "CalPlug Workshop # 15 April 21-22, 2020– Presented Online" | "CalPlug Workshop #15 & Earth Day Celebration" (the title used in News), date line, "Presented online." |
| Events Archive, #15 | established biannual workshops since its inception; bringing all stakeholders in the energy sector to maximize; As a state California ...; as a California public research center; Calplug; Dr. G.P Li; Co-Founder  Of | has held biannual workshops since its inception; bringing all stakeholders in the energy sector together to maximize; As a state, California ...; as a California public research center, CalPlug; Dr. G.P. Li; Co-Founder of |
| Events Archive, all | Times as 10 am, 9:00 a.m., 1:00pm; dates as Monday, October 18, 2021 / July 12-15, 2021 / Mar 17, 2021 | 10:00 am, 9:00 am, 1:00 pm; Oct 18, 2021 / Jul 12–15, 2021 / Mar 17, 2021 |
| Events Archive, all | Link words "Related Slides", "Presentation Slides", "Program Brochure", "Watch Recording", "PPT", "here" | "Slides", "Brochure", "Recording", "slides" (the words used in News) |

Paragraphs split without changing a word (limit: 150 words per paragraph):

- SIGNAL: new paragraph “Second, a state-of-the-art…” / “Third, a comprehensive…”
- AI-TES: new paragraph “This research proposal intro…”
- Edge Data Center: new paragraph “The project integrates digit…”
- PLETICS: new paragraph “In this project, the team se…”
- Nevada Industry 4.0: new paragraph “Staffing needs are a major c…” / “A key contribution of this s…” / “Overall, variations in evalu…”
- SMM Survey: new paragraph “The goal of the Smart Connec…”
- Computer PM Survey: new paragraph “Important reasons given for …”
- Computer Power Modes: new paragraph “Power state monitoring shows…” / “Greater power management eng…”

Also: the SIM Home project no longer has a second page with the same title and the same paragraph; its row on Research opens the SIM Home lab page, which now carries the report link.

## Permissions needed before launch

- Photos and LinkedIn links of students and alumni: each person confirms.
- Photos of advisory board and council members: source unknown.

## Images carried over from the old site (decision 2026-11-12: reuse is fine for now)

| Image | Note |
|---|---|
| AI-TES figure (from f1000research), Edge Data Center image (from belden.com), Chelsea Choudhary photo (from calit2.uci.edu) | Copied into `assets/ext/` on 2026-11-13; no longer hot-linked. The first two come from other organizations: replace with the lab's own figures when possible |
| `pexels-singkham-...jpg`, `solar-energy.png` (Freepik) | Stock images; Freepik asks for attribution |
| Member and affiliate logos | All 12 have a logo. CPUC, PG&E, ComEd, DIRECTV and Embertec logos were provided by Keven Zhuang on 2026-11-13 (`assets/logos/`) |

## Images to replace when better ones arrive

- Home group photo (`zotwatt-2.jpg`, only 400 by 225 pixels): it is now the first thing on the Home page and looks soft on large screens. Needs a recent group photo at 1600px or wider; the page is built to show it larger as soon as one arrives.
- Logo (`calpluglogo-small.png`, 600px): needs the original vector file.
- Event photos: all under 530px wide.

## Not published on the new site

- The old Careers, Support, Friends and Members pages: their content was rewritten into `data/careers.json` and `data/support.json`; the old text is kept in `content/legacy/` as a record.
- The old Facilities page: now "Our labs" on Research.
