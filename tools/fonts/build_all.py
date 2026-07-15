#!/usr/bin/env python3
import os
from gen_vlw import generate

FONTS_DIR = "freefont-20120503"
OUT_DIR = "../../data"
os.makedirs(OUT_DIR, exist_ok=True)

SANS = f"{FONTS_DIR}/FreeSans.otf"
SANSB = f"{FONTS_DIR}/FreeSansBold.otf"
MONO = f"{FONTS_DIR}/FreeMono.otf"
MONOB = f"{FONTS_DIR}/FreeMonoBold.otf"

DIGITS = [c for c in "0123456789."]

JOBS = [
    # (font file, PIL size, output name, charset or None=full ASCII)
    # Second trim: another ~10% off the previous pass (still not matching
    # the old GFXFF footprint exactly - eyeballed/iterated against the real
    # display instead).
    (SANS,  15,  "FreeSans9",       None),
    (SANS,  21,  "FreeSans12",      None),
    (SANSB, 15,  "FreeSansBold9",   None),
    (SANSB, 21,  "FreeSansBold12",  None),
    (SANSB, 30,  "FreeSansBold18",  None),
    (SANSB, 41,  "FreeSansBold24",  None),
    (MONO,  17,  "FreeMono9",       None),
    (MONOB, 17,  "FreeMonoBold9",   None),
    (SANSB, 52,  "FreeSansBold36",  DIGITS),
    (SANSB, 75,  "FreeSansBold48",  DIGITS),
    (SANSB, 106, "FreeSansBold72",  DIGITS),
    (SANSB, 149, "FreeSansBold96",  DIGITS),
]

total = 0
for path, size, name, charset in JOBS:
    out_path = f"{OUT_DIR}/{name}.vlw"
    generate(path, size, out_path, charset=charset)
    total += os.path.getsize(out_path)

print(f"\nTotal size: {total} bytes ({total/1024:.1f} KB)")
