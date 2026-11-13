#!/usr/bin/env python3
"""Trace a logo bitmap into an SVG, one filled layer per brand color.

Usage: python tools/trace_logo.py IN.png OUT.svg --colors "#005BAA,#8BC53F,#000000" [--scale 3] [--crop x,y,w,h]

Each pixel is assigned to the nearest of the given colors or to white (the background), after enlarging
the image so that edges come out smooth. Each color is then traced with potrace (pip install potracer).
The result is only as faithful as the source bitmap: small text in a small image comes out approximate.
"""
import argparse
from PIL import Image
import numpy as np
import potrace


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def trace_layer(mask, scale, turd):
    bm = potrace.Bitmap(~mask)  # potracer traces the dark (False) pixels, so pass the inverse
    plist = bm.trace(turdsize=turd, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.2)
    f = lambda p: f"{p.x / scale:.2f} {p.y / scale:.2f}"
    d = []
    for curve in plist:
        d.append("M" + f(curve.start_point))
        for seg in curve.segments:
            if seg.is_corner:
                d.append("L" + f(seg.c) + "L" + f(seg.end_point))
            else:
                d.append("C" + f(seg.c1) + " " + f(seg.c2) + " " + f(seg.end_point))
        d.append("Z")
    return "".join(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--colors", required=True)
    ap.add_argument("--scale", type=int, default=3)
    ap.add_argument("--crop", default="")
    ap.add_argument("--label", default="Logo")
    ap.add_argument("--bg-bias", type=float, default=1.0)
    ap.add_argument("--text-from", type=int, default=0, help="source row where small text starts")
    ap.add_argument("--text-bias", type=float, default=2.0)
    a = ap.parse_args()
    im = Image.open(a.src).convert("RGBA")
    bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); im = bg.convert("RGB")
    if a.crop:
        x, y, w, h = map(int, a.crop.split(","))
        im = im.crop((x, y, x + w, y + h))
    W, H = im.size
    big = np.array(im.resize((W * a.scale, H * a.scale), Image.LANCZOS)).astype(int)
    colors = [c.strip() for c in a.colors.split(",")]
    palette = np.array([(255, 255, 255)] + [hex2rgb(c) for c in colors])
    # Saturated pixels take the brand color nearest in hue (a blurred light-blue edge stays blue, never green);
    # unsaturated pixels can only be a neutral color (black) or the background.
    def hue(rgb):
        r, g, b = [rgb[..., i] / 255.0 for i in range(3)]
        mx, mn = np.max(rgb, -1) / 255.0, np.min(rgb, -1) / 255.0
        d = np.where(mx - mn == 0, 1e-9, mx - mn)
        h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4))
        return h * 60
    chroma = big.max(-1) - big.min(-1)
    pal_chroma = palette.max(-1) - palette.min(-1)
    chromatic = [i for i in range(1, len(palette)) if pal_chroma[i] >= 40]
    neutral = [i for i in range(1, len(palette)) if pal_chroma[i] < 40]
    rgbdist = lambda i: ((big - palette[i]) ** 2).sum(-1).astype(float)
    bias = np.full(big.shape[:2], a.bg_bias)
    if a.text_from:  # small text below this row (in source pixels) is blurrier: keep more of it
        bias[a.text_from * a.scale:, :] = a.text_bias
    bgdist = rgbdist(0) * bias ** 2
    label = np.zeros(big.shape[:2], dtype=int)
    sat = chroma >= 25
    if chromatic:
        ph = hue(big.astype(float)); best = None; bestd = None
        for i in chromatic:
            hd = np.abs((ph - hue(palette[i][None].astype(float))[0] + 180) % 360 - 180)
            best = np.where(bestd is None or True, best, best) if False else best
            if bestd is None:
                best, bestd = np.full(ph.shape, i), hd
            else:
                take = hd < bestd; best = np.where(take, i, best); bestd = np.where(take, hd, bestd)
        fg = np.zeros(ph.shape, dtype=float)
        for i in chromatic:
            fg = np.where(best == i, rgbdist(i), fg)
        label = np.where(sat & (fg < bgdist), best, label)
    if neutral:
        nd = np.stack([rgbdist(i) for i in neutral], -1)
        nbest = np.array(neutral)[nd.argmin(-1)]
        label = np.where(~sat & (nd.min(-1) < bgdist), nbest, label)
    paths = []
    for i, c in enumerate(colors, start=1):
        d = trace_layer(label == i, a.scale, turd=4 * a.scale)
        if d:
            paths.append(f'<path fill="{c}" fill-rule="evenodd" d="{d}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{a.label}">\n'
           + "\n".join(paths) + "\n</svg>\n")
    open(a.out, "w").write(svg)
    print(f"Wrote {a.out}: {W}x{H}, {len(paths)} layers, {len(svg) // 1024} KB")


if __name__ == "__main__":
    main()
