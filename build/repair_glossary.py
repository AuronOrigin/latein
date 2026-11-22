#!/usr/bin/env python3
"""Reparatur des Glossars.

Behebt systematische Datenfehler in ``glossar/vokabeln.tsv``:

* fehlende Bindestriche am Ende der Stamm-Spalte,
* bekannte Tippfehler wie ``al uī``.

Das Skript arbeitet zeilenweise auf der TSV-Quelle und schreibt nur dann
zurueck, wenn es mindestens eine Aenderung gefunden hat.  Vorher wird eine
Sicherheitskopie nach ``glossar/vokabeln.tsv.bak`` gelegt.

**Nicht** geaendert wird die Spalte ``familie``: sie ist ein Schluessel ohne
Makronen (890 von 893 Eintraegen) und wird abschliessend so gefuehrt.  Ebenso
bleibt die Stamm-Spalte der Verben in der Konvention des Buches, die die
thematischen Vokale weglässt (amare -> am-, regere -> reg-).

Aufruf::

    python3 build/repair_glossary.py           # nur berichten
    python3 build/repair_glossary.py --write   # Aenderungen uebernehmen
"""

from __future__ import annotations

import argparse
import shutil
import sys
import unicodedata
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
GLOSSAR = WURZEL / "glossar" / "vokabeln.tsv"

# Feste Ersetzungen fuer ganze Zeilen: latein -> (latein, deutsch)
ZEILEN_FIX = {
    "alō, alere, al uī, alitum": ("alō, alere, aluī, alitum", "nähren, ernähren"),
}


def ohne_makron(text: str) -> str:
    """Text ohne Makronen und andere Diakritika, kleingeschrieben."""
    zersetzt = unicodedata.normalize("NFD", text)
    return "".join(c for c in zersetzt
                   if not unicodedata.combining(c)).lower()


def repariere_zeile(zeile: list[str]) -> tuple[list[str], list[str]]:
    """Repariert eine Zeile und liefert (Zeile, Liste der Bemerke)."""
    bemerkungen: list[str] = []
    if len(zeile) < 5:
        return zeile, bemerkungen

    # 1. Bekannte Tippfehler in der lateinischen Spalte.
    roh = zeile[0].strip()
    if roh in ZEILEN_FIX:
        neu, glosse = ZEILEN_FIX[roh]
        zeile[0] = neu
        if glosse:
            zeile[1] = glosse
        bemerkungen.append(f"Tippfehler '{roh}' -> '{neu}'")

    # 2. Leerzeichen in einer Form: nur die Summe-Formen sind erlaubt.
    for index, form in enumerate(zeile[0].split(",")):
        form = form.strip()
        if not form or " " not in form:
            continue
        if form.endswith(" sum") or "(" in form:
            continue
        bemerkungen.append(f"Leerzeichen in der Form {form!r}")

    # 3. Stamm ohne Bindestrich am Ende.
    stamm = zeile[3].strip()
    if stamm and not stamm.endswith("-"):
        zeile[3] = stamm + "-"
        bemerkungen.append(f"Stamm '{stamm}' -> '{stamm}-' (Bindestrich)")

    # 4. Stufe muss A bis E sein.
    stufe = zeile[2].strip().upper()
    if stufe not in ("A", "B", "C", "D", "E"):
        bemerkungen.append(f"Ungueltige Stufe '{zeile[2]}'")

    return zeile, bemerkungen


def main() -> int:
    ap = argparse.ArgumentParser(description="Glossar reparieren")
    ap.add_argument("--write", action="store_true",
                    help="Aenderungen in glossar/vokabeln.tsv schreiben")
    args = ap.parse_args()

    if not GLOSSAR.exists():
        print(f"FEHLER: {GLOSSAR} nicht gefunden", file=sys.stderr)
        return 1

    roh = GLOSSAR.read_text(encoding="utf-8")
    zeilen = roh.split("\n")
    letzte_leer = zeilen[-1] == ""
    if letzte_leer:
        zeilen = zeilen[:-1]

    geaendert = 0
    neue_zeilen: list[str] = []
    bericht: list[str] = []
    for nummer, text in enumerate(zeilen, start=1):
        teile = text.split("\t")
        repariert, bemerkungen = repariere_zeile(teile)
        if bemerkungen:
            geaendert += 1
            bericht.append(f"  Z. {nummer:4}  {'; '.join(bemerkungen)}")
        neue_zeilen.append("\t".join(repariert))

    print(f"Gezielt geprueft: {len(zeilen)} Zeilen, beanstandet: {geaendert}")
    for zeile in bericht:
        print(zeile)

    if args.write and geaendert:
        shutil.copy2(GLOSSAR, GLOSSAR.with_suffix(".tsv.bak"))
        ausgabe = "\n".join(neue_zeilen) + ("\n" if letzte_leer else "")
        GLOSSAR.write_text(ausgabe, encoding="utf-8")
        print(f"\nGeschrieben: {GLOSSAR} (Sicherung: {GLOSSAR.with_suffix('.tsv.bak')})")
    elif args.write:
        print("\nKeine Aenderung noetig.")
    else:
        print("\nNur Bericht. Mit --write uebernehmen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
