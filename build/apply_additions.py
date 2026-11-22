#!/usr/bin/env python3
"""Fuegt die kuratierte Ergaenzung in glossar/vokabeln.tsv ein.

Die Eintraege aus build/vocab_additions.tsv werden am Ende der jeweiligen
Stufe (A-E) eingefuegt, damit die alphabetische Ordnung innerhalb einer
Stufe erhalten bleibt.  Vorher wird eine Sicherung nach
glossar/vokabeln.tsv.bak gelegt.

Aufruf::

    python3 build/apply_additions.py            # nur berichten
    python3 build/apply_additions.py --write    # einspielen
"""

from __future__ import annotations

import argparse
import shutil
import sys
import unicodedata
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
GLOSSAR = WURZEL / "glossar" / "vokabeln.tsv"
ERGAENZUNG = WURZEL / "build" / "vocab_additions.tsv"


def lies_ergaenzung() -> list[list[str]]:
    zeilen: list[list[str]] = []
    for roh in ERGAENZUNG.read_text(encoding="utf-8").splitlines():
        if not roh.strip() or roh.lstrip().startswith("#"):
            continue
        felder = roh.split("\t")
        if len(felder) != 5:
            sys.exit(f"{ERGAENZUNG.name}: erwartet 5 Felder: {roh!r}")
        zeilen.append(felder)
    return zeilen


def main() -> int:
    ap = argparse.ArgumentParser(description="Ergaenzung einspielen")
    ap.add_argument("--write", action="store_true", help="Aenderungen schreiben")
    args = ap.parse_args()

    alt = GLOSSAR.read_text(encoding="utf-8").split("\n")
    if alt and alt[-1] == "":
        alt = alt[:-1]

    neue = lies_ergaenzung()
    print(f"Glossar: {len(alt)} Eintraege, Ergaenzung: {len(neue)} Eintraege")

    # Bereits vorhandene Eintraege ueberspringen: das Werkzeug muss
    # wiederholt laufen duerfen, ohne etwas doppelt einzuspielen.
    def kern(s: str) -> str:
        lemma = s.split("\t")[0].split(",")[0].strip()
        return "".join(c for c in unicodedata.normalize("NFD", lemma)
                       if not unicodedata.combining(c)).lower()

    vorhanden = {kern(z) for z in alt}
    neu = [z for z in neue if kern("\t".join(z)) not in vorhanden]
    uebersprungen = len(neue) - len(neu)
    if uebersprungen:
        print(f"  bereits vorhanden, uebersprungen: {uebersprungen}")
    neue = neu

    # Bestehende Zeilen nach Stufe gruppieren (Reihenfolge bleibt erhalten).
    stufen: dict[str, list[str]] = {}
    for zeile in alt:
        felder = zeile.split("\t")
        stufe = felder[2] if len(felder) >= 3 else ""
        stufen.setdefault(stufe, []).append(zeile)

    for zeile in neue:
        stufen.setdefault(zeile[2], []).append("\t".join(zeile))

    # Innerhalb einer Stufe alphabetisch nach dem Lemma sortieren.  Der
    # Schluessel ist das erste Lemma ohne Makronen und ohne Beistriche,
    # damit "puella, puellae" nicht mit "puella" kollidiert.
    def sortier(s: str) -> tuple:
        lemma = s.split("\t")[0]
        kern = lemma.split(",")[0].strip()
        kern = "".join(c for c in unicodedata.normalize("NFD", kern)
                       if not unicodedata.combining(c)).lower()
        return (kern, kern)

    ergebnis: list[str] = []
    for stufe in ("A", "B", "C", "D", "E"):
        gruppe = sorted(stufen.get(stufe, []), key=sortier)
        ergebnis.extend(gruppe)
        print(f"  Stufe {stufe}: {len(gruppe)} Eintraege")

    # Was in keiner Stufe landete, bleibt unangetastet erhalten.
    for stufe, gruppe in stufen.items():
        if stufe not in ("A", "B", "C", "D", "E"):
            ergebnis.extend(gruppe)

    print(f"Ergebnis: {len(ergebnis)} Eintraege")

    if args.write:
        shutil.copy2(GLOSSAR, GLOSSAR.with_suffix(".tsv.bak"))
        GLOSSAR.write_text("\n".join(ergebnis) + "\n", encoding="utf-8")
        print(f"Geschrieben: {GLOSSAR} (Sicherung: {GLOSSAR.with_suffix('.tsv.bak')})")
    else:
        print("Nur Bericht. Mit --write uebernehmen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
