#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world news
of Thursday 19 November 2026. Run: python3 draw_news.py  ->  entry.png
Only Pillow is needed at draw time; the submitted entrypoint (main.py) is
stdlib-only and just copies the finished image into the output directory."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 92, 98)
RULE = (180, 175, 160)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def icon_radar(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = (x1 - x0) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=5)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
              outline=c, width=3)
    d.line([(cx, cy), (cx + r - 6, cy - r + 10)], fill=c, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=c)
    d.ellipse([cx + r - 14, cy + 4, cx + r - 4, cy + 14], fill=c)


def icon_summit(d, box, c):
    x0, y0, x1, y1 = box
    for cx in (x0 + 22, (x0 + x1) // 2, x1 - 22):
        d.ellipse([cx - 13, y0 + 14, cx + 13, y0 + 40], fill=c)
        d.pieslice([cx - 18, y0 + 44, cx + 18, y0 + 78], 180, 360, fill=c)
    d.line([(x0 + 4, y1 - 8), (x1 - 4, y1 - 8)], fill=c, width=5)


def icon_alert(d, box, c):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    d.polygon([(cx, y0 + 8), (x1 - 8, y1 - 12), (x0 + 8, y1 - 12)], fill=c)
    d.rectangle([cx - 4, y0 + 34, cx + 4, y0 + 58], fill=(255, 255, 255))
    d.ellipse([cx - 5, y0 + 64, cx + 5, y0 + 74], fill=(255, 255, 255))


def icon_vote(d, box, c):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 + 10, y0 + 26, x1 - 10, y1 - 10], 6,
                        outline=c, width=6)
    d.rectangle([x0 + 30, y0 + 8, x1 - 30, y0 + 28], fill=c)
    d.line([(x0 + 22, y0 + 52), (x0 + 38, y0 + 70), (x1 - 20, y0 + 34)],
           fill=c, width=7)


def icon_cyclone(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r, start in ((30, 20), (22, 140), (14, 260)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 220,
              fill=c, width=6)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=c)


def icon_star(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    import math
    pts = []
    for i in range(10):
        r = 38 if i % 2 == 0 else 16
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=c)


def story_block(d, x, y, w, h, kicker, headline, body, icon, accent):
    """One story: icon tile left, kicker + headline + body right."""
    tile = 92
    d.rounded_rectangle([x, y, x + tile, y + tile], 10, fill=accent)
    icon(d, (x + 8, y + 8, x + tile - 8, y + tile - 8), (255, 255, 255))
    tx = x + tile + 16
    tw = w - tile - 16
    d.text((tx, y + 2), kicker, font=font(SANS_B, 19), fill=RED)
    y2 = para(d, tx, y + 30, headline, font(SANS_B, 27), tw, 33,
              max_lines=2)
    para(d, tx, y2 + 4, body, font(SANS, 21), tw, 27, max_lines=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((36, 22), "THE WORLD IN ONE DAY", font=font(SERIF, 58),
           fill=(255, 255, 255))
    d.text((36, 100), "THURSDAY  19  NOVEMBER  2026",
           font=font(SANS_B, 26), fill=(255, 214, 90))
    d.text((W - 36, 104), "WORLD NEWS", font=font(SANS_B, 24),
           fill=(200, 205, 220), anchor="ra")

    # Lead story
    y = 176
    d.text((36, y), "ASIA-PACIFIC  ·  DIPLOMACY", font=font(SANS_B, 20),
           fill=RED)
    y = para(d, 36, y + 30,
             "Trump, Xi and Putin issue joint declaration",
             font(SERIF, 44), 700, 52, max_lines=2)
    para(d, 36, y + 8,
         "The three leaders hold their first-ever three-way summit in "
         "Shenzhen at APEC and pledge dialogue on nuclear risks and "
         "stable energy flows.",
         font(SANS, 24), 700, 32, max_lines=3)
    d.rounded_rectangle([780, 176, 988, 384], 12, fill=NAVY)
    icon_summit(d, (796, 192, 972, 368), (255, 214, 90))
    d.line([(36, 420), (988, 420)], fill=RULE, width=2)

    # Four more stories in a 2x2 grid
    stories = [
        ("THE HAGUE  ·  JUSTICE", "UN top court: Myanmar committed genocide",
         "The top UN court rules Myanmar committed genocide against "
         "the Rohingya.",
         icon_alert, (178, 34, 34)),
        ("MIDDLE EAST", "Houthi missile damages Riyadh's tallest tower",
         "A Riyadh skyscraper housing the sovereign wealth fund is "
         "damaged in a Houthi attack.",
         icon_radar, (20, 33, 61)),
        ("SOUTH ASIA  ·  WEATHER", "Cyclone Akvan nears India's east coast",
         "Landfall is due Friday on the Andhra Pradesh-Odisha coast, "
         "winds 90-100 km/h.",
         icon_cyclone, (20, 33, 61)),
        ("CULTURE  ·  GAMES", "GTA VI launches after a 13-year wait",
         "Grand Theft Auto VI launches on Thursday to global fanfare "
         "after a 13-year wait.",
         icon_star, (178, 34, 34)),
    ]
    gx, gy = 36, 444
    cw, ch = 466, 236
    for i, (kicker, headline, body, icon, accent) in enumerate(stories):
        x = gx + (i % 2) * (cw + 20)
        yy = gy + (i // 2) * (ch + 16)
        story_block(d, x, yy, cw, ch, kicker, headline, body, icon, accent)
        if i % 2 == 0:
            d.line([(x + cw + 10, yy + 6), (x + cw + 10, yy + ch - 6)],
                   fill=RULE, width=2)

    d.line([(36, 934), (988, 934)], fill=RULE, width=2)
    d.text((36, 950),
           "Also: Three oil tankers hit mines near Hormuz  ·  Voyager 1 "
           "one light-day out",
           font=font(SANS, 19), fill=GREY)
    d.text((36, 978),
           "Jeffries set to be first Black House Speaker  ·  Denmark in "
           "Arctic deal with US",
           font=font(SANS, 19), fill=GREY)
    d.text((36, 1004), "Drawn from reports published on 19 November 2026.",
           font=font(SANS, 18), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
