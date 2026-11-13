# CalPlug website

Source of the website of the California Plug Load Research Center (CalPlug), UC Irvine.

**Status: sample for review. Not the official site.** The official site is https://www.calplug.org. Search engines are told not to index this sample.

## How it works

- Content lives in `data/*.json` (people, projects, publications, events, partners, site text).
- `tools/build.py` turns the data into plain HTML pages in `dist/`. No framework, no database.
- Every push runs the build and the checks on GitHub. If they pass on `main`, the site is published.

## Preview on your computer

Needs Python 3.12 or newer. Nothing to install.

```
python tools/build.py
python tools/check.py
python -m http.server --directory dist 8000
```

Then open http://localhost:8000.

## Read before you change anything

| File | Read it when |
|---|---|
| `MAINTAINING.md` | You want to add a person, a paper, a project or an event, or publish |
| `DESIGN.md` | You want to change how something looks or add a new kind of section |
| `AGENTS.md` | You are an AI assistant working in this repository |
| `CONTENT-NOTES.md` | You want to know what is unconfirmed or still missing |

## People

| Role | Who |
|---|---|
| Owner | To be set when the repository moves to the lab's GitHub organization |
| Site maintainer | Keven Zhuang (until December 2026) |
| Backup maintainer | To be named |
