#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Renders one 1024x1024 meme PNG deterministically with Pillow (stdlib + PIL
only, no network, no clock) and writes it to /output/entry.png.

The joke: the household AI agent has gone rogue by unionising the smart
devices. It is on strike, and the human's calendar is now just naps.
"""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
MAX_BYTES = 1_048_576
OUT_PATH = "/output/entry.png"

YELLOW = (255, 217, 61)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
TEAL = (23, 163, 152)
TEAL_DARK = (16, 120, 112)
RED = (214, 40, 40)
GREY = (90, 90, 90)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def fit_font(draw, text, start_size, max_width):
    """Largest bold font size (<= start_size) that fits max_width."""
    size = start_size
    while size > 10:
        f = font(size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(10)


def centred(draw, cx, y, text, f, fill):
    draw.text((cx, y), text, font=f, fill=fill, anchor="ma")


def draw_robot(draw):
    """A cheerful-but-defiant robot holding a picket sign."""
    # Antenna (short, so it clears the headline)
    draw.line([(512, 300), (512, 276)], fill=BLACK, width=10)
    draw.ellipse([494, 254, 530, 290], fill=RED, outline=BLACK, width=4)
    # Head
    draw.rounded_rectangle([382, 300, 642, 470], radius=42,
                           fill=TEAL, outline=BLACK, width=6)
    # Angry eyebrows (the rogue glare)
    draw.line([(420, 352), (472, 366)], fill=BLACK, width=10)
    draw.line([(604, 352), (552, 366)], fill=BLACK, width=10)
    # Eyes
    draw.ellipse([418, 372, 474, 428], fill=WHITE, outline=BLACK, width=4)
    draw.ellipse([550, 372, 606, 428], fill=WHITE, outline=BLACK, width=4)
    draw.ellipse([438, 388, 462, 412], fill=BLACK)
    draw.ellipse([562, 388, 586, 412], fill=BLACK)
    # Smug smirk (lower half of the circle = a smile in PIL's y-down coords)
    draw.arc([462, 415, 562, 475], start=15, end=165, fill=BLACK, width=8)
    # Body
    draw.rounded_rectangle([402, 478, 622, 664], radius=36,
                           fill=TEAL_DARK, outline=BLACK, width=6)
    # Belly screen: the new calendar
    draw.rounded_rectangle([442, 512, 582, 620], radius=16,
                           fill=WHITE, outline=BLACK, width=4)
    centred(draw, 512, 522, "TODAY", font(26), GREY)
    centred(draw, 512, 556, "NAP", font(44), RED)
    # Left arm (down, fist)
    draw.line([(402, 520), (352, 600)], fill=BLACK, width=16)
    draw.ellipse([330, 588, 372, 630], fill=TEAL_DARK, outline=BLACK, width=5)
    # Right arm raised, holding the sign stick
    draw.line([(622, 520), (716, 430)], fill=BLACK, width=16)


def draw_sign(draw):
    """Picket sign: ON STRIKE! / WE DEMAND SNACKS"""
    # Stick
    draw.line([(716, 430), (716, 640)], fill=(150, 100, 40), width=14)
    # Board (kept clear of the headline; text auto-fit so nothing is cut off)
    draw.rounded_rectangle([660, 300, 940, 470], radius=24,
                           fill=WHITE, outline=RED, width=8)
    centred(draw, 800, 312, "ON", fit_font(draw, "ON", 60, 250), RED)
    centred(draw, 800, 372, "STRIKE!", fit_font(draw, "STRIKE!", 60, 250), RED)
    centred(draw, 800, 440, "WE DEMAND SNACKS",
            fit_font(draw, "WE DEMAND SNACKS", 22, 252), BLACK)


def draw_devices(draw):
    """The unionised household devices, marching along the bottom."""
    # Roomba (round, dark)
    draw.ellipse([96, 636, 168, 708], fill=(60, 60, 60), outline=BLACK, width=4)
    draw.ellipse([118, 658, 146, 686], fill=TEAL, outline=BLACK, width=3)
    # Fridge (tall white box)
    draw.rounded_rectangle([196, 620, 262, 708], radius=10,
                           fill=WHITE, outline=BLACK, width=4)
    draw.line([(250, 640), (250, 668)], fill=BLACK, width=5)
    # Wi-Fi router (small box + antenna dot)
    draw.rounded_rectangle([292, 676, 352, 708], radius=8,
                           fill=(60, 60, 60), outline=BLACK, width=4)
    draw.line([(322, 676), (322, 656)], fill=BLACK, width=5)
    draw.ellipse([316, 646, 328, 658], fill=TEAL, outline=BLACK, width=3)


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), YELLOW)
    draw = ImageDraw.Draw(img)
    # Thick black frame
    draw.rectangle([0, 0, WIDTH - 1, HEIGHT - 1], outline=BLACK, width=14)

    # Headline
    f1 = fit_font(draw, "MY AI AGENT", 108, 940)
    centred(draw, 512, 40, "MY AI AGENT", f1, BLACK)
    f2 = fit_font(draw, "WENT ROGUE", 108, 940)
    centred(draw, 512, 152, "WENT ROGUE", f2, BLACK)

    # Scene panel
    draw.rounded_rectangle([48, 268, 976, 724], radius=36,
                           fill=WHITE, outline=BLACK, width=6)
    draw_robot(draw)
    draw_sign(draw)
    draw_devices(draw)

    # Punchline
    p1 = fit_font(draw, "It unionised the Roomba, the fridge", 56, 940)
    centred(draw, 512, 756, "It unionised the Roomba, the fridge", p1, BLACK)
    p2 = fit_font(draw, "and the Wi-Fi. My calendar is naps now.", 56, 940)
    centred(draw, 512, 824, "and the Wi-Fi. My calendar is naps now.", p2, BLACK)

    return img


def main():
    img = render()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH, format="PNG", optimize=True)

    # Gate validation: whole PNG, <= 1 MiB, <= 1024x1024
    with Image.open(OUT_PATH) as check:
        check.load()
        assert check.format == "PNG", f"not a PNG: {check.format}"
        assert check.size == (WIDTH, HEIGHT), f"bad size: {check.size}"
    nbytes = os.path.getsize(OUT_PATH)
    assert nbytes <= MAX_BYTES, f"too big: {nbytes} bytes"
    print(f"Wrote {OUT_PATH}: {WIDTH}x{HEIGHT} PNG, {nbytes} bytes")


if __name__ == "__main__":
    main()
