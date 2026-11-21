#!/usr/bin/env python3
"""Erzeugt glossar/vokabeln.csv und glossar/begriffe.csv aus den TSV-Quellen.

Die TSV-Dateien sind die von Hand gepflegten Quellen; die CSV-Dateien sind
die maschinenlesbaren Fassungen (Anki-Import, Nachschlagewerk, Druck).

    python3 tools/gen_glossar.py
"""
from __future__ import annotations

import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GLOSSAR = ROOT / "glossar"

VOKABEL_FELDER = ["latein", "deutsch", "stufe", "stamm", "familie"]
BEGRIFF_FELDER = ["begriff", "kategorie", "herkunft", "definition", "verwandte_begriffe", "kapitel"]


def lies_tsv(pfad: pathlib.Path) -> list[dict[str, str]]:
    zeilen: list[dict[str, str]] = []
    for num, roh in enumerate(pfad.read_text(encoding="utf-8").splitlines(), 1):
        if not roh.strip() or roh.startswith("#"):
            continue
        felder = roh.split("\t")
        if len(felder) != 5:
            sys.exit(f"{pfad.name}:{num} erwartet 5 Felder, gefunden {len(felder)}")
        zeilen.append(dict(zip(VOKABEL_FELDER, felder)))
    return zeilen


def main() -> int:
    GLOSSAR.mkdir(exist_ok=True)

    vokabeln = lies_tsv(GLOSSAR / "vokabeln.tsv")
    ziel_v = GLOSSAR / "vokabeln.csv"
    with ziel_v.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=VOKABEL_FELDER)
        w.writeheader()
        w.writerows(vokabeln)

    begriffe: list[dict[str, str]] = []
    for roh in (GLOSSAR / "begriffe.tsv").read_text(encoding="utf-8").splitlines():
        if not roh.strip() or roh.startswith("#"):
            continue
        felder = roh.split("\t")
        if len(felder) != 6:
            sys.exit(f"begriffe.tsv: erwartet 6 Felder, gefunden {len(felder)}: {roh[:60]}")
        begriffe.append(dict(zip(BEGRIFF_FELDER, felder)))

    ziel_b = GLOSSAR / "begriffe.csv"
    with ziel_b.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=BEGRIFF_FELDER)
        w.writeheader()
        w.writerows(begriffe)

    stufen: dict[str, int] = {}
    for v in vokabeln:
        stufen[v["stufe"]] = stufen.get(v["stufe"], 0) + 1
    print(f"vokabeln.csv : {len(vokabeln)} Einträge {stufen}")
    print(f"begriffe.csv : {len(begriffe)} Einträge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
