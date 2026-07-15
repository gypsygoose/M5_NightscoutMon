#!/usr/bin/env python3
"""Generate TFT_eSPI 'Smooth Font' (.vlw) files from a TTF/OTF source,
using Pillow to rasterize anti-aliased glyph bitmaps (8-bit alpha).

vlw format (big-endian), as documented in TFT_eSPI's In_eSPI.cpp loadFont():
  header (6 x int32): gCount, version, size, deprecated(0), ascent, descent
  per glyph (7 x int32): unicode, height, width, xAdvance, dY, dX, 0
  then glyph bitmaps back to back, 1 byte (alpha 0-255) per pixel, row-major
"""
import struct
import sys
from PIL import Image, ImageDraw, ImageFont

CHARSET = [chr(c) for c in range(0x21, 0x7F)]  # '!' .. '~'  (space handled by lib itself)


def measure_height(font_path, size, sample="8"):
    font = ImageFont.truetype(font_path, size)
    bbox = font.getbbox(sample)
    return bbox[3] - bbox[1]


def find_size_for_target_height(font_path, target_height, sample="8", lo=4, hi=500):
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        h = measure_height(font_path, mid, sample)
        if h < target_height:
            lo = mid + 1
        else:
            best = mid
            hi = mid - 1
    return best


def render_glyph(font, ch, pad):
    # Canvas big enough to hold any ascender/descender/overshoot without clipping.
    size_guess = font.size
    w = size_guess * 4
    h = size_guess * 5
    bx = pad
    by = size_guess * 3
    img = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(img)
    draw.text((bx, by), ch, font=font, fill=255, anchor="ls")
    adv = draw.textlength(ch, font=font)

    px = img.load()
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            if px[x, y]:
                if x < minx:
                    minx = x
                if x > maxx:
                    maxx = x
                if y < miny:
                    miny = y
                if y > maxy:
                    maxy = y

    if maxx < 0:
        # Blank glyph (shouldn't happen for printable ASCII, but be safe)
        return {
            "unicode": ord(ch),
            "width": 1,
            "height": 1,
            "xAdvance": max(1, round(adv)),
            "dY": 0,
            "dX": 0,
            "bitmap": bytes([0]),
        }

    width = maxx - minx + 1
    height = maxy - miny + 1
    bitmap = bytearray(width * height)
    for yy in range(height):
        for xx in range(width):
            bitmap[yy * width + xx] = px[minx + xx, miny + yy]

    return {
        "unicode": ord(ch),
        "width": width,
        "height": height,
        "xAdvance": round(adv),
        "dY": by - miny,
        "dX": minx - bx,
        "bitmap": bytes(bitmap),
    }


def generate(font_path, size, out_path, pad=16, charset=None):
    font = ImageFont.truetype(font_path, size)
    ascent, descent = font.getmetrics()

    glyphs = []
    for ch in (charset if charset is not None else CHARSET):
        g = render_glyph(font, ch, pad)
        for key in ("width", "height", "xAdvance"):
            if g[key] > 255:
                raise ValueError(f"{out_path}: {ch!r} {key}={g[key]} exceeds 255 (font too large)")
        if not (-127 <= g["dX"] <= 127):
            raise ValueError(f"{out_path}: {ch!r} dX={g['dX']} out of int8 range")
        glyphs.append(g)

    with open(out_path, "wb") as f:
        f.write(struct.pack(">iiiiii", len(glyphs), 11, size, 0, ascent, descent))
        for g in glyphs:
            f.write(
                struct.pack(
                    ">iiiiiii",
                    g["unicode"],
                    g["height"],
                    g["width"],
                    g["xAdvance"],
                    g["dY"],
                    g["dX"],
                    0,
                )
            )
        for g in glyphs:
            f.write(g["bitmap"])

    total_bitmap = sum(len(g["bitmap"]) for g in glyphs)
    print(f"{out_path}: size={size} ascent={ascent} descent={descent} "
          f"glyphs={len(glyphs)} bitmapBytes={total_bitmap} "
          f"fileBytes={24 + 28*len(glyphs) + total_bitmap}")


if __name__ == "__main__":
    font_path, size, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    generate(font_path, size, out_path)
