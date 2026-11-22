#!/usr/bin/env python3
"""Erzeugt einen Vorschlag fuer die Ergaenzung des Vokabelverzeichnisses.

Die Wortschatz-Kaesten der Kapitel fuehren Vokabeln ein, die im
Vokabelverzeichnis (glossar/vokabeln.tsv) fehlen. Dieses Werkzeug liest
die Kaesten, erkennt die Luecken und schlaegt passende Verzeichniszeilen
vor - Stamm, Stufe und Wortfamilie werden aus dem Eintrag abgeleitet.

Der Vorschlag wird bewusst zur Pruefung geschrieben und nicht direkt
eingespielt:

    python3 build/vocab_fill.py --out /tmp/vorschlag.tsv

Die Datei hat dieselbe Form wie glossar/vokabeln.tsv
(latein, deutsch, stufe, stamm, familie).
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import audit_vocab as A  # noqa: E402

ROOT = A.ROOT

# Ausnahmen bei der Stammbildung: Verben, deren Besonderheit sich nicht
# aus den Endungen ergibt.
VERB_SONDER = {
    "sum": "esse", "fīō": "fi-", "eō": "e-", "nōlō": "nōl-", "mālō": "māl-",
    "volō": "vol-", "scīō": "scī-", "queīm": "queī-", "ferō": "fer-",
    "possum": "pos-", "memini": "memin-", "nēscīō": "nēscī-",
}

# Unregelmaessige Nomina: Stamm weicht vom Lemma ab.
NOMEN_SONDER = {
    "hominēs": "homin-", "pēs": "ped-", "mūs": "mūs-", "bos": "bov-",
    "urbs": "urb-", "nex": "nec-", "dīēs": "diē-", "lūx": "lūc-",
    "fīx": "fīc-", "nōx": "nōc-", "pēs": "ped-", "quīs": "quid-",
}

# Endungen, an denen sich eine gebeugte Form erkennen laesst.  Nur was mit
# einer dieser Endungen endet, gilt als Form eines anderen Lemmas.
FORM_ENDUNGEN = {
    "am", "ā", "ae", "as", "at", "em", "en", "es", "et", "i", "ī", "is", "it",
    "o", "ō", "um", "us", "ūs", "ōs", "as", "ārum", "ōrum", "ium", "ēī",
    "ant", "ent", "ātur", "itur", "āre", "ere", "īre", "eō", "ō", "ē",
    "ābam", "ēbam", "erā", "erō", "im", "īs", "iā", "iō", "āt", "et",
}


# Konjugationen: Infinitivendung -> Stamm.
KONJ = [
    ("āre", 3, ""),      # 1. Konjugation
    ("ēre", 3, ""),      # 2. Konjugation
    ("ere", 3, ""),      # 3. Konjugation und 3. Konj. -io
    ("īre", 4, "ā"),     # 4. Konjugation
    ("scīre", 4, ""),
]


def stamm_von_nomen(stamm: str) -> str:
    """Stamm eines Substantivs aus der Deklinationsregel."""
    return stamm + "-"


# Endungen, an denen sich ein Infinitiv erkennen laesst.
INFINITIV = ("āre", "ēre", "ere", "īre", "rī", "se", "isse")


def ist_verb(formen: list[str]) -> bool:
    """Ist die Formenliste die eines Verbs? (Infinitiv an zweiter Stelle)"""
    if len(formen) < 2:
        return False
    return formen[1].endswith(INFINITIV)


def adjektiv_stamm(lemma: str) -> str:
    """Stamm eines Adjektivs ohne Flexionsendung: pulcher -> pulch-."""
    for endung, laenge in (("us", 2), ("er", 2), ("is", 2), ("e", 1), ("a", 1)):
        if lemma.endswith(endung) and len(lemma) > laenge + 1:
            return lemma[:-laenge] + "-"
    return lemma + "-"


def nomen_stamm(lemma: str, genitiv: str) -> str | None:
    """Stamm eines Substantivs oder Adjektivs aus Nominativ und Genitiv."""
    if not genitiv:
        return None
    # Partizipien: amans/amantis, amatus/amatum
    if lemma.endswith("ns") and genitiv.endswith("ntis"):
        return lemma[:-2]
    if lemma.endswith("us") and genitiv.endswith(("um", "ī")):
        return lemma[:-2]
    for endung, laenge in (("ōrum", 4), ("ae", 2), ("ēī", 2), ("ī", 1),
                           ("is", 2), ("ūs", 2), ("um", 2)):
        if genitiv.endswith(endung):
            return genitiv[:-laenge]
    return None


def stamm_von_verb(formen: list[str]) -> str:
    """Stamm eines Verbs aus Praesens und Infinitiv."""
    praesens = formen[0] if formen else ""
    infinitiv = formen[1] if len(formen) > 1 else ""
    for name, wert in VERB_SONDER.items():
        if A.strip_mk(praesens).startswith(A.strip_mk(name)):
            return wert
    for endung, laenge, ersatz in KONJ:
        if infinitiv.endswith(endung) and len(infinitiv) > laenge + 1:
            if endung == "īre" and not praesens.endswith(("iō", "iunt")):
                continue
            return infinitiv[:-laenge] + ersatz + "-"
    return praesens + "-"


def stamm3(lemma: str) -> str:
    """Stamm eines Substantivs der 3. Deklination.

    Der Nominativ gibt die Endung vor; der Stamm liegt bei den
    meisten Bildungen einfach davor.
    """
    if lemma.endswith("as"):            # sānitas, veritās, pietās
        return lemma[:-2]
    if lemma.endswith("es"):            # fauces, fruges, Aboriginēs
        return lemma[:-2]
    if lemma.endswith(("ēns", "āns", "ens")):   # occidēns, amāns
        return lemma[:-2]
    if lemma.endswith(("on", "ix", "or", "ar")):  # Acheron, Orgetorix, mercātor
        return lemma[:-2]
    if lemma.endswith("is"):            # panis
        return lemma[:-2]
    return lemma[:-1]                   # exercitātiō, latro, coniūnctio


def erweitere(lemma: str, formen: list[str]) -> tuple[str, str]:
    """(volle Form, Stamm) aus der Endungsangabe der Wortschatz-Kaesten."""
    suffix = formen[0][1:]              # ohne fuehrenden Strich

    # 1. Deklination: puella -> puellae
    if suffix == "ae":
        return lemma[:-1] + "ae", lemma[:-1]
    # 2. Deklination: discipulus -> discipuli, bellum -> belli
    if suffix == "ī":
        return lemma[:-2] + "ī", lemma[:-2]
    # 2. Deklination mit Linkkonsonant: magister -> magistri
    if suffix in ("trī", "brī", "erī"):
        return lemma[:-2] + suffix, lemma[:-2]
    # 4. Deklination: conflictus -> conflictus, cornū -> cornuus
    if suffix == "ūs":
        if lemma.endswith("ū"):
            # cornū: der Stamm traegt das lange u (cornūs)
            return lemma + "s", lemma
        return lemma[:-2] + "ūs", lemma[:-2]
    # 5. Deklination: ira -> irae
    if suffix == "rae":
        return lemma[:-1] + "rae", lemma[:-1]
    # Genitiv Plural: Celtae -> Celtorum, arma -> armorum
    if suffix == "ōrum":
        return lemma[:-1] + "ōrum", lemma[:-1]
    # 3. Deklination, Genitiv Singular
    if suffix == "is":
        # Caesar -> Caesaris, panis -> panis
        if lemma.endswith("is"):
            return lemma[:-2] + "is", lemma[:-2]
        return lemma + "is", lemma
    if suffix == "entis":
        # occidens -> occidentis
        stamm = stamm3(lemma)
        return stamm + "ntis", stamm
    if suffix in ("ōnis", "ātis", "ōris", "inis", "ontis", "ēs", "igis", "ium"):
        stamm = stamm3(lemma)
        return stamm + suffix, stamm
    # Unbekanntes Muster: die Endung angehaengt lassen.
    return lemma + suffix, lemma


def sammle_kaesten() -> list[dict]:
    """Alle Einträge der Wortschatz-Kaesten."""
    eintraege: list[dict] = []
    for name in sorted(os.listdir(A.BOOK)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(A.BOOK, name), encoding="utf-8") as fh:
            text = fh.read()
        for m in re.finditer(r"^:::wortschatz[^\n]*\n(.*?)^:::\s*$", text, re.M | re.S):
            for item in m.group(1).split("·"):
                item = item.strip()
                if not item:
                    continue
                head = re.match(r"^\*\*(.+?)\*\*", item)
                if not head:
                    continue
                roh = head.group(1).strip()
                rest = item[head.end():].strip()
                # Uebersetzung: Text nach dem Gedankenstrich
                translation = ""
                m2 = re.search(r"—\s*(.+)$", rest)
                if m2:
                    translation = m2.group(1).strip().rstrip("·").strip()
                if not translation:
                    continue
                teile = [t.strip() for t in roh.split(",")]
                lemma = teile[0].strip()
                lemma = re.sub(r"\s*\([^)]*\)\s*$", "", lemma).strip()
                if not lemma or A.GERMAN.match(lemma):
                    continue
                if not A.LATIN.match(lemma):
                    continue
                eintraege.append({
                    "kapitel": name,
                    "lemma": lemma,
                    "formen": teile[1:],
                    "roh": roh,
                    "uebersetzung": translation,
                })
    return eintraege


def stufe_pro_kapitel() -> dict[str, Counter]:
    """Welche Stufe haben die bereits verzeichneten Woerter je Kapitel?"""
    glossar = {}
    for row in A.read_glossary():
        if row.get("_fehler"):
            continue
        for form in A.lemma_forms(row["_latein"]):
            glossar.setdefault(form, row.get("stufe", "").strip())
    pro: dict[str, Counter] = defaultdict(Counter)
    for eintrag in sammle_kaesten():
        stufe = glossar.get(A.strip_mk(eintrag["lemma"]))
        if stufe:
            pro[eintrag["kapitel"]][stufe] += 1
    return pro


def main() -> None:
    zeile = None
    if "--out" in sys.argv:
        zeile = sys.argv[sys.argv.index("--out") + 1]

    vorhanden: dict[str, str] = {}
    for row in A.read_glossary():
        if row.get("_fehler"):
            continue
        for form in A.lemma_forms(row["_latein"]):
            vorhanden.setdefault(form, row["_latein"])
    stamm_index = {}
    for row in A.read_glossary():
        if row.get("_fehler"):
            continue
        stamm = (row.get("stamm") or "").strip().rstrip("-")
        if stamm:
            stamm_index.setdefault(A.strip_mk(stamm), row["_latein"])

    pro_kapitel = stufe_pro_kapitel()
    vorschlaege: dict[str, dict] = {}

    for eintrag in sammle_kaesten():
        key = A.strip_mk(eintrag["lemma"])
        if key in vorhanden:
            continue
        # Gebeugte Form eines bereits verzeichneten Wortes?
        if any(key.startswith(s) and len(s) >= 3 for s in stamm_index):
            continue
        # Ein Wort kommt in mehreren Kapiteln vor; die ausfuehrlichste
        # Angabe gewinnt ("rosa, -ae" vor "rosa").
        alt = vorschlaege.get(key)
        if alt is not None:
            if len(eintrag["formen"]) > len(alt["formen"]):
                vorschlaege[key] = eintrag
            continue
        vorschlaege[key] = eintrag

    zeilen = []
    for key, eintrag in sorted(vorschlaege.items(),
                               key=lambda kv: (kv[1]["kapitel"], kv[0])):
        lemma = eintrag["lemma"]
        formen = eintrag["formen"]

        if formen and not formen[0].startswith("-"):
            # "portō, portāre", "amō, amāre, amāvī, amātum" oder "manus, manūs"
            latein = ", ".join([lemma] + formen)
            if ist_verb([lemma] + formen):
                stamm = stamm_von_verb([lemma] + formen)
            else:
                stamm = NOMEN_SONDER.get(lemma)
                if stamm is None:
                    stamm = nomen_stamm(lemma, formen[0])
                if stamm is None:
                    stamm = adjektiv_stamm(lemma)
                else:
                    stamm = stamm + "-"
        elif formen:
            if len(formen) == 2 and formen[0].startswith("-") and formen[1].startswith("-"):
                # Adjektiv: "futūrus, -a, -um"
                latein = ", ".join([lemma, lemma + formen[0][1:], lemma + formen[1][1:]])
                stamm = NOMEN_SONDER.get(lemma, adjektiv_stamm(lemma))
            else:
                voll, stamm_raw = erweitere(lemma, formen)
                latein = f"{lemma}, {voll}"
                stamm = NOMEN_SONDER.get(lemma, stamm_von_nomen(stamm_raw))
        else:
            latein = lemma
            stamm = NOMEN_SONDER.get(lemma, lemma + "-")

        # Stufe: Modalwert der bereits verzeichneten Woerter desselben Kapitels
        stufen = pro_kapitel.get(eintrag["kapitel"])
        stufe = stufen.most_common(1)[0][0] if stufen else "C"

        zeilen.append((latein, eintrag["uebersetzung"], stufe, stamm, lemma))

    # Gebeugte Formen streichen, die zu einem bereits vorgeschlagenen Lemma
    # gehoeren ("rosam" ist die Akkusativform von "rosa").  Der eigene Stamm
    # eines Eintrags zaehlt dabei nicht.
    stammliste = [(A.strip_mk(z[3].rstrip("-")), A.strip_mk(z[4])) for z in zeilen]
    gefiltert = []
    for eintrag_zeile in zeilen:
        key = A.strip_mk(eintrag_zeile[4])
        eigen = A.strip_mk(eintrag_zeile[3].rstrip("-"))
        treffer = False
        for s, lemma_key in stammliste:
            if s == eigen or len(s) < 3:
                continue
            if key == lemma_key or not key.startswith(s):
                continue
            rest = key[len(s):]
            if rest in FORM_ENDUNGEN:
                treffer = True
                break
        if not treffer:
            gefiltert.append(eintrag_zeile)
    zeilen = gefiltert

    print(f"Vorschlaege: {len(zeilen)}")
    for latein, deutsch, stufe, stamm, lemma in zeilen:
        print(f"   {latein:38} | {deutsch[:34]:34} | {stufe} | {stamm:14} | {lemma}")

    if zeile:
        with open(zeile, "w", encoding="utf-8") as fh:
            for row in zeilen:
                fh.write("\t".join(row) + "\n")
        print(f"\ngeschrieben: {zeile}")


if __name__ == "__main__":
    main()
