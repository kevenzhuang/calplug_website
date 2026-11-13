# Instructions for AI assistants

You are working on the CalPlug website. Follow these rules whatever tool you are.

1. Read `MAINTAINING.md` before changing content and `DESIGN.md` before changing anything visual.
2. Content changes go in `data/*.json` only. Do not edit `dist/`. Do not write content into `tools/build.py`.
3. Use only the tokens in `DESIGN.md` section 3 (colors, type sizes, weights, line heights, spacing, radii, durations) and the four controls listed there. `tools/check.py` rejects raw values in the stylesheet. If you need something new, add it to `DESIGN.md` first, with its job and reason, and say so.
4. Do not invent facts. Every name, number, date, title and partner must come from the person you are working with or from a source you can point to. If you are unsure, add the item to `CONTENT-NOTES.md` and leave it off the site.
5. After every change run `python tools/build.py` and `python tools/check.py`. Fix what they report. Do not weaken a check to make it pass.
6. For visual changes, look at the result at 1440px and 390px wide before saying it is done.
7. Follow the approval phase in `MAINTAINING.md` section 3. In the operation phase: work on a branch, open a pull request, and wait for a person to approve. Never push to `main`, never merge your own change, and never publish without a person's explicit yes.
8. Never add secrets, tracking scripts, or files downloaded from unknown sources.
9. If a fix applies to one item, check whether the same problem exists elsewhere and fix all of it.
10. Formats come first. If content does not fit a format in `DESIGN.md`, do not improvise: propose a change to the format, get it approved, update the guide and its change log, then apply it everywhere.
