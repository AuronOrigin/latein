# -*- coding: utf-8 -*-
"""Entfernt die expliziten Inline-Antworten aus den Kapiteldateien.

Der Anhang V (Kapitel 54) enthält alle Lösungen.  In den Kapiteln 01–53
stehen die Aufgaben deshalb **ohne** Lösungen.  Dieses Skript entfernt die
noch verbliebenen Antwortmarker:

* ``→`` gefolgt von einer Antwort  —  aus ``:::uebung``, ``:::wiederholung``
  und ``:::check``
* ``—`` gefolgt von einer Übersetzung in Anführungszeichen (nur in
  ``:::check``-Blöcken, Nummer 2 „Übersetze: …“)

Zeilen, in denen der Pfeil nur **Aufgabenmaterial** voneinander trennt
(z. B. *5. *Utinam moriar!* → 6. *Exāmus!* → 7. …* in Kapitel 20 oder
*Lückenanweisungen* wie *→ ______*), bleiben unangetastet — sie tragen
keine Antwort.

Aufruf::

    python3 build/loesungen/strip_answers.py [--check]
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "book"

# --- Muster, die KEINE Antwort enthalten, sondern Aufgabenmaterial ----------

# Lücke zum Ausfüllen:  „… → ______“
RE_LUECKE = re.compile(r"→\s*(?:_{2,}|\.{3,})\s*$")

# Verkettete Aufgaben: „5. X → 6. Y → 7. Z“  — der Pfeil trennt Nummern.
RE_NUMMERN_FOLGE = re.compile(r"→\s*\d+\.")

# Auswahlaufgabe: „9. *Dīcō:* → *venīre / vēnisse / venītūrum esse?*“
RE_AUSWAHL = re.compile(r"→\s*\*[^?]*\?\*\s*$")

# „8. *possuī?* (→ *potuī*)“ — Korrekturhinweis in Klammern, KEINE Antwort
# (die Aufgabe fragt nach Tempus/Person/Numerus von *possuī*).
RE_KLAMMER_KORREKTUR = re.compile(r"\s*\(\s*→[^)]*?\s*\)")

# „5. *Utinam moriar!* → 6. *Exāmus!*“ — der Pfeil trennt Nummern, trägt
# aber keine Antwort.  (Wird von RE_NUMMERN_FOLGE abgedeckt.)

# „1. *pulcher* → Komparativ, Superlativ“ (Kapitel 14) — der Pfeil nennt die
# **gefragte** Form, nicht die Antwort.  Die Antwort steht im Anhang.
RE_AUFTRAG_FORM = re.compile(r"^→\s*(Komparativ|Superlativ)\b.*$")

# „9. *Magister discipulōs monet.* → „Die Schüler ermahnen den Lehrer.““
# (Kapitel 38) — der Pfeil enthält eine **bewusst falsche** Übersetzung,
# die die Aufgabe erst auslöst.  Sie bleibt stehen.
RE_FEHLER_QUELLE = re.compile(r"^→\s*[„\"]")


def _ist_antwortzeile(text: str) -> bool:
    """Trägt die Zeile eine explizite Antwort nach ``→``?"""
    if "→" not in text:
        return False
    if RE_LUECKE.search(text):
        return False
    if RE_NUMMERN_FOLGE.search(text):
        return False
    if RE_AUSWAHL.search(text):
        return False
    if RE_AUFTRAG_FORM.match(text.split("→", 1)[1].strip()):
        return False
    return True


def strip_check_block(body: str) -> tuple[str, list[str]]:
    """Entfernt Antworten aus einem ``:::check``-Block.

    In den Prüfungschecks steht die Antwort in zwei Formen:

    * nach ``→``  — z. B. „1. Setze ein: *Magister ______ (sum).* → *est*“
    * nach ``—``  — z. B. „2. Übersetze: *X.* — „Übersetzung““

    Der Gedankenstrich ``—`` **im Aufgabentext** (etwa „*fīō* / *fītur* —
    dieselbe Form, aber …“) bleibt stehen; entfernt wird nur der Teil
    **hinter** der Antwort.

    Gibt (neuer Text, Liste der entfernten Antworten) zurück.
    """
    out_lines: list[str] = []
    removed: list[str] = []
    for line in body.split("\n"):
        stripped = line.strip()
        indent = line[: len(line) - len(line.lstrip())]

        # --- Fall 0: Korrekturhinweis in Klammern (Kapitel 11, Aufgabe 8)
        #     „8. *possuī?* (→ *potuī*) 9. *fertis* …“ — die Klammer samt
        #     Inhalt entfällt, die **Aufgaben** bleiben vollständig erhalten.
        if RE_KLAMMER_KORREKTUR.search(stripped):
            removed.append(RE_KLAMMER_KORREKTUR.search(stripped).group(0).strip(" ()"))
            out_lines.append(indent + RE_KLAMMER_KORREKTUR.sub("", stripped))
            continue

        # --- Fall 1: „1. Setze ein: … → *est*“ -------------------------
        if _ist_antwortzeile(stripped):
            pre, post = stripped.split("→", 1)
            removed.append(post.strip())
            out_lines.append(indent + pre.rstrip())
            continue

        # --- Fall 2: „2. Übersetze: … — „Übersetzung““ -----------------
        #         bzw.  „3. Erkläre: … — Begründung → Antwort“
        m = re.match(r"^(\d+\.\s+)(.*)$", stripped)
        if m and "—" in m.group(2):
            kopf, rest = m.group(1), m.group(2)
            dash_pos = rest.find("—")
            tail = rest[dash_pos + 1 :].strip()
            # Antwortteil: Zitat, lateinische Form oder Begründungssatz
            ist_antwort = (
                tail.startswith(("„", '"', "*"))
                or "→" in tail
                or re.match(r"^(Weil|Da\b|Denn|Wenn|Der|Die|Das|Als)", tail)
                # „— kein Partizip, aber: „Der Feldherr …““ (Kapitel 31)
                or re.match(r"^(kein|keine|keinen|keiner|keines)\b", tail)
            )
            if ist_antwort:
                if "→" in tail:
                    _, _, answer = tail.partition("→")
                    removed.append(answer.strip())
                else:
                    removed.append(tail)
                out_lines.append(indent + kopf + rest[:dash_pos].rstrip())
                continue

        out_lines.append(line)
    return "\n".join(out_lines), removed


def strip_simple_block(body: str) -> tuple[str, list[str]]:
    """Entfernt Antworten aus ``:::uebung``- und ``:::wiederholung``-Blöcken.

    Nur was wirklich eine **Antwort** ist, wird entfernt:

    * Kapitel 14: „1. *pulcher* → Komparativ, Superlativ“ — der Pfeil nennt
      die **gefragte** Form; die Antwort steht im Anhang.
    * Kapitel 38: „1. *Magister discipulōs monet.* → „Die Schüler ermahnen
      den Lehrer.““ — die bewusst **falsche** Übersetzung löst erst die
      Fehlersuche aus; sie bleibt stehen.
    """
    out_lines: list[str] = []
    removed: list[str] = []
    for line in body.split("\n"):
        stripped = line.strip()
        indent = line[: len(line) - len(line.lstrip())]

        # Korrekturhinweis in Klammern (Kapitel 11, Aufgabe 8):
        # „8. *possuī?* (→ *potuī*) 9. *fertis* …“ — die Klammer samt Inhalt
        # entfällt, die **Aufgaben** bleiben vollständig erhalten.
        if RE_KLAMMER_KORREKTUR.search(stripped):
            removed.append(RE_KLAMMER_KORREKTUR.search(stripped).group(0).strip(" ()"))
            out_lines.append(indent + RE_KLAMMER_KORREKTUR.sub("", stripped))
            continue

        if "→" in stripped:
            post = stripped.split("→", 1)[1].strip()
            if RE_FEHLER_QUELLE.match(post) or RE_AUFTRAG_FORM.match(post):
                out_lines.append(line)
                continue
        if _ist_antwortzeile(stripped):
            pre, post = stripped.split("→", 1)
            removed.append(post.strip())
            out_lines.append(indent + pre.rstrip())
            continue
        out_lines.append(line)
    return "\n".join(out_lines), removed


BLOCK_RE = re.compile(
    r"^(:::(uebung|wiederholung|check)[^\n]*\n)(.*?)(^:::\s*$)",
    re.M | re.S,
)


def process(path: Path) -> tuple[str, dict[str, list[str]]]:
    text = path.read_text(encoding="utf-8")
    found: dict[str, list[str]] = {"check": [], "uebung": [], "wiederholung": []}

    def repl(m: re.Match[str]) -> str:
        head, kind, body, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        if kind == "check":
            new_body, removed = strip_check_block(body)
        else:
            new_body, removed = strip_simple_block(body)
        found[kind].extend(removed)
        return head + new_body + tail

    new_text = BLOCK_RE.sub(repl, text)
    return new_text, found


def main() -> int:
    check_only = "--check" in sys.argv
    total = 0
    for path in sorted(BOOK.glob("*.md")):
        if path.name.startswith("54-anhang-loesungen"):
            continue
        new_text, found = process(path)
        n = sum(len(v) for v in found.values())
        if not n:
            continue
        total += n
        print(f"{path.name}: {n} Antwort(en) entfernt")
        for kind, items in found.items():
            for it in items:
                print(f"    [{kind}] {it[:110]}")
        if not check_only:
            path.write_text(new_text, encoding="utf-8")
    print(f"GESAMT: {total} Antwort(en) entfernt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
