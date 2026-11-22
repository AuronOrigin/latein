#!/usr/bin/env python3
"""Klassifiziert die Vorschlaege aus build/vocab_fill.py.

Die Wortschatz-Kaesten der Kapitel enthalten vier Arten von Eintrae-gen:

1. echte Grundvokabeln, die im Vokabelverzeichnis fehlen (Aufnahme),
2. Flexionsformen bereits verzeichneter Woerter (keine Aufnahme),
3. Eigennamen aus den Lektueren (Aufnahme in eine eigene Liste),
4. deutsche Fachbegriffe, die ins Begriffs-Glossar gehoeren.

Dieses Werkzeug sortiert die Vorschlaege in diese Gruppen und schreibt je
Gruppe eine pruefbare TSV-Datei.  Die Aufnahme in glossar/vokabeln.tsv
bleibt eine redaktionelle Entscheidung und erfolgt nicht automatisch.

    python3 build/classify_gaps.py --out /tmp/gruppen
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import audit_vocab as A  # noqa: E402
import vocab_fill as V  # noqa: E402

# Eigennamen, die in den Lektueren vorkommen.  Sie werden nicht in das
# Vokabelverzeichnis aufgenommen, sondern in die Lektueren-Liste.
EIGENNAMEN = {
    "Caesar", "Metella", "Acheron", "Cerberus", "Cocytus", "Mīnos",
    "Sisyphus", "Belgium", "Garumna", "Helvētiī", "Orgetorix", "Rhēnus",
    "Rhodanus", "Aboriginēs", "Achīvī", "Aeneās", "Lāvīnium", "Trōia",
    "Troiaānus", "Amphitritē", "Phōbē", "Titan", "Albion", "Brittania",
    "Oceanus", "lucilius", "Rōma",
}

# Deutsche Fachbegriffe aus den Anhaengen.  Sie gehoeren in
# glossar/begriffe.tsv, nicht in das Vokabelverzeichnis.
FACHBEGRIFFE = {
    "Herkunft", "Kapitelverweis", "Hauptformen", "Paradigma",
    "Tempuszeichen", "Klausur", "Punktesystem", "Reproduktion",
    "Fehleranalyse", "Kontrollieren", "Punktewertung",
}

# Flexionsformen, die als eigene Lemmata erscheinen, aber zu einem
# bereits verzeichneten Wort gehoeren.
FLEXIONSFORMEN = {
    "amat", "amābam", "amāveram", "amābō", "amārī", "amāvisse",
    "amārem", "amāverim", "amāvissem", "amēm", "Rōmam", "rosam",
    "auxiliō", "optimō", "eā", "hāc", "Rōmae", "irī", "orī", "ūtī",
    "fruī", "cuius", "quem", "quam", "sī", "terrīs", "memorem",
    "amandum", "amandus", "cōnandum", "studendum", "amāns", "amātus",
    "iudex", "nūsus", "pāscua", "ūna", "saga", "gesta", "salinae",
    "animī", "arma", "fugō", "fuit",
}

# Primae, die aus dem Wortschatz-Kasten stammen, aber keine Fehlstellen
# des Verzeichnisses sind (z. B. aus der Lektueren-Lektuere).
NEBENFORMEN = {
    "arbuteus", "Troiaānus", "Belgium", "Brittania", "Albion",
}


def sammle_kandidaten() -> dict[str, dict]:
    """Die Kandidatenliste aus vocab_fill, ungefiltert."""
    vorhanden: dict[str, str] = {}
    for row in A.read_glossary():
        if row.get("_fehler"):
            continue
        for form in A.lemma_forms(row["_latein"]):
            vorhanden.setdefault(A.strip_mk(form), row["_latein"])
    stamm_index: dict[str, str] = {}
    for row in A.read_glossary():
        if row.get("_fehler"):
            continue
        stamm = (row.get("stamm") or "").strip().rstrip("-")
        if stamm:
            stamm_index.setdefault(A.strip_mk(stamm), row["_latein"])

    kandidaten: dict[str, dict] = {}
    for eintrag in V.sammle_kaesten():
        key = A.strip_mk(eintrag["lemma"])
        if key in vorhanden:
            continue
        if any(key.startswith(s) and len(s) >= 3 for s in stamm_index):
            continue
        alt = kandidaten.get(key)
        if alt is not None:
            if len(eintrag["formen"]) > len(alt["formen"]):
                kandidaten[key] = eintrag
            continue
        kandidaten[key] = eintrag
    return kandidaten


def klassifiziere(kandidaten: dict[str, dict]) -> dict[str, list]:
    gruppen: dict[str, list] = {
        "vokabeln": [],     # echte Grundvokabeln
        "eigennamen": [],   # Eigennamen aus den Lektueren
        "fachbegriffe": [], # deutsche Fachbegriffe
        "formen": [],       # Flexionsformen, keine Aufnahme
    }
    for key, eintrag in kandidaten.items():
        lemma = eintrag["lemma"]
        if lemma in FACHBEGRIFFE:
            gruppen["fachbegriffe"].append(eintrag)
        elif lemma in EIGENNAMEN:
            gruppen["eigennamen"].append(eintrag)
        elif lemma in FLEXIONSFORMEN or lemma in NEBENFORMEN:
            gruppen["formen"].append(eintrag)
        else:
            gruppen["vokabeln"].append(eintrag)
    return gruppen


def main() -> int:
    ap = argparse.ArgumentParser(description="Luecken klassifizieren")
    ap.add_argument("--out", default="", help="Verzeichnis fuer die TSV-Dateien")
    args = ap.parse_args()

    kandidaten = sammle_kandidaten()
    gruppen = klassifiziere(kandidaten)

    print(f"Kandidaten gesamt: {len(kandidaten)}")
    for name, eintraege in gruppen.items():
        print(f"  {name:14} {len(eintraege):4}")

    if not args.out:
        return 0

    os.makedirs(args.out, exist_ok=True)
    for name, eintraege in gruppen.items():
        ziel = os.path.join(args.out, f"{name}.tsv")
        with open(ziel, "w", encoding="utf-8") as fh:
            for eintrag in sorted(eintraege, key=lambda e: (e["kapitel"], e["lemma"])):
                fh.write("\t".join([
                    eintrag["lemma"],
                    ", ".join(eintrag["formen"]),
                    eintrag["uebersetzung"],
                    eintrag["kapitel"],
                ]) + "\n")
        print(f"  geschrieben: {ziel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
