# Smooth font generator

Regenerates the anti-aliased `.vlw` fonts in `/data` (TFT_eSPI "Smooth Font"
format) from GNU FreeFont, the same font family the existing `Free_Fonts.h`
vector fonts (`FSSB24` etc.) were generated from. Unlike those, `.vlw`
glyphs carry an 8-bit alpha value per pixel, so text is alpha-blended
against the background instead of being a hard 1-bit stencil — no more
stair-stepped edges on large text.

## Usage

```
curl -LO https://ftp.gnu.org/gnu/freefont/freefont-otf-20120503.tar.gz
tar xzf freefont-otf-20120503.tar.gz
pip install --user Pillow   # only dependency
python3 build_all.py        # writes ../../data/*.vlw
```

`gen_vlw.py` does the actual rasterizing/packing; `build_all.py` just lists
which (font, pixel size, glyph set) to render into which output file — see
`SmoothFonts.h` for what each file is used for and why that size was chosen.

## Regenerating a font at a different size

Call `generate()` from `gen_vlw.py` directly, or add a row to the `JOBS`
list in `build_all.py`. `find_size_for_target_height()` in `gen_vlw.py` can
binary-search for the PIL point size that produces a given glyph pixel
height, which is how the sizes in `build_all.py` were picked (matched
against the old GFXFF font's line height / glyph bbox height so existing
`fillRect` clear boxes and datum positions in the sketch didn't need to
change).

## License

GNU FreeFont is GPLv3 with a font-embedding exception (embedding it in a
document/firmware does not require that firmware to be GPL) — see
`freefont-20120503/COPYING` and `README` in the downloaded archive, or
https://www.gnu.org/software/freefont/. Same license already covers the
`Free_Fonts.h`/GFXFF fonts bundled with the M5Stack library.
