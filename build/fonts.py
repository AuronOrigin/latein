"""Portabler Schriftauswahl fuer den PDF-Export.

Der PDF-Export setzt Unicode-faehige Schriften voraus: das Buch verwendet
Makronen (a-bar, e-bar), griechische Buchstaben in den Formenlehre-Tabellen,
Rahmenzeichen in den Kaesten und Verszeichen in den Skansionen. Die
eingebauten Schriften von ReportLab (Helvetica, Times, Courier) decken davon
fast nichts ab. Gesucht wird deshalb in dieser Reihenfolge:

  1. ``build/fontfiles/*.ttf`` - mitgelieferte, auf das Buch zugeschnittene
     Schnitte von DejaVu (frei weiterverteilbar, siehe ``build/fontfiles/LICENSE.txt``).
     Das ist der Normalfall: der Build laeuft auf jedem System gleich.
  2. Systemschriften: DejaVu zuerst, danach Times New Roman, Arial,
     Liberation und FreeSerif.
  3. Die Base-14-Schriften von ReportLab als Notnagel. Sie decken weder
     Makronen noch griechische Buchstaben ab; der Build meldet das als
     Warnung und die Glyphenpruefung schlaegt an.

Die mitgelieferten Schnitte erzeugt ``build/make_fonts.py`` aus einer
Systeminstallation von DejaVu. Wer eigene Schriften bevorzugt, legt sie
unter ``build/fontfiles/`` ab - der Renderer nimmt sie bevorzugt.
"""

from __future__ import annotations

import glob
import os
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED_DIR = os.path.join(HERE, "fontfiles")

# Verzeichnisse, in denen nach Schriften gesucht wird.
_FONT_DIRS = [
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    "/opt/homebrew/share/fonts",
    "/opt/local/share/fonts",
    "/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "C:/Windows/Fonts",
    os.path.expanduser("~/.local/share/fonts"),
    os.path.expanduser("~/Library/Fonts"),
    os.path.expanduser("~/.fonts"),
]

# Familie -> Beschreibung der Rollen (normal/fett) und der Notnagel.
# Die Reihenfolge der Kandidaten entscheidet: der erste Treffer gewinnt.
FAMILIES: dict[str, dict] = {
    "sans": {
        "alias": "BuchSans",
        "normal": {
            "bundle": "DejaVuSans.ttf",
            "system": [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/dejavu/DejaVuSans.ttf",
                "/usr/local/share/fonts/DejaVuSans.ttf",
                "/opt/homebrew/share/fonts/DejaVuSans.ttf",
                "/Library/Fonts/DejaVuSans.ttf",
                "/System/Library/Fonts/Supplemental/DejaVuSans.ttf",
                "C:/Windows/Fonts/DejaVuSans.ttf",
            ],
            "fallback": "Helvetica",
        },
        "bold": {
            "bundle": "DejaVuSans-Bold.ttf",
            "system": [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
                "/usr/local/share/fonts/DejaVuSans-Bold.ttf",
                "/opt/homebrew/share/fonts/DejaVuSans-Bold.ttf",
                "/Library/Fonts/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Supplemental/DejaVuSans-Bold.ttf",
                "C:/Windows/Fonts/DejaVuSans-Bold.ttf",
            ],
            "fallback": "Helvetica-Bold",
        },
    },
    "serif": {
        "alias": "BuchSerif",
        "normal": {
            "bundle": "DejaVuSerif.ttf",
            "system": [
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                "/usr/share/fonts/dejavu/DejaVuSerif.ttf",
                "/usr/local/share/fonts/DejaVuSerif.ttf",
                "/opt/homebrew/share/fonts/DejaVuSerif.ttf",
                "/Library/Fonts/DejaVuSerif.ttf",
                "/System/Library/Fonts/Supplemental/DejaVuSerif.ttf",
                "C:/Windows/Fonts/DejaVuSerif.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
            ],
            "fallback": "Times-Roman",
        },
        "bold": {
            "bundle": "DejaVuSerif-Bold.ttf",
            "system": [
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                "/usr/share/fonts/dejavu/DejaVuSerif-Bold.ttf",
                "/usr/local/share/fonts/DejaVuSerif-Bold.ttf",
                "/opt/homebrew/share/fonts/DejaVuSerif-Bold.ttf",
                "/Library/Fonts/DejaVuSerif-Bold.ttf",
                "/System/Library/Fonts/Supplemental/DejaVuSerif-Bold.ttf",
                "C:/Windows/Fonts/DejaVuSerif-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
            ],
            "fallback": "Times-Bold",
        },
    },
    "mono": {
        "alias": "BuchMono",
        "normal": {
            "bundle": "DejaVuSansMono.ttf",
            "system": [
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
                "/usr/local/share/fonts/DejaVuSansMono.ttf",
                "/opt/homebrew/share/fonts/DejaVuSansMono.ttf",
                "/Library/Fonts/DejaVuSansMono.ttf",
                "/System/Library/Fonts/Supplemental/DejaVuSansMono.ttf",
                "C:/Windows/Fonts/DejaVuSansMono.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            ],
            "fallback": "Courier",
        },
        "bold": {
            "bundle": "DejaVuSansMono-Bold.ttf",
            "system": [
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                "/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf",
                "/usr/local/share/fonts/DejaVuSansMono-Bold.ttf",
                "/opt/homebrew/share/fonts/DejaVuSansMono-Bold.ttf",
                "/Library/Fonts/DejaVuSansMono-Bold.ttf",
                "/System/Library/Fonts/Supplemental/DejaVuSansMono-Bold.ttf",
                "C:/Windows/Fonts/DejaVuSansMono-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
            ],
            "fallback": "Courier-Bold",
        },
    },
}


@dataclass
class FontSet:
    """Ergebnis der Schriftenauflösung."""

    fonts: dict[str, str] = field(default_factory=dict)      # Rolle -> ReportLab-Name
    files: dict[str, str] = field(default_factory=dict)      # Rolle -> Dateipfad
    sources: dict[str, str] = field(default_factory=dict)    # Rolle -> Herkunft
    notes: list[str] = field(default_factory=list)

    @property
    def unicode_capable(self) -> bool:
        """True, wenn mindestens eine Rolle eine echte Unicode-Schrift nutzt."""
        return any(self.files.get(role) for role in self.fonts)

    def describe(self) -> str:
        parts = []
        for role in sorted(self.fonts):
            src = self.sources.get(role, "?")
            parts.append(f"{role}={self.fonts[role]} ({src})")
        return ", ".join(parts)


def _find_file(system_paths: list[str], filename: str) -> str | None:
    """Sucht eine Schriftdatei: erst die bekannten Pfade, dann die Font-Verzeichnisse."""
    for path in system_paths:
        if os.path.isfile(path):
            return path
    for directory in _FONT_DIRS:
        if not os.path.isdir(directory):
            continue
        for hit in sorted(glob.glob(os.path.join(directory, filename))):
            if os.path.isfile(hit):
                return hit
    for directory in _FONT_DIRS:
        if not os.path.isdir(directory):
            continue
        for hit in sorted(glob.glob(os.path.join(directory, "**", filename), recursive=True)):
            if os.path.isfile(hit):
                return hit
    return None


def resolve_fonts(quiet: bool = False) -> FontSet:
    """Ermittelt die verfuegbaren Schriften und registriert sie bei ReportLab."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    fset = FontSet()
    registered = set(pdfmetrics.getRegisteredFontNames())

    for family, spec in FAMILIES.items():
        alias = spec["alias"]
        normal = spec["normal"]
        bold = spec["bold"]

        n_path = os.path.join(BUNDLED_DIR, normal["bundle"])
        b_path = os.path.join(BUNDLED_DIR, bold["bundle"])

        if os.path.isfile(n_path) and os.path.isfile(b_path):
            n_src, b_src = n_path, b_path
            origin = "mitgeliefert"
        else:
            n_found = _find_file(normal["system"], normal["bundle"])
            b_found = _find_file(bold["system"], bold["bundle"])
            if n_found and b_found:
                n_src, b_src = n_found, b_found
                origin = "System"
            else:
                n_src = b_src = None
                origin = "Notnagel"

        n_alias = f"{alias}"
        b_alias = f"{alias}-Bold"

        if n_src and b_src:
            if n_alias not in registered:
                pdfmetrics.registerFont(TTFont(n_alias, n_src))
            if b_alias not in registered:
                pdfmetrics.registerFont(TTFont(b_alias, b_src))
            fset.fonts[f"{family}"] = n_alias
            fset.fonts[f"{family}-bold"] = b_alias
            fset.files[f"{family}"] = n_src
            fset.files[f"{family}-bold"] = b_src
            fset.sources[f"{family}"] = f"{origin}: {os.path.basename(n_src)}"
            fset.sources[f"{family}-bold"] = f"{origin}: {os.path.basename(b_src)}"
            # Italic gibt es bei DejaVu nicht; Kursiv wird auf die Normalschrift
            # abgebildet, damit <i> im PDF nicht in einer Fehlermeldung endet.
            pdfmetrics.registerFontFamily(
                alias, normal=n_alias, bold=b_alias, italic=n_alias, boldItalic=b_alias)
        else:
            fset.fonts[family] = normal["fallback"]
            fset.fonts[f"{family}-bold"] = bold["fallback"]
            fset.sources[family] = "Notnagel"
            fset.sources[f"{family}-bold"] = "Notnagel"
            fset.notes.append(
                f"Keine Unicode-Schrift fuer '{family}' gefunden - "
                f"Rueckfall auf {normal['fallback']}. Makronen, griechische "
                "Buchstaben und Rahmenzeichen fehlen dann im PDF.")

    if not quiet:
        print(f"FONTS -> {fset.describe()}")
        for note in fset.notes:
            print(f"  ! {note}")

    return fset


def _char_map(font_name: str) -> dict | None:
    """Zeichen-Tabelle einer registrierten Schrift (None, wenn nicht pruefbar)."""
    from reportlab.pdfbase import pdfmetrics
    try:
        font = pdfmetrics.getFont(font_name)
    except Exception:
        return None
    face = getattr(font, "face", None)
    return getattr(face, "charToGlyph", None)


def missing_glyphs(text: str, fset: FontSet) -> dict[str, set[str] | None]:
    """Pro Rolle: die Zeichen aus *text*, die die Schrift nicht darstellen kann.

    Der Wert None bedeutet: diese Rolle ist nicht auf Zeichenebene pruefbar
    (das trifft auf die eingebauten Type-1-Schriften von ReportLab zu).
    """
    out: dict[str, set[str] | None] = {}
    for role, name in fset.fonts.items():
        c2g = _char_map(name)
        if c2g is None:
            out[role] = None
            continue
        out[role] = {ch for ch in set(text)
                     if ch not in "\n\r\t" and ord(ch) not in c2g}
    return out


def coverage(text: str, fset: FontSet) -> tuple[set[str], set[str], dict[str, set[str] | None]]:
    """Prueft die Glyphenabdeckung.

    Rueckgabe: (in_keiner_schrift, irgendwo_fehlend, pro_rolle).
    *in_keiner_schrift* sind Zeichen, die keine der pruefbaren Schriften
    darstellen kann - ein echter Fehler, das PDF verliert sie.
    *irgendwo_fehlend* sind Zeichen, die in einzelnen Rollen fehlen (z. B. in
    der Serifenschrift); das ist meist unkritisch, wird aber genannt.
    """
    per_role = missing_glyphs(text, fset)
    checkable = [chars for chars in per_role.values() if chars is not None]
    if not checkable:
        return set(), set(), per_role
    # Fehlt in allen pruefbaren Rollen -> Schnitt der Mengen.
    everywhere = set.intersection(*checkable)
    # Fehlt in mindestens einer Rolle -> Vereinigung der Mengen.
    somewhere = set().union(*checkable)
    return everywhere, somewhere, per_role
