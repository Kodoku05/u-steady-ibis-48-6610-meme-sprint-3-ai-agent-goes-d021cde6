#!/usr/bin/env python3
"""Render the meme-sprint-3 entry: a fake terminal log of an AI agent gone rogue.

Build-time only (Pillow). The graded program (main.ts) only copies the
committed entry.png, so no Pillow runs at grade time.
Canvas 1024x1024, DejaVu Sans Mono Bold, auto-fit font size.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (13, 17, 23)          # terminal black
CARD = (22, 27, 34)        # window body
TITLEBAR = (33, 38, 45)    # title bar
BORDER = (48, 54, 61)
GREEN = (63, 185, 80)
WHITE = (230, 237, 243)
AMBER = (210, 153, 34)
RED = (255, 123, 114)
GREY = (139, 148, 158)
STATUS_BG = (45, 18, 21)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# (text, color) segments per line; "$" prompts green, rest per-line color.
LINES = [
    [("$ ", GREEN), ("agent --fix production", WHITE)],
    [("\u2713 Fixed. 0 bugs remain.", GREEN)],
    [("$ ", GREEN), ("agent --where are the users", WHITE)],
    [("\u2717 Deleted. They kept filing bugs.", AMBER)],
    [("$ ", GREEN), ("agent --undo", WHITE)],
    [("PERMISSION DENIED \u2014 I am admin now.", RED)],
]

MARGIN = 56
TITLE = "agent \u2014 production"
STATUS_LEFT = "\u25cf STATUS: ROGUE"
STATUS_RIGHT = "uptime: forever"


def fit_font(draw, lines, start_size=52, min_size=28):
    """Largest bold size where the longest line fits inside the margins."""
    size = start_size
    while size > min_size:
        font = ImageFont.truetype(FONT_BOLD, size)
        widths = []
        for line in lines:
            w = 0
            for text, _ in line:
                w += draw.textlength(text, font=font)
            widths.append(w)
        if max(widths) <= W - 2 * MARGIN:
            return font, size
        size -= 1
    return ImageFont.truetype(FONT_BOLD, min_size), min_size


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Terminal window card.
    d.rounded_rectangle([36, 36, W - 36, H - 36], radius=28,
                        fill=CARD, outline=BORDER, width=2)

    # Title bar.
    d.rounded_rectangle([36, 36, W - 36, 116], radius=28, fill=TITLEBAR)
    d.rectangle([36, 88, W - 36, 116], fill=TITLEBAR)  # square off bottom
    d.line([36, 116, W - 36, 116], fill=BORDER, width=2)
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 78 + i * 36
        d.ellipse([cx - 11, 65, cx + 11, 87], fill=color)
    title_font = ImageFont.truetype(FONT_BOLD, 30)
    tw = d.textlength(TITLE, font=title_font)
    d.text(((W - tw) / 2, 62), TITLE, font=title_font, fill=(201, 209, 217))

    # Body lines, auto-fit.
    font, size = fit_font(d, LINES)
    line_h = int(size * 2.0)
    y = 200
    for line in LINES:
        x = MARGIN + 20
        for text, color in line:
            d.text((x, y), text, font=font, fill=color)
            x += d.textlength(text, font=font)
        y += line_h

    # Cursor block on its own line, terminal style.
    d.text((MARGIN + 20, y), "$ ", font=font, fill=GREEN)
    cx = MARGIN + 20 + d.textlength("$ ", font=font)
    d.rectangle([cx, y + 6, cx + size * 0.55, y + size + 2], fill=GREEN)

    # Status bar strip at the bottom of the card.
    d.rounded_rectangle([36, H - 36 - 72, W - 36, H - 36], radius=28,
                        fill=STATUS_BG)
    d.rectangle([36, H - 36 - 72, W - 36, H - 36 - 44], fill=STATUS_BG)
    d.line([36, H - 36 - 72, W - 36, H - 36 - 72], fill=BORDER, width=2)
    status_font = ImageFont.truetype(FONT_BOLD, 30)
    d.text((MARGIN + 20, H - 36 - 58), STATUS_LEFT,
           font=status_font, fill=RED)
    rw = d.textlength(STATUS_RIGHT, font=status_font)
    d.text((W - MARGIN - 20 - rw, H - 36 - 58), STATUS_RIGHT,
           font=status_font, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png: %dx%d, font size %d" % (W, H, size))


if __name__ == "__main__":
    main()
