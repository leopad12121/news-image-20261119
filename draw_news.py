#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up 19 November 2026.

PIL only, no network, no timestamps, no randomness: running this script
twice produces a byte-identical entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
OUT_PATH = "entry.png"

PAPER = (247, 243, 234)      # warm newsprint
INK = (26, 28, 34)           # near-black text
NAVY = (27, 35, 64)          # masthead / panels
GOLD = (233, 196, 90)        # masthead accent
RED = (178, 34, 34)          # kickers and red icons
RULE = (180, 172, 155)       # thin divider lines

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font_obj, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font_obj) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_text_block(draw, x, y, text, font_obj, fill, max_width, line_spacing=6):
    """Draw wrapped text starting at (x, y); return y just below the block."""
    for line in wrap(draw, text, font_obj, max_width):
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_spacing
    return y


def draw_person(draw, cx, top, scale, head_fill, body_fill):
    """A minimal person glyph: circle head above a half-disc torso."""
    head_r = int(13 * scale)
    head_cy = top + head_r
    draw.ellipse(
        [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
        fill=head_fill,
    )
    torso_top = head_cy + head_r + int(4 * scale)
    torso_bottom = torso_top + int(16 * scale)
    torso_w = int(26 * scale)
    draw.pieslice(
        [cx - torso_w, torso_top, cx + torso_w, torso_bottom + int(16 * scale)],
        start=180,
        end=360,
        fill=body_fill,
    )


def draw_scales(draw, x, y, size, color):
    """Simple justice scales inside a square starting at (x, y)."""
    cx = x + size // 2
    top = y + int(size * 0.16)
    bottom = y + int(size * 0.84)
    draw.line([cx, top, cx, bottom], fill=color, width=4)
    draw.line([x + int(size * 0.16), top + 8, x + int(size * 0.84), top + 8],
              fill=color, width=4)
    draw.line([x + int(size * 0.16), top + 8, x + int(size * 0.16), top + 34],
              fill=color, width=3)
    draw.line([x + int(size * 0.84), top + 8, x + int(size * 0.84), top + 34],
              fill=color, width=3)
    for pan_x in (x + int(size * 0.16), x + int(size * 0.84)):
        draw.pieslice([pan_x - 16, top + 30, pan_x + 16, top + 52],
                      start=0, end=180, fill=color)
    draw.rectangle([cx - 22, bottom - 4, cx + 22, bottom + 4], fill=color)


def draw_target(draw, x, y, size, color):
    """Concentric target rings with a small centre dot."""
    cx, cy = x + size // 2, y + size // 2
    for r in (34, 24, 14):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=color, width=4)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)


def draw_cyclone(draw, x, y, size, color):
    """A spiral-ish storm glyph made of three arcs."""
    cx, cy = x + size // 2, y + size // 2
    for r, start, end in ((32, 200, 20), (23, 20, 200), (14, 200, 20)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=start, end=end,
                 fill=color, width=5)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)


def draw_star(draw, x, y, size, color):
    """A five-point star built from polygon points."""
    import math
    cx, cy = x + size // 2, y + size // 2
    outer, inner = size * 0.42, size * 0.18
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = outer if i % 2 == 0 else inner
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    draw.polygon(points, fill=color)


ICON_DRAWERS = {
    "scales": draw_scales,
    "target": draw_target,
    "cyclone": draw_cyclone,
    "star": draw_star,
}

STORIES = [
    {
        "kicker": "THE HAGUE  \u00b7  JUSTICE",
        "headline": "UN top court: Myanmar committed genocide",
        "deck": "The top UN court rules Myanmar committed genocide against the Rohingya.",
        "icon": "scales",
        "color": RED,
    },
    {
        "kicker": "MIDDLE EAST",
        "headline": "Houthi missile damages Riyadh's tower",
        "deck": "A Houthi attack damages a Riyadh tower housing the sovereign wealth fund.",
        "icon": "target",
        "color": NAVY,
    },
    {
        "kicker": "SOUTH ASIA  \u00b7  WEATHER",
        "headline": "Cyclone Akvan nears India's east coast",
        "deck": "Landfall due Friday on the Andhra Pradesh-Odisha coast, winds 90-100 km/h.",
        "icon": "cyclone",
        "color": NAVY,
    },
    {
        "kicker": "CULTURE  \u00b7  GAMES",
        "headline": "GTA VI launches after a 13-year wait",
        "deck": "Grand Theft Auto VI launches Thursday to global fanfare after 13 years.",
        "icon": "star",
        "color": RED,
    },
]

FOOTER_ITEMS = [
    "Three oil tankers hit mines near Hormuz",
    "Voyager 1 one light-day out",
    "Jeffries set to be first Black House Speaker",
    "Denmark in Arctic deal with US",
]


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    draw.rectangle([0, 0, WIDTH, 150], fill=NAVY)
    title_font = font(SERIF, 66)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_font)
    draw.text(((WIDTH - tw) / 2, 22), title, font=title_font, fill=(255, 255, 255))
    date_font = font(SANS_BOLD, 30)
    draw.text((36, 100), "THURSDAY  19  NOVEMBER  2026",
              font=date_font, fill=GOLD)
    section_font = font(SANS_BOLD, 26)
    section = "WORLD NEWS"
    draw.text((WIDTH - 36 - draw.textlength(section, font=section_font), 102),
              section, font=section_font, fill=(190, 196, 214))

    # ---- Lead story -----------------------------------------------------
    lead_x, lead_y = 36, 170
    lead_w = 640
    kicker_font = font(SANS_BOLD, 24)
    draw.text((lead_x, lead_y), "ASIA-PACIFIC  \u00b7  DIPLOMACY",
              font=kicker_font, fill=RED)
    head_font = font(SERIF, 44)
    y = draw_text_block(draw, lead_x, lead_y + 38,
                        "Trump, Xi and Putin\nissue joint declaration",
                        head_font, INK, lead_w, line_spacing=8)
    deck_font = font(SANS, 25)
    draw_text_block(
        draw, lead_x, y + 8,
        "The three leaders hold their first-ever three-way summit in "
        "Shenzhen, pledging dialogue on nuclear risks.",
        deck_font, INK, lead_w, line_spacing=8)

    # Lead illustration: navy panel with three leaders as person glyphs.
    panel_x, panel_y = 712, 170
    panel_w, panel_h = 276, 236
    draw.rounded_rectangle([panel_x, panel_y, panel_x + panel_w,
                            panel_y + panel_h], radius=14, fill=NAVY)
    for cx in (panel_x + 62, panel_x + 138, panel_x + 214):
        draw_person(draw, cx, panel_y + 52, 1.0, GOLD, GOLD)
    draw.line([panel_x + 40, panel_y + 196, panel_x + panel_w - 40,
               panel_y + 196], fill=GOLD, width=5)

    # ---- Divider under the lead ----------------------------------------
    draw.line([36, 420, WIDTH - 36, 420], fill=RULE, width=2)

    # ---- Four-story grid ------------------------------------------------
    grid_top = 438
    cell_w, cell_h = 476, 190
    col_xs = (36, 512)
    row_ys = (grid_top, grid_top + cell_h + 10)
    for idx, story in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        x = col_xs[col]
        y = row_ys[row]
        icon_size = 92
        draw.rounded_rectangle([x, y, x + icon_size, y + icon_size],
                               radius=12, fill=story["color"])
        ICON_DRAWERS[story["icon"]](draw, x + 6, y + 6, icon_size - 12,
                                    (255, 255, 255))
        text_x = x + icon_size + 16
        text_w = cell_w - icon_size - 16
        draw.text((text_x, y + 2), story["kicker"], font=kicker_font, fill=RED)
        story_head = font(SERIF, 26)
        hy = draw_text_block(draw, text_x, y + 36, story["headline"],
                             story_head, INK, text_w, line_spacing=4)
        draw_text_block(draw, text_x, hy + 6, story["deck"],
                        font(SANS, 19), INK, text_w, line_spacing=4)
        if col == 0:
            draw.line([x + cell_w + 4, y + 4, x + cell_w + 4, y + cell_h - 12],
                      fill=RULE, width=2)

    # ---- Footer ---------------------------------------------------------
    foot_y = 860
    draw.line([36, foot_y, WIDTH - 36, foot_y], fill=RULE, width=2)
    also_font = font(SANS, 21)
    also_text = "Also: " + "  \u00b7  ".join(FOOTER_ITEMS)
    draw_text_block(draw, 36, foot_y + 14, also_text, also_font, INK,
                    WIDTH - 72, line_spacing=4)
    draw.text((36, HEIGHT - 34), "Drawn from reports published on 19 November 2026.",
              font=font(SANS, 18), fill=(110, 106, 96))

    img.save(OUT_PATH, "PNG")
    print(f"Saved {OUT_PATH} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
