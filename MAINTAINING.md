# Maintaining the CalPlug website

Version 0.2 (draft). For whoever looks after the site, with or without an AI assistant.

The rule that matters most: **change the data, not the pages.** Pages are generated. Never edit files in `dist/`.

## 1. Everyday tasks

Each task is one edit in one file under `data/`. Copy an existing entry and change its values.

| I want to | Edit | What to do |
|---|---|---|
| Add a student | `data/people.json`, list `students` | Add `name`, `program`, `level`; optional `linkedin`, `photo`. The name is shown as text and the link as "LinkedIn" on its own line (faculty: `url`, shown as "Profile") |
| Mark a student as graduated | `data/people.json` | Move the entry from `students` to `alumni` |
| Add a publication | `data/publications.json`, list `publications` | Add `type` (journal, conference, report, press), `year`, `authors`, `title`, `venue`, `url`. If `url` is a PDF, run the "Import images and make thumbnails" workflow on GitHub (Actions tab) to create its thumbnail |
| Add a project | `data/projects.json`, list `projects` | Add `id`, `title`, `status` (active or completed), `start`, `end`, `sponsor`, `summary`, `themes`; active projects also need `description` and `image`, and a `short_title` for the Home card. Every project with a `description` gets its own page. `description` is a list of paragraphs, each at most 150 words. A project that already has a page elsewhere on the site names it in `page` instead (SIM Home: `"page": "sim-home.html"`) |
| Finish a project | `data/projects.json` | Change `status` to `completed`, set `end`, add the report under `links` |
| Add an event or news item | `data/events.json`, list `events` | Add `id`, `title`, `date` (YYYY-MM-DD), `summary`, `links`, and `image` (see DESIGN.md, News images). Without `image` the default image is used |
| Change contact details | `data/site.json` | Edit `contact` |
| Move the site to calplug.org | `data/site.json` | Change `site_url` to `https://www.calplug.org`. Share links and the 404 page use it |
| Change the share picture | `tools/share/share.html` | Edit, then run `python tools/make_share_image.py` (needs Playwright) |
| Make slides or a flyer | `brand-kit/` | Start from the templates; see `brand-kit/README.md` |
| Turn a logo picture into a vector file | `tools/trace_logo.py` | `python tools/trace_logo.py in.png out.svg --colors "#005BAA,#8BC53F,#000000" --scale 3` (needs `pip install potracer`). Compare the result with the picture before using it |
| Download new images or PDF documents from the old site, or images from another site named in the data | GitHub Actions, "Import images and documents" | Never rewrites data or pages. Images go to `assets/legacy/`, documents to `wp-content/uploads/` (their old path). Files over 90 MB are reported and left out. The imported files are published with the next change; to publish them at once, run "Build, check and deploy" from the Actions tab |
| Add a new document (report, slides, poster) | `wp-content/uploads/` | Put the PDF there and write its path in the data as `/wp-content/uploads/<file>.pdf`. Lower-case letters, digits and hyphens in the name; under 50 MB if possible |
| After adding any image | `python tools/optimize_images.py` | Writes smaller copies to `assets/opt/` (needs Pillow). The build refuses images over 400 KB |
| Update Careers (term, deadline, positions) | `data/careers.json` | Change `term` and `deadline`; each position has `id`, `title`, `mentors` (name, email, photo), one-sentence `description`, up to 3 `tasks`, and optionally `project` (the `id` of its project in `data/projects.json`; the card then links to the project page). The build stops if a piece is too long (DESIGN.md section 5) |
| Update Support (members, affiliates, benefits) | `data/support.json` | Members and affiliates: `name` and optional `logo` (without a logo the name is shown in a tile). Benefits: one line per benefit with the levels that include it (`G`, `P`, `D`) |
| Change the home paragraph or a page introduction | `data/site.json` (`tagline`), `data/projects.json` (`intro`), `data/careers.json`, `data/support.json` | Keep within the length limits in DESIGN.md section 5. The home paragraph must contain "California Plug Load Research Center (CalPlug)" |
| Replace the Home group photo | `assets/legacy/zotwatt-2.jpg`, then `tools/build.py` (`build_home`) and DESIGN.md "Home welcome" | Use a photo at least 1600px wide; with it the 640px limit in `src/css/site.css` (`.welcome figure`) can go up to the text width |
| Edit a lab page or the Events Archive | `content/legacy/<page>.html` | Plain HTML, first copied from the old site and since brought up to DESIGN.md. Edit the text directly; keep the tags simple (p, h2, h3, ul, li, a, figure, img with alt). A new event in the archive copies the block of an existing one: title, date, paragraph, speakers, agenda, links, picture. Do not run `tools/import_pages.py` again: it would overwrite these files with the old site's version. `careers.html`, `support.html`, `friends.html` and `members.html` there are kept as the record of the old pages and are no longer published |
| Add a board member | `data/people.json`, list `advisory_board` or `technology_council` | Add `name`, `title`, `org`, `org_url`, `photo` |

Example, adding a publication:

```json
{ "type": "conference", "year": 2027, "authors": "A. Student, S. Wang, G.P. Li",
  "title": "Title of the paper", "venue": "Name of the conference", "url": "https://doi.org/..." }
```

Photos: put the file in `assets/people/` (square, at least 600 by 600 pixels) and write its path in `photo`. Leave `photo` out if there is none; the site shows the person's initials.

## 2. Publishing a change

1. Create a branch and make the change.
2. Run `python tools/build.py` and `python tools/check.py`. Both must pass.
3. Open a pull request. Say what changed and where the information comes from.
4. GitHub runs the same build and checks. A red mark means it cannot be merged yet.
5. A reviewer approves (see section 3). Merge. The site updates by itself a few minutes later.

In the operation phase nobody pushes straight to `main` (see section 3).

## 3. Approval: two phases

| Phase | When | Rule |
|---|---|---|
| Setup | Now, while the site is a sample under review | The site maintainer and their AI assistant may push directly to `main` to move fast. Every change is still built and checked automatically. |
| Operation | From the day the director or project scientist approves the first version (record the date here: ______) | No change goes live without a person's approval. An AI assistant may prepare a change on a branch and open a pull request; it may not merge, and it may not push to `main`. Turn on branch protection for `main` on that day. |

In both phases an AI assistant asks before it changes a format in `DESIGN.md` or this file.

## 3b. Who can do what

| Role | Who | Can do |
|---|---|---|
| Owner | Center director and project scientist | Manage members and settings; approve changes to Home, Partner, people's titles, and partner names or logos |
| Maintainer | Site maintainer and one backup | Review and merge everyday changes (students, publications, events) |
| Contributor | Any lab member | Open a pull request |

Each merge needs one approval from someone other than the author. Everyday data changes: a maintainer. Anything that speaks for the center (Home, Partner, sponsor names, claims with numbers): an owner.

## 4. Record of changes

Git is the record. To keep it readable:

- One topic per pull request.
- Commit message format: `Add: ...`, `Update: ...`, `Fix: ...`, `Remove: ...`, followed by what and why. Example: `Add: 2027 e-Energy paper to publications (from Arnold, email of Jan 20)`.
- Changes made with an AI assistant are reviewed the same way as any other change; say in the pull request which assistant was used.
- Changes to the look of the site also update the change log at the end of `DESIGN.md`.

## 5. Improving the formats

The formats in `DESIGN.md` and in this file are expected to get better over time. When something does not fit:

1. Say what does not fit and propose the change to the format.
2. After approval, update `DESIGN.md` or this file first, with a line in the change log.
3. Then update the build script and bring all existing content up to the new format.

Everything new is built on the current formats. No one-off exceptions.

## 5b. Regular upkeep

| When | What |
|---|---|
| Any time | New papers, events and news |
| Start of every quarter | Students who joined or left; open positions and deadline on the People page; finished projects |
| Once a year (September) | Advisory board and council titles; contact details; items in `CONTENT-NOTES.md`; broken outside links |
| One quarter before the maintainer leaves | Name the next maintainer; they make one full change (add a person, add a paper, publish) while the current maintainer watches |

## 5c. Going live on calplug.org

The sample runs at a GitHub address and tells search engines to stay away. On the day the site replaces the WordPress site, in this order:

| Step | Where | What |
|---|---|---|
| 1 | `CONTENT-NOTES.md` | Every item under "Before launch" is answered or removed from the site |
| 2 | GitHub Actions, "Import images and documents" | Run it one last time while the old site is still up; the build should print no "still point to the old site" note |
| 3 | `data/site.json` | Change `site_url` to `https://www.calplug.org` |
| 4 | `tools/build.py`, function `page()` | Remove the `noindex` line so search engines may list the site |
| 5 | Repository | Add a `CNAME` file containing `www.calplug.org`, and a `sitemap.xml` listing the pages (ask for both in one change) |
| 6 | Domain settings (whoever manages calplug.org) | Point `www.calplug.org` to GitHub Pages; in the repository settings, Pages, set the custom domain and turn on "Enforce HTTPS" |
| 7 | Browser | Open five old addresses (a PDF from a paper, `/projects`, `/people`, `/about/careers`, `/eventsarchive`). PDFs open as before; old page addresses show the 404 page with links, unless redirects were added |
| 8 | This file, section 3 | Write the approval date and turn on branch protection for `main` |

Size: the repository holds about 350 MB of documents (63 PDFs, the largest 66 MB) and 35 MB of images. GitHub Pages allows 1 GB per site and 100 MB per file.

## 6. What must never be in this repository

Passwords, API keys, login details for the domain or hosting, private email threads, unpublished results.

## 7. When something goes wrong

- Build fails: read the message. It names the file and the missing field.
- Check fails: it lists the page and the problem (broken link, image without description, leftover placeholder text, a time not written like "5:00 pm PT", a paragraph over 150 words, an arrow link that leaves the site).
- A bad change went live: revert the merge on GitHub. The previous version is published again.
