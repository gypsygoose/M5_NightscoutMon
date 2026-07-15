// Anti-aliased "Smooth Font" names for TFT_eSPI's loadFont().
//
// These are pre-rendered from GNU FreeFont (FreeSans/FreeSansBold/FreeMono/
// FreeMonoBold, GPLv3 + font exception) and stored as .vlw files in /data,
// uploaded to SPIFFS. Unlike the GFXFF vector fonts in Free_Fonts.h, these
// are alpha-blended per pixel, so large text no longer shows stair-stepped
// edges. See tools/fonts/README.md for how to regenerate them.
//
// Sizes below were chosen to match the pixel footprint of the GFXFF font
// (and, where the sketch previously used setTextSize() to blow up FSSB18/
// FSSB24, the resulting scaled-up size) they replace, so existing layout
// (fillRect clear boxes, datum positions) doesn't need to change.

#define NSF_S9    "FreeSans9"        // was FSS9
#define NSF_S12   "FreeSans12"       // was FSS12
#define NSF_SB9   "FreeSansBold9"    // was FSSB9
#define NSF_SB12  "FreeSansBold12"   // was FSSB12
#define NSF_SB18  "FreeSansBold18"   // was FSSB18
#define NSF_SB24  "FreeSansBold24"   // was FSSB24
#define NSF_M9    "FreeMono9"        // was FM9
#define NSF_MB9   "FreeMonoBold9"    // was FMB9

// Digits-only large fonts for the big glucose readings, replacing
// setFreeFont(FSSBxx) + setTextSize(2)/(4) (which scaled the vector font
// with blocky nearest-neighbour pixel doubling - the worst offender for
// the "staircase" artifact).
#define NSF_SB36  "FreeSansBold36"   // was FSSB18 @ textSize(2)
#define NSF_SB48  "FreeSansBold48"   // was FSSB24 @ textSize(2)
#define NSF_SB72  "FreeSansBold72"   // was FSSB18 @ textSize(4)
#define NSF_SB96  "FreeSansBold96"   // was FSSB24 @ textSize(4)
