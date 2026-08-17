#!/usr/bin/env python3
"""Generate favicon SVG/PNGs and OG image for We, the People from a shared
'signal' icon definition (scattered dots + connected ascending signal line),
matching the uploaded logo concept."""
import math
from PIL import Image, ImageDraw, ImageFont

# --- Shared icon geometry (100x100 viewBox) -----------------------------
# Large "signal" dots connected by a line, ascending left -> right with
# two small dips, echoing the reference logo.
SIGNAL_POINTS = [
    (10, 78),
    (27, 46),
    (44, 60),
    (61, 30),
    (78, 42),
    (94, 14),
]
SIGNAL_RADIUS = 4.6

# Scattered, unconnected "noise" dots (raw, unread signals)
NOISE_POINTS = [
    (6, 30, 2.0), (18, 18, 2.6), (33, 12, 1.8), (50, 8, 2.2),
    (68, 10, 1.6), (86, 4, 2.0), (96, 34, 1.8), (90, 58, 2.4),
    (72, 66, 1.8), (55, 74, 2.6), (38, 82, 2.0), (20, 92, 1.8),
    (4, 58, 1.6), (14, 62, 2.2), (30, 72, 1.6), (46, 44, 1.8),
    (62, 58, 1.6), (80, 26, 1.8),
]

def build_svg(stroke="#12121A", dot_fill="#12121A", noise_fill="#12121A",
              noise_opacity=0.38, bg=None, pad=6, size=100):
    vb = size + pad * 2
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}">']
    if bg:
        parts.append(f'<rect width="{vb}" height="{vb}" rx="{vb*0.22:.1f}" fill="{bg}"/>')
    # offset points by pad
    pts = [(x + pad, y + pad) for x, y in SIGNAL_POINTS]
    path_d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    parts.append(f'<path d="{path_d}" fill="none" stroke="{stroke}" '
                  f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, y, r in NOISE_POINTS:
        parts.append(f'<circle cx="{x+pad:.1f}" cy="{y+pad:.1f}" r="{r:.1f}" '
                      f'fill="{noise_fill}" opacity="{noise_opacity}"/>')
    for x, y in pts:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{SIGNAL_RADIUS}" fill="{dot_fill}"/>')
    parts.append('</svg>')
    return "\n".join(parts)

def draw_icon_pil(draw, ox, oy, scale, stroke=(18,18,26,255), dot_fill=(18,18,26,255),
                   noise_fill=(18,18,26,110)):
    def tx(x, y):
        return (ox + x * scale, oy + y * scale)
    pts = [tx(*p) for p in SIGNAL_POINTS]
    draw.line(pts, fill=stroke, width=max(2, int(2.6 * scale)), joint="curve")
    for x, y, r in NOISE_POINTS:
        cx, cy = tx(x, y)
        rr = r * scale
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=noise_fill)
    for x, y in SIGNAL_POINTS:
        cx, cy = tx(x, y)
        rr = SIGNAL_RADIUS * scale
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=dot_fill)

import os
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)

# 1. favicon.svg (transparent bg, works on light chrome UI)
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write(build_svg(stroke="#12121A", dot_fill="#12121A", noise_fill="#12121A", noise_opacity=0.42))

# 2. mark.svg - standalone icon used inline in header/footer (currentColor)
svg_mark = build_svg(stroke="currentColor", dot_fill="currentColor", noise_fill="currentColor", noise_opacity=0.42)
with open(os.path.join(OUT, "mark.svg"), "w") as f:
    f.write(svg_mark)

# 3. Raster favicons / touch icon (off-white rounded bg + dark icon)
BG = (250, 250, 248, 255)
DARK = (18, 18, 26, 255)
DARKFADE = (18, 18, 26, 110)

def make_raster(px, filename, bg=BG, rounded=True):
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if bg:
        if rounded:
            d.rounded_rectangle([0, 0, px, px], radius=int(px * 0.22), fill=bg)
        else:
            d.rectangle([0, 0, px, px], fill=bg)
    scale = px / 112.0
    pad = 6 * scale
    draw_icon_pil(d, pad, pad, scale, stroke=DARK, dot_fill=DARK, noise_fill=DARKFADE)
    img.save(os.path.join(OUT, filename))

make_raster(32, "favicon-32.png")
make_raster(180, "apple-touch-icon.png")
make_raster(192, "icon-192.png")
make_raster(512, "icon-512.png")

# 4. OG image 1200x630
W, H = 1200, 630
og = Image.new("RGB", (W, H), (250, 250, 248))
d = ImageDraw.Draw(og)
scale = 2.6
draw_icon_pil(d, 90, 150, scale, stroke=DARK, dot_fill=DARK, noise_fill=DARKFADE)

def load_font(bold, size):
    path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else \
           "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    return ImageFont.truetype(path, size)

title_font = load_font(True, 78)
tag_font = load_font(False, 30)
sub_font = load_font(False, 26)

tx = 430
d.text((tx, 210), "We, the People", font=title_font, fill=(18, 18, 26))
d.line([(tx, 300), (tx, 300)], fill=(18,18,26))
d.text((tx, 302), "READING THE SIGNALS OF CHANGE", font=tag_font, fill=(18, 18, 26))
d.text((tx, 360), "Diskurse produzieren keine Wahrheit.", font=sub_font, fill=(85, 86, 92))
d.text((tx, 396), "Sie produzieren Signale.", font=sub_font, fill=(15, 142, 134))
og.save(os.path.join(OUT, "og-image.png"), quality=92)

print("done")
