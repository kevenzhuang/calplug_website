# Maintaining the CalPlug website

Version 0.1 (draft). For whoever looks after the site, with or without an AI assistant.

The rule that matters most: **change the data, not the pages.** Pages are generated. Never edit files in `dist/`.

## 1. Everyday tasks

Each task is one edit in one file under `data/`. Copy an existing entry and change its values.

| I want to | Edit | What to do |
|---|---|---|
| Add a student | `data/people.json`, list `students` | Add `name`, `program`, `level`; optional `linkedin`, `photo` |
| Mark a student as graduated | `data/people.json` | Move the entry from `students` to `alumni` |
| Add a publication | `data/publications.json`, list `publications` | Add `type` (journal, conference, report, press), `year`, `authors`, `title`, `venue`, `url`. If `url` is a PDF, run the "Import images and make thumbnails" workflow on GitHub (Actions tab) to create its thumbnail |
| Add a project | `data/projects.json`, list `projects` | Add `id`, `title`, `status` (active or completed), `start`, `end`, `sponsor`, `summary`, `themes`; active projects also need `description` |
| Finish a project | `data/projects.json` | Change `status` to `completed`, set `end`, add the report under `links` |
| Add an event or news item | `data/events.json`, list `events` | Add `id`, `title`, `date` (YYYY-MM-DD), `summary`, `links`, and `image` (see DESIGN.md, News images). Without `image` the default image is used |
| Change contact details | `data/site.json` | Edit `contact` |
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

## 6. What must never be in this repository

Passwords, API keys, login details for the domain or hosting, private email threads, unpublished results.

## 7. When something goes wrong

- Build fails: read the message. It names the file and the missing field.
- Check fails: it lists the page and the problem (broken link, image without description, leftover placeholder text).
- A bad change went live: revert the merge on GitHub. The previous version is published again.
