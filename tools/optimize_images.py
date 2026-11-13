#!/usr/bin/env python3
"""Make smaller copies of large images. Originals are never changed.

For every PNG or JPEG under assets/legacy, assets/ext and assets/site that is over 100 KB, writes assets/opt/<same path>.jpg (longest side 1000 px, JPEG quality 80: enough for the largest size any image is shown at, on sharp screens). tools/build.py serves the
copy when it exists. Needs Pillow (pip install Pillow). Run after adding images.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
made = 0
for folder in ("legacy", "ext", "site"):
    for f in (ROOT / "assets" / folder).rglob("*"):
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg") or f.stat().st_size < 100_000:
            continue
        out = ROOT / "assets" / "opt" / f.relative_to(ROOT / "assets")
        out = out.with_name(out.name + ".jpg")
        im = Image.open(f)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        im = im.convert("RGB")
        im.thumbnail((1000, 1000))
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, "JPEG", quality=80, optimize=True, progressive=True)
        if out.stat().st_size >= f.stat().st_size:
            out.unlink()
            continue
        made += 1
        print(f"{f.relative_to(ROOT)}: {f.stat().st_size // 1024} KB -> {out.stat().st_size // 1024} KB")
print(f"{made} optimized copies written to assets/opt/")
