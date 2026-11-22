#!/usr/bin/env python3
"""Prueft das Vokabelverzeichnis gegen die Wortschatz-Kaesten der Kapitel.

Zwei Richtungen:

1. **Abdeckung** - jede lateinische Vokabel, die ein Kapitel im
   Wortschatz-Kasten einfuehrt, muss im Vokabelverzeichnis stehen.
   Fehlt sie, ist der Anhang unvollstaendig: der Leser findet das Wort
   nicht wieder.

2. **Datenqualitaet** - kaputte Eintraege im Verzeichnis: ein Wort
   mit einem Leerzeichen darin (``al uī``), doppelte Lemmata, Lemmata
   ohne Stufe.

Aufruf:

    python3 build/audit_vocab.py           # Bericht auf stdout
    python3 build/audit_vocab.py --json    # als JSON (fuer den Build-Check)

"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
GLOSSAR = os.path.join(ROOT, "glossar", "vokabeln.tsv")

# Woerter, die kein Lemma sind, sondern einen Verweis oder einen Begriff
# auf Deutsch bezeichnen.
GERMAN = re.compile(
    r"(?i)^(ende|endung|endungen|nacharbeit|arbeitsblatt|vokabular|"
    r"lernprozess|pragmatik|kasus\s*/\s*fall|wortfamilie|wortbildung|"
    r"bezeichnung|übersicht|beispiel|form|formen|plural|singular|"
    r"adjektiv|verbum|partizip|konjunktiv|indikativ|imperativ|infinitiv|"
    r"deklinatio|kaskus|konjugation|tempus|modus|adverb|präposition|"
    r"konjunktion|zahlwort|pronomen|adverbium|artikel|preposition)$")

# Ein Lemma: lateinische Buchstaben, optional mit Makronen, optional ein
# Beistrich (z. B. "puella, -ae").
LATIN = re.compile(r"^[A-Za-zāēīōūĀĒĪŌŪæœß]+(?:\s*,\s*-?[A-Za-zāēīōūĀĒĪŌŪæœß]*)?$")


def strip_mk(text: str) -> str:
    """Entfernt Makronen und normalisiert, damit Formen vergleichbar sind."""
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.lower().replace("j", "i").replace("v", "u")


def read_glossary() -> list[dict]:
    """Liest glossar/vokabeln.tsv (ohne Kopfzeile: latein, deutsch, stufe, stamm, familie)."""
    rows: list[dict] = []
    with open(GLOSSAR, encoding="utf-8") as fh:
        for num, line in enumerate(fh, start=1):
            parts = line.rstrip("\n").split("\t")
            if not parts or not parts[0].strip():
                continue
            if len(parts) != 5:
                rows.append({"_latein": parts[0], "_zeile": num, "_fehler": True})
                continue
            row = dict(zip(("latein", "deutsch", "stufe", "stamm", "familie"), parts))
            row["_latein"] = parts[0]
            row["_zeile"] = num
            rows.append(row)
    return rows


def lemma_forms(latein: str) -> list[str]:
    """Alle im Glossareintrag genannten Formen, normalisiert."""
    out = []
    for part in latein.split(","):
        form = part.strip()
        if form and form != "-":
            out.append(strip_mk(form))
    return out


def collect_wortschatz() -> list[tuple[str, str, str]]:
    """(Kapiteldatei, Lemma, Kontext) aus allen Wortschatz-Kaesten."""
    found: list[tuple[str, str, str]] = []
    for name in sorted(os.listdir(BOOK)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(BOOK, name), encoding="utf-8") as fh:
            text = fh.read()
        for m in re.finditer(r"^:::wortschatz[^\n]*\n(.*?)^:::\s*$", text, re.M | re.S):
            body = m.group(1)
            for item in body.split("·"):
                item = item.strip()
                if not item:
                    continue
                head = re.match(r"^\*\*(.+?)\*\*", item)
                if not head:
                    continue
                lemma = head.group(1).strip()
                # "puella, -ae" -> "puella"; "Rōma (Gen. Rōmae)" -> "Rōma"
                lemma = lemma.split(",")[0].strip()
                lemma = re.sub(r"\s*\([^)]*\)\s*$", "", lemma).strip()
                lemma = lemma.split("/")[0].strip()
                if not lemma or GERMAN.match(lemma) or not LATIN.match(lemma):
                    continue
                found.append((name, lemma, item))
    return found


def stem_of(lemma: str) -> str:
    """Leitet aus einem Lemma einen Stamm ab, an dem sich Formen erkennen lassen.

    Die Endungen sind so gewählt, dass die ueblichen Flexionsformen
    erkannt werden (am-am, am-avi, puell-a, Rōm-am ...). Ambigulaet ist
    hier erlaubt: es geht um Abdeckung, nicht um korrekte Lemmatisierung.
    """
    stem = strip_mk(lemma)
    for suffix in ("ibus", "issem", "erunt", "eris", "ere", "eunt",
                   "am", "as", "at", "is", "it", "em", "es", "et", "um",
                   "ae", "ei", "ei", "i", "o", "a", "e", "u"):
        if len(stem) - len(suffix) >= 3 and stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


# Woerter, die sich nur durch die Betonung (Makron) unterscheiden und
# daher absichtlich zweimal im Verzeichnis stehen.
HOMOGRAMME = {"liber"}


def is_eigenname(lemma: str) -> bool:
    """Ist das Lemma ein Eigenname (grossgeschrieben, kein Wort der_alltags)?"""
    if not lemma or not lemma[0].isupper():
        return False
    # Maenner- und Frauennamen sowie Ortsnamen enden auf typische Endungen.
    return True


def is_flexionsform(lemma: str, stems: dict[str, str]) -> bool:
    """Ist das Lemma eine gebeugte Form eines bekannten Wortes?

    Erkannt wird an der Endung: die Form muss auf einen im Verzeichnis
    bekannten Stamm zurueckfuehren lassen.  Partizipien und Gerundien
    zaehlen nicht als blosse Form - sie haben eigene Lemmata.
    """
    key = strip_mk(lemma)
    for endung in ("am", "as", "at", "em", "en", "es", "et", "is", "it",
                   "um", "us", "os", "i", "o", "a", "e", "ae", "ei",
                   "orum", "ium", "ibus", "ere", "eunt", "eris", "isse"):
        if not key.endswith(endung) or len(key) <= len(endung) + 2:
            continue
        stamm = key[: -len(endung)]
        if len(stamm) < 2:
            continue
        if stamm in stems:
            return True
        # Der Stamm kann noch ein Praefix tragen (z. B. "ab" in "abdicare").
        for s in stems:
            if len(s) >= 2 and (stamm == s or stamm.endswith(s)):
                return True
    return False


def is_partizip_oder_gerundium(lemma: str, stems: dict[str, str]) -> bool:
    """Ist das Lemma ein Partizip oder ein Gerundium?

    Beide sind Wortformen mit eigenem Lemma-Charakter, werden aber
    im Vokabelverzeichnis nicht als eigener Eintrag gefuehrt.
    """
    key = strip_mk(lemma)
    # Gerundium / Gerundivum: -ndum, -ndus, -nda, -ndi, -ndum
    for endung in ("ndum", "ndus", "nda", "ndi", "ndo"):
        if key.endswith(endung) and len(key) > len(endung) + 2:
            stamm = key[: -len(endung)]
            for s in stems:
                if len(s) >= 3 and (stamm == s or stamm.endswith(s)):
                    return True
    # Partizip Praesens aktiv: -ns (amans) mit Genitiv -ntis
    if key.endswith("ns") and len(key) > 3:
        stamm = key[:-2]
        for s in stems:
            if len(s) >= 2 and (stamm == s or stamm.endswith(s)):
                return True
    # Partizip Perfekt passiv: -us, -a, -um (amatus)
    if key.endswith(("us", "um")) and len(key) > 3:
        stamm = key[:-2]
        for s in stems:
            if len(s) >= 2 and (stamm == s or stamm.endswith(s)):
                return True
    return False


def audit() -> dict:
    rows = read_glossary()

    problems: list[str] = []
    missing: list[dict] = []
    broken: list[dict] = []
    duplicates: list[dict] = []
    eigennamen: list[dict] = []
    formen: list[dict] = []

    # --- Datenqualitaet des Verzeichnisses ---
    seen: dict[str, int] = {}
    for row in rows:
        num = row["_zeile"]
        latein = row["_latein"]
        if row.get("_fehler"):
            problems.append(f"vokabeln.tsv Zeile {num}: '{latein}' hat nicht 5 Spalten")
            continue
        for form in latein.split(","):
            form = form.strip()
            if not form:
                continue
            # "factus sum" und "iī (īvī)" sind zulaessige Schreibweisen.
            if " " in form and not form.endswith(" sum") and "(" not in form:
                broken.append({"zeile": num, "eintrag": latein,
                               "problem": f"Leerzeichen im Wort: {form!r}"})
        key = strip_mk(latein.split(",")[0].strip())
        # "liber" (Buch) und "līber" (frei) sind verschiedene Woerter:
        # nach dem Entfernen der Makronen fallen sie zusammen, werden aber
        # getrennt gefuehrt.
        if key in seen and key not in HOMOGRAMME:
            duplicates.append({"zeile": num, "eintrag": latein, "auch": seen[key]})
        else:
            seen[key] = num
        if not row.get("stufe", "").strip():
            problems.append(f"vokabeln.tsv Zeile {num}: '{latein}' ohne Stufe")

    # --- Abdeckung ---
    index: dict[str, str] = {}
    stems: dict[str, str] = {}
    for row in rows:
        if row.get("_fehler"):
            continue
        for form in lemma_forms(row["_latein"]):
            index.setdefault(form, row["_latein"])
        lemma = row["_latein"].split(",")[0].strip()
        index.setdefault(strip_mk(lemma), row["_latein"])
        # Der Stamm aus der Stamm-Spalte, sonst aus dem Lemma.
        stamm = (row.get("stamm") or "").strip().rstrip("-")
        if stamm:
            stems.setdefault(strip_mk(stamm), row["_latein"])
        else:
            stems.setdefault(stem_of(lemma), row["_latein"])

    seen_missing: dict[str, list[str]] = {}
    for fname, lemma, item in collect_wortschatz():
        key = strip_mk(lemma)
        if key in index:
            continue
        # Gebeugte Form: der Stamm eines bekannten Lemmas steckt im Wort.
        if any(key.startswith(s) and len(s) >= 3 for s in stems):
            continue
        seen_missing.setdefault(lemma, []).append(fname)

    for lemma, files in sorted(seen_missing.items()):
        eintrag = {"lemma": lemma, "gefunden_in": sorted(set(files))}
        if is_eigenname(lemma):
            eigennamen.append(eintrag)
        elif is_flexionsform(lemma, stems) or is_partizip_oder_gerundium(lemma, stems):
            formen.append(eintrag)
        else:
            missing.append(eintrag)

    return {
        "eintraege": len(rows),
        "gepruefte_wortschatz_eintraege": len(collect_wortschatz()),
        "fehlend": missing,
        "eigennamen": eigennamen,
        "flexionsformen": formen,
        "kaputt": broken,
        "doppelt": duplicates,
        "probleme": problems,
    }


def main() -> None:
    result = audit()
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"Glossar: {result['eintraege']} Eintraege")
    print(f"Wortschatz-Eintraege geprueft: {result['gepruefte_wortschatz_eintraege']}")

    print(f"\nOhne Verzeichniseintrag: {len(result['fehlend'])}")
    for m in result["fehlend"]:
        print(f"   {m['lemma']:24} {', '.join(m['gefunden_in'][:3])}")

    print(f"\nEigennamen (bewusst ohne Verzeichniseintrag): {len(result['eigennamen'])}")
    for m in result["eigennamen"]:
        print(f"   {m['lemma']:24} {', '.join(m['gefunden_in'][:3])}")

    print(f"\nFlexionsformen (bewusst ohne Verzeichniseintrag): "
          f"{len(result['flexionsformen'])}")
    for m in result["flexionsformen"]:
        print(f"   {m['lemma']:24} {', '.join(m['gefunden_in'][:3])}")

    print(f"\nKaputte Eintraege: {len(result['kaputt'])}")
    for b in result["kaputt"]:
        print(f"   Zeile {b['zeile']}: {b['eintrag']} -> {b['problem']}")

    print(f"\nDoppelte Lemmata: {len(result['doppelt'])}")
    for d in result["doppelt"]:
        print(f"   Zeile {d['zeile']}: {d['eintrag']} (zuvor Zeile {d['auch']})")

    print(f"\nWeitere Probleme: {len(result['probleme'])}")
    for p in result["probleme"]:
        print(f"   {p}")


if __name__ == "__main__":
    main()
