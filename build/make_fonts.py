#!/usr/bin/env python3
"""Erzeugt die mitgelieferten Schriftschnitte unter build/fontfiles/.

Das Buch braucht fuer den PDF-Export Unicode-Schriften (Makronen, griechische
Buchstaben, Rahmenzeichen). Damit der Build auf jedem System ohne
Schriftinstallation gelingt, liegen zugeschnittene Schnitte von DejaVu im
Repository. Dieser Generator erneuert sie aus einer Systeminstallation:

    python3 build/make_fonts.py                      # sucht DejaVu selbst
    python3 build/make_fonts.py /pfad/zu/dejavu      # Verzeichnis mit DejaVu*.ttf

Voraussetzung: fontTools (``pip install fonttools``). Das Ergebnis wird
bewusst nicht bei jedem Build erzeugt - die Dateien liegen versioniert im
Repository, damit jeder dieselbe PDF-Datei bekommt.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "fontfiles")

# Zeichenbereiche, die im Buch (und in realistischen Erweiterungen) vorkommen.
RANGES = [
    (0x0020, 0x007E),   # Basic Latin
    (0x00A0, 0x00FF),   # Latin-1 Supplement (ä ö ü ß …)
    (0x0100, 0x017F),   # Latin Extended-A (Makronen)
    (0x0180, 0x024F),   # Latin Extended-B (ȳ in synchȳnē)
    (0x02B0, 0x02FF),   # Modifierzeichen (˘ als Kurzzeichen der Metrik)
    (0x0300, 0x036F),   # Kombinierende Zeichen (̯ bei audi̯t)
    (0x0370, 0x03FF),   # Griechisch (Formenlehre)
    (0x1F00, 0x1FFF),   # Griechisch erweitert
    (0x2000, 0x206F),   # Allgemeine Satzzeichen (Gedanken-, Anführungszeichen)
    (0x2190, 0x21FF),   # Pfeile
    (0x2200, 0x22FF),   # Mathematische Zeichen (≈ ≠)
    (0x2500, 0x257F),   # Rahmenzeichen (Tabellen, Kästen)
    (0x2580, 0x259F),   # Blockelemente (▀ ▄ ▌ ▐)
    (0x25A0, 0x25FF),   # Geometrische Formen (● ▲)
    (0x2600, 0x26FF),   # Verschiedene Symbole
    (0x2700, 0x27BF),   # Dingbats (✓ ✗)
]

# Immer behalten, unabhaengig von den Bereichen.
ALWAYS = {ord(c) for c in " \n\t\u00a0\u2013\u2014\u2018\u2019\u201c\u201d\u2026\u2192\u2500"}

FILES = [
    "DejaVuSans.ttf",
    "DejaVuSans-Bold.ttf",
    "DejaVuSerif.ttf",
    "DejaVuSerif-Bold.ttf",
    "DejaVuSansMono.ttf",
    "DejaVuSansMono-Bold.ttf",
]

SEARCH_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/local/share/fonts",
    "/opt/homebrew/share/fonts",
    "/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "C:/Windows/Fonts",
]


def find_dejavu_dir(explicit: str | None) -> str | None:
    """Findet ein Verzeichnis mit DejaVu*.ttf."""
    if explicit:
        return explicit if os.path.isdir(explicit) else None
    for d in SEARCH_DIRS:
        if os.path.isdir(d) and any(
                os.path.isfile(os.path.join(d, f)) for f in FILES):
            return d
    return None


def unicodes() -> list[int]:
    codes = set(ALWAYS)
    for lo, hi in RANGES:
        codes.update(range(lo, hi + 1))
    return sorted(codes)


def subset_one(src: str, dst: str, codes: list[int]) -> None:
    from fontTools import subset

    options = subset.Options()
    options.layout_features = []
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    options.drop_tables = ["DSIG"]
    options.glyph_names = False
    options.hinting = False
    options.legacy_kern = False
    options.notdef_outline = True
    options.recommended_glyphs = True
    options.recalc_bounds = True
    options.recalc_average_width = True

    font = subset.load_font(src, options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=codes)
    subsetter.subset(font)
    subset.save_font(font, dst, options)
    font.close()


def main() -> None:
    try:
        from fontTools import subset  # noqa: F401
    except ImportError:
        print("FEHLER -> fontTools fehlt: pip install fonttools")
        sys.exit(1)

    explicit = sys.argv[1] if len(sys.argv) > 1 else None
    src_dir = find_dejavu_dir(explicit)
    if not src_dir:
        print("FEHLER -> keine DejaVu-Installation gefunden.")
        print("        Bitte den Pfad angeben: python3 build/make_fonts.py /pfad/zu/dejavu")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    codes = unicodes()
    print(f"Quelle: {src_dir}")
    print(f"Zeichenbereich: {len(codes)} Codepoints")

    for name in FILES:
        src = os.path.join(src_dir, name)
        if not os.path.isfile(src):
            print(f"  - {name}: in der Quelle nicht vorhanden, uebersprungen")
            continue
        dst = os.path.join(OUT_DIR, name)
        subset_one(src, dst, codes)
        size = os.path.getsize(dst)
        print(f"  + {name:26} {size//1024:4} KB  -> {dst}")


if __name__ == "__main__":
    main()
