# -*- coding: utf-8 -*-
"""Erzeugt Anhang V (Kapitel 54) — die Lösungen zu allen Übungen.

Datenquellen:

* ``build/loesungen/moved.json``  — die aus den Kapiteln in den Anhang
  migrierten Lösungen (122 Einträge: Übungsblöcke, Wiederholungsfächer,
  Mikroübungen und die separaten Prüfungscheck-Lösungen der Kapitel 02–10).
* ``build/loesungen/check_answers*.py`` — die fachlichen Musterantworten auf
  die offenen Prüfungscheck-Fragen der Kapitel 01 und 11–53.
* ``build/loesungen/teil_e_block.md`` — der Lösungsband zur Gesamtprüfung.

Aufruf::

    python3 build/loesungen/build_anhang.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from check_answers import CHECK_ANSWERS  # noqa: E402

BOOK = ROOT / "book"

moves_raw = json.loads((HERE / "moved.json").read_text(encoding="utf-8"))
stripped_raw = json.loads((HERE / "stripped.json").read_text(encoding="utf-8"))
MOVES: dict[int, list[tuple[str, str]]] = {
    int(k): [(kind, body) for kind, body in v] for k, v in moves_raw.items()
}
TEIL_E = (HERE / "teil_e_block.md").read_text(encoding="utf-8").strip()

# --- Kapitelmetadaten --------------------------------------------------------

TITEL: dict[int, str] = {}
MIKRO_TITEL: dict[int, list[str]] = {}
CHECK_ITEMS: dict[int, list[tuple[int, str, str | None]]] = {}

for path in sorted(BOOK.glob("*.md")):
    m = re.search(r"(\d+)-", path.name)
    if not m:
        continue
    no = int(m.group(1))
    text = path.read_text(encoding="utf-8")
    tm = re.search(r"^title:\s*(.+)$", text, re.M)
    TITEL[no] = re.sub(r"^\d+\.\s*", "", tm.group(1).strip().strip('"')) if tm else "?"
    MIKRO_TITEL[no] = [
        x.group(1).strip() for x in re.finditer(r"^:::mikro\s*(.+)$", text, re.M)
    ]
    for cm in re.finditer(r"^:::check[^\n]*\n(.*?)^:::\s*$", text, re.M | re.S):
        items = []
        for line in cm.group(1).split("\n"):
            nm = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
            if nm:
                items.append((int(nm.group(1)), nm.group(2).strip(), None))
        if items:
            CHECK_ITEMS[no] = items

# --- Prüfungscheck-Lösungen --------------------------------------------------

CHECK_LOESUNG: dict[int, str] = {}

# Die beim Bereinigen der Kapitel entfernten Antworten.  Sie tragen die
# Lösungen der Aufgaben 1 und 2 der Prüfungschecks (Form einsetzen,
# übersetzen); Aufgabe 3 steht in ``check_answers``.
STRIPPED: dict[int, dict[str, list[str]]] = {}
for _name, _kinds in stripped_raw.items():
    _m = re.search(r"(\d+)-", _name)
    if not _m:
        continue
    STRIPPED[int(_m.group(1))] = _kinds

# 1) Die neun Kapitel 02–10 haben bereits separate, nummerierte Check-Lösungen
#    in ``moved.json``.  Sie werden unverändert übernommen.
for no in range(2, 11):
    for kind, body in MOVES.get(no, []):
        if kind == "check":
            CHECK_LOESUNG[no] = body.strip()

# 2) Für die übrigen Kapitel wird die Check-Lösung aus den Antworten
#    zusammengesetzt: Nummer 1 und 2 stammen aus den Musterantworten bzw.
#    sind bereits im Anhang abgedeckt, Nummer 3 ist die Erklärfrage.
EXTRA_ANSWER: dict[int, dict[int, str]] = {}


def _normalize(text: str) -> str:
    text = re.sub(r"[*_`]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def build_check_loesungen() -> None:
    """Erzeugt die Check-Lösung je Kapitel aus den gespeicherten Antworten."""
    for no, items in CHECK_ITEMS.items():
        if no in CHECK_LOESUNG:
            continue
        answers = CHECK_ANSWERS.get(str(no), {})
        removed = STRIPPED.get(no, {}).get("check", [])
        parts: list[str] = []
        for idx, (nr, frage, _) in enumerate(items):
            answer = answers.get(str(nr))
            if answer is None:
                # Aufgabe 1 und 2: Form bzw. Übersetzung.  Die Antwort wurde
                # beim Bereinigen des Kapitels entfernt und liegt hier vor.
                if idx < len(removed):
                    answer = removed[idx]
                else:
                    answer = f"*(siehe Musterlösung)* — {frage}"
            parts.append(f"{nr}. {answer}")
        # Wenn eine Aufgabe eine eigene Musterantwort hat (etwa K38 Nr. 2),
        # steht sie an ihrer Stelle — nicht an der einer anderen Nummer.
        if not parts:
            continue
        CHECK_LOESUNG[no] = "\n".join(parts)


build_check_loesungen()

# --- Anhang-Aufbau -----------------------------------------------------------

RANGES = [
    (1, 1, "Vorwort und Einleitung"),
    (2, 20, "Teil I — Die Sprache im Kopf  ·  Teil II — Formenlehre"),
    (21, 39, "Teil III — Syntax  ·  Teil IV — Die Kunst der Übersetzung"),
    (40, 49, "Teil V — Lektüre"),
    (50, 54, "Teil VI — Anhänge"),
]

RANG = {"mikro": 0, "speziell": 1, "uebung": 2, "wiederholung": 3, "check": 4}
LABEL = {
    "mikro": "Mikroübung",
    "speziell": "Wort-für-Wort-Übersetzung",
    "uebung": "Übungsblock",
    "wiederholung": "Wiederholungsfach",
    "check": "Prüfungscheck",
}

KOPF = """---
title: 54. Anhang V — Lösungen zu allen Übungen
part: Teil VI – Anhänge
subtitle: Die Lösungen zu jedem Übungsblock, Wiederholungsfach, Prüfungscheck und jeder Mikroübung des Buches
---

:::ziel Lernziele
Nach diesem Anhang kannst du:
- deine Ergebnisse **selbst kontrollieren**, ohne dass die Lösung neben der Aufgabe steht,
- **Fehler einordnen** — die Lösung nennt in der Regel die Regel, nicht nur das Ergebnis,
- erkennen, welche **Kapitel** du nacharbeiten musst.
:::

:::wortschatz
**Lösung** — die richtige Antwort auf eine Aufgabe ·
**Fehleranalyse** — die systematische Suche nach der Ursache eines Fehlers ·
**Nacharbeit** — die Arbeit, die auf einen erkannten Fehler folgt ·
**Kontrollieren** — die eigene Antwort mit der Musterlösung vergleichen ·
**Musterlösung** — die Lösung, an der du deine eigene misst ·
**Punktewertung** — die Umrechnung richtiger Antworten in einen Punktwert
:::

## So arbeitest du mit diesem Anhang

Dieser Anhang enthält **alle** Lösungen des Buches: zu jedem Übungsblock, zu jedem Wiederholungsfach, zu jedem Prüfungscheck und zu jeder Mikroübung — dazu den vollständigen Lösungsband zur Gesamtprüfung aus Kapitel 53.

```
  1. Aufgabe bearbeiten  — ohne zu blättern
  2. Selbst korrigieren  — erst selbst prüfen, dann blättern
  3. Fehler einordnen   — die Lösung nennt die Regel
  4. Kapitel nacharbeiten — bei zwei Fehlern in einem Thema: zurück zum Text
```

:::merksatz Die Regel, die mehr bringt als Punkte
Ein **richtiges** Ergebnis bringt dir einen Punkt. Eine **begründete** Lösung bringt dir den nächsten Test. Wenn du beim Prüfen merkst, dass du die Antwort *weißt* — aber nicht *begründen* kannst, zählt die Aufgabe trotzdem als Fehler.
:::

:::info Der Weg durch dieses Buch
Die Kapitel 01–53 enthalten **Aufgaben ohne Lösungen** — so kannst du sie bearbeiten, ohne in die falsche Ecke zu schauen. Hinter jedem Aufgabenblock steht ein kurzer Verweis hierher. Diese Lösungen sind nach Kapiteln geordnet: Springe mit dem Inhaltsverzeichnis direkt zu dem Kapitel, bei dem du unsicher warst.
:::

"""

out: list[str] = [KOPF]

for lo, hi, name in RANGES:
    vorhanden = [n for n in sorted(TITEL) if lo <= n <= hi]
    if not vorhanden:
        continue
    out.append("**" + name + "**")
    out.append("")
    for n in vorhanden:
        out.append("## %02d — %s" % (n, TITEL[n]))
        out.append("")

        if n == 53:
            out.append("### Lösungen zur Gesamtprüfung (Teil A–E)")
            out.append("")
            te = TEIL_E.split("\n", 1)[1].lstrip()
            te = te.replace("## Teil E — Lösungen\n\n", "")
            teile = re.split(r"^### Teil ([A-E])\s*$", te, flags=re.M)
            for idx in range(1, len(teile), 2):
                tl = teile[idx]
                body = teile[idx + 1].strip()
                out.append(":::loesung Gesamtprüfung Teil %s (Kapitel 53)" % tl)
                out.append("")
                out.append(body)
                out.append(":::")
                out.append("")

        eintraege: list[tuple[str, str]] = []
        for kind, body in MOVES.get(n, []):
            if kind == "check":
                continue  # kommt als eigener Block weiter unten
            eintraege.append((kind, body))
        if n in CHECK_LOESUNG:
            eintraege.append(("check", CHECK_LOESUNG[n]))

        eintraege.sort(key=lambda x: RANG[x[0]])
        mi = 0
        for kind, body in eintraege:
            if kind == "mikro":
                tt = (
                    MIKRO_TITEL[n][mi]
                    if mi < len(MIKRO_TITEL.get(n, []))
                    else "Mikroübung"
                )
                mi += 1
                out.append("### %s — %s" % (LABEL[kind], tt))
            else:
                out.append("### " + LABEL[kind])
            out.append("")
            out.append(":::loesung %s (Kapitel %02d)" % (LABEL[kind], n))
            out.append("")
            out.append(body.strip())
            out.append(":::")
            out.append("")

# --- Eigene Bausteine des Anhangs -------------------------------------------

out.append("## Der Lösungsanhang selbst")
out.append("")
out.append(":::uebung")
out.append("**A. Verstehen.**")
out.append("1. In welcher Reihenfolge arbeitest du mit einer Aufgabe und ihrer Lösung? ______")
out.append("2. Was ist der Unterschied zwischen einer *richtigen* und einer *begründeten* Lösung? ______")
out.append("3. Warum stehen die Lösungen zu den Mikroübungen **nicht** direkt an der Aufgabe? ______")
out.append("4. Wann ist eine Antwort „richtig\", aber trotzdem ein Fehler? ______")
out.append("")
out.append("**B. Anwenden.**")
out.append("5. Du hast im Kapitel „Genitiv\" zwei von fünf Aufgaben falsch. Schreibe auf, welche Regel dir gefehlt hat, und in welchem Kapitel du sie nachliest. ______")
out.append("6. Du hast die Gesamtprüfung mit 62 Punkten bestanden. Welche drei Themen aus Teil A–D schaust du zuerst an — und warum? ______")
out.append(":::")
out.append("")
out.append(":::loesung Übungsblock (Anhang V selbst)")
out.append("**A.**")
out.append("1. Bearbeiten → selbst korrigieren → Fehler einordnen → Kapitel nacharbeiten. 2. Die *richtige* Lösung nennt das Ergebnis; die *begründete* nennt die Regel dahinter — erst sie macht den Test wiederholbar. 3. Weil die Lösungen im Buch gesammelt stehen: Wer sie direkt neben der Aufgabe findet, liest sie meistens sofort — und lernt nichts. 4. Wenn du die Antwort *weißt*, aber sie nicht begründen kannst: Dann sitzt die Form, aber nicht die Funktion.")
out.append("")
out.append("**B.**")
out.append("5. Muster: *„Ich habe den Genitivus originis nicht erkannt — er steht bei Eigennamen ohne Possessivum (Caesaris = von Caesar). Kapitel 23, Unterabschnitt ‚Genitiv als Herkunft'.\"* 6. Muster: *„Erst Teil C (Übersetzung), weil dort 30 der 100 Punkte liegen und ich die Fehlerquote nicht kenne; dann Teil B, weil die Syntax die Übersetzung behindert; zuletzt Teil A, weil Formfehler nur 20 Punkte tragen.\"*")
out.append(":::")
out.append("")
out.append(":::wiederholung Wiederholungsfach")
out.append("**Aus dem Gedächtnis:**")
out.append("1. Wie viele Kapitel hat das Buch? ______")
out.append("2. In welchem Anhang stehen alle Lösungen? ______")
out.append("3. Wie viele Punkte hat die Gesamtprüfung? ______")
out.append("4. Was ist die Regel „Form → Funktion → Bedeutung\"? ______")
out.append(":::")
out.append("")
out.append(":::loesung Wiederholungsfach (Anhang V selbst)")
out.append("1. 55 (Kapitel 00 bis 54). 2. Anhang V (Kapitel 54). 3. 100 Punkte. 4. Erst die Form (Endung, Stamm), dann die Funktion im Satz, dann die Bedeutung — wer bei der Form stehen bleibt, lernt nur Deklination.")
out.append(":::")
out.append("")
out.append(":::loesung Prüfungscheck (Anhang V selbst)")
out.append("Diese vier Fragen sind **Selbstbeurteilung** — sie haben keine richtige Antwort, sondern eine ehrliche. Die Musterantwort zeigt, worauf es ankommt:")
out.append("")
out.append("1. **Muster:** Ja — aber prüfe es an einem konkreten Kapitel: Wenn du in Kapitel 23 die Genitiv-Aufgaben nicht ohne Blick ins Buch lösen konntest, ist die Antwort \"nein\". Diese Selbstehrlichkeit ist der Punkt.")
out.append("2. **Muster:** Ja, wenn zu mindestens einem Fehler ein eigener Satz dasteht, in dem die Regel **angewendet** wird. Ein Fehler, den man einmal selbst überwunden hat, wiederholt sich nicht.")
out.append("3. **Muster:** Ja — und die Uhr stand dabei. Ohne Zeitdruck prüfst du dein Tempo nicht, sondern nur dein Wissen. Der erste Durchgang zählt nicht als Prüfung.")
out.append("4. **Muster:** Ja — mit **Kapitelzahlen**, nicht mit Stichworten. Eine Liste \"Deklination, Kasus, Tempus\" bringt nichts; die Liste \"Kapitel 23, 26, 31\" bringt alles.")
out.append(":::")
out.append("")
out.append(":::check Prüfungscheck")
out.append("1. Hast du **jedes** Kapitel mit Übungsblock bearbeitet, **bevor** du hier geblättert hast?")
out.append("2. Hast du für jeden Fehler ein **eigenes Satzbeispiel** gebildet, das die Regel anwendet?")
out.append("3. Hast du die **Gesamtprüfung** unter Zeitbedingung geschrieben und dann erst korrigiert?")
out.append("4. Hast du eine **Nacharbeitliste** — mit Kapitelzahlen — angelegt?")
out.append(":::")
out.append("")
out.append(":::vertiefung")
out.append("- **Der Plan für die zweite Runde:** Nach vier Wochen dieselbe Gesamtprüfung noch einmal, ohne Hilfen. Der Unterschied zwischen den beiden Punktzahlen zeigt deinen Fortschritt besser als jede einzelne Note.")
out.append("- **Noch nicht sitzend?** Arbeite die Kapitel 04–12 (Baukasten, Deklination, Verb) und 22–30 (Syntax) in dieser Reihenfolge durch. Das ist der schnellste Weg von 45 auf 75 Punkte.")
out.append("- **Für Fortgeschrittene:** Übersetze die Lektüretexte aus Kapitel 40–49 **ohne** Vokabelhilfe und vergleiche deine Fassung mit der Wort-für-Wort-Übersetzung im Buch. Das ist die eigentliche Lesekompetenz.")
out.append(":::")

text = "\n".join(out)
text = re.sub(r"\n{4,}", "\n\n\n", text)
target = BOOK / "54-anhang-loesungen.md"
target.write_text(text, encoding="utf-8")
print(
    "Anhang V: %d Zeichen, %d Lösungskästen, %d Kapitelabschnitte"
    % (
        len(text),
        len(re.findall(r"^:::loesung\b", text, re.M)),
        len(re.findall(r"^## \d\d — ", text, re.M)),
    )
)
print("Check-Loesungen erzeugt:", len(CHECK_LOESUNG))
