#!/usr/bin/env python3
"""Baut das Latein-Lehrbuch aus den Markdown-Quellen.

    python3 build/build.py            # HTML + EPUB + PDF + Anki-CSV
    python3 build/build.py --html     # nur HTML
    python3 build/build.py --epub     # nur EPUB
    python3 build/build.py --pdf      # nur PDF
    python3 build/build.py --check    # Konsistenzprüfung

Quellen:   book/*.md (mit Frontmatter)  ->  dist/latein.html, dist/latein.epub, dist/latein.pdf
Glossar:   glossar/*.csv                ->  build/anki/*.csv (Anki-Import)
"""

from __future__ import annotations

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import md  # noqa: E402
import render  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(ROOT, "book")
DIST = os.path.join(ROOT, "dist")
GLOSSAR = os.path.join(ROOT, "glossar")
ANKI = os.path.join(ROOT, "build", "anki")

META = {
    "title": "Latein verstehen",
    "subtitle": "Ein modernes Lehrbuch zum Lesen, Übersetzen und Genießen der lateinischen Sprache",
    "meta": "Formenlehre · Syntax · Wortschatz · Übersetzungstechnik · Lektüre · Glossar der Fachbegriffe",
    "creator": "AuronOrigin",
    "uuid": "latein-verstehen-2026",
}


# --------------------------------------------------------------------------

def read_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    head = text[3:end]
    rest = text[end + 4:].lstrip("\n")
    data = {}
    for line in head.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            data[k.strip()] = v.strip().strip('"')
    return data, rest


def load_chapters() -> list[dict]:
    files = sorted(f for f in os.listdir(BOOK_DIR) if f.endswith(".md"))
    chapters = []
    for fn in files:
        path = os.path.join(BOOK_DIR, fn)
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        fm, body = read_frontmatter(raw)
        blocks = md.parse(expand_placeholders(body))
        title = fm.get("title") or fn[:-3]
        chapters.append({
            "file": fn,
            "title": title,
            "subtitle": fm.get("subtitle", ""),
            "part": fm.get("part", ""),
            "anchor": render.slug(title),
            "blocks": blocks,
            "hidden": fm.get("hidden", "") == "yes",
        })
    return chapters


def expand_placeholders(body: str) -> str:
    """Ersetzt {{glossar}} und {{vokabeln:A}} durch automatisch erzeugte Tabellen."""
    def glossary(m):
        return glossary_table()

    def vocab(m):
        return vocab_table(m.group(1).upper())

    body = re.sub(r"\{\{glossar\}\}", glossary, body)
    body = re.sub(r"\{\{vokabeln:([A-E])\}\}", vocab, body)
    return body


def glossary_table() -> str:
    path = os.path.join(GLOSSAR, "begriffe.csv")
    if not os.path.exists(path):
        return "*(Glossar-Tabelle noch nicht vorhanden.)*"
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    out = ["| Begriff | Herkunft | Bedeutung |", "|---|---|---|"]
    for r in sorted(rows, key=lambda x: x["begriff"].lower()):
        out.append(f"| **{r['begriff']}** | {r.get('herkunft', '')} | {r['bedeutung']} |")
    return "\n".join(out)


def vocab_table(stufe: str) -> str:
    path = os.path.join(GLOSSAR, "vokabeln.csv")
    if not os.path.exists(path):
        return "*(Vokabeltabelle noch nicht vorhanden.)*"
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    sel = [r for r in rows if r.get("stufe", "").upper() == stufe]
    out = ["| Latein | Deutsch | Stamm | Wortfamilie |", "|---|---|---|---|"]
    for r in sel:
        out.append(f"| {r['latein']} | {r['deutsch']} | {r.get('stamm', '')} | {r.get('familie', '')} |")
    return "\n".join(out)


def build_all(what: list[str]) -> None:
    os.makedirs(DIST, exist_ok=True)
    os.makedirs(ANKI, exist_ok=True)
    chapters = load_chapters()
    css_path = os.path.join(ROOT, "build", "style.css")
    with open(css_path, encoding="utf-8") as fh:
        css = fh.read()

    if "html" in what:
        out = os.path.join(DIST, "latein.html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(render.build_html(chapters, META, css))
        print(f"HTML  -> {out} ({os.path.getsize(out)//1024} KB)")

    if "epub" in what:
        out = os.path.join(DIST, "latein.epub")
        data = render.build_epub(chapters, META, css)
        with open(out, "wb") as fh:
            fh.write(data)
        print(f"EPUB  -> {out} ({os.path.getsize(out)//1024} KB)")

    if "pdf" in what:
        out = os.path.join(DIST, "latein.pdf")
        try:
            data = render.build_pdf(chapters, META, ROOT)
            with open(out, "wb") as fh:
                fh.write(data)
            print(f"PDF   -> {out} ({os.path.getsize(out)//1024} KB)")
        except ImportError:
            print("PDF   -> übersprungen (reportlab nicht installiert: pip install reportlab)")

    if "anki" in what:
        build_anki()
    if "check" in what:
        check(chapters)


def build_anki() -> None:
    src = os.path.join(GLOSSAR, "vokabeln.csv")
    if not os.path.exists(src):
        print("ANKI  -> keine glossar/vokabeln.csv gefunden")
        return
    with open(src, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    de_lat = os.path.join(ANKI, "latein_de_lat.csv")
    lat_de = os.path.join(ANKI, "latein_lat_de.csv")
    with open(de_lat, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Front", "Back", "Tags", "Hinweis"])
        for r in rows:
            if r.get("stufe", "").lower() in ("d", "e"):
                continue
            w.writerow([r["deutsch"], r["latein"], f'latein stufe-{r.get("stufe", "")}',
                        r.get("familie", "")])
    with open(lat_de, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Front", "Back", "Tags", "Hinweis"])
        for r in rows:
            if r.get("stufe", "").lower() in ("d", "e"):
                continue
            w.writerow([r["latein"], r["deutsch"], f'latein stufe-{r.get("stufe", "")}',
                        r.get("familie", "")])
    print(f"ANKI  -> {de_lat}, {lat_de} ({len(rows)} Einträge)")


def check(chapters: list[dict]) -> None:
    """Einfache Konsistenzprüfung des Buches."""
    problems: list[str] = []

    # 1. Kapitel-IDs eindeutig
    seen: dict[str, str] = {}
    for ch in chapters:
        if ch["anchor"] in seen:
            problems.append(f"Doppelte Kapitel-Überschrift: {ch['title']} ({ch['file']} und {seen[ch['anchor']]})")
        seen[ch["anchor"]] = ch["file"]

    # 2. Überschriften-Ebenen: keine Sprünge > 1
    for ch in chapters:
        prev = 0
        for h in md.headings(ch["blocks"]):
            if prev and h["level"] > prev + 1:
                problems.append(f"Sprung in Überschriftsebenen in {ch['file']}: h{prev} -> h{h['level']}")
            prev = h["level"]

    # 3. Kästen mit unbekannter Art
    def walk(blocks):
        for b in blocks:
            if b["type"] == "box":
                if b["kind"] not in md.BOX_KINDS:
                    problems.append(f"Unbekannte Box-Art '{b['kind']}' in {ch['file']}")
            if b["type"] in ("box", "quote"):
                walk(b["blocks"])
    for ch in chapters:
        walk(ch["blocks"])

    # 4. Pflicht-Bausteine je Kapitel (Vorwort und Einleitungskapitel ausgenommen)
    REQUIRED = {"ziel", "wortschatz", "uebung", "wiederholung", "check"}
    for ch in chapters:
        if ch.get("part", "").startswith("Vorwort"):
            continue
        kinds = set()
        def collect(blocks):
            for b in blocks:
                if b["type"] == "box":
                    kinds.add(b["kind"])
                if b["type"] in ("box", "quote"):
                    collect(b["blocks"])
        collect(ch["blocks"])
        missing = REQUIRED - kinds
        if missing:
            problems.append(
                f"{ch['file']}: fehlende Bausteine: {', '.join(sorted(missing))}")

    # 5. Leere Kapitel / fehlende Überschrift
    for ch in chapters:
        if not ch["blocks"]:
            problems.append(f"{ch['file']}: Kapitel ist leer")
        if not any(b["type"] == "heading" for b in ch["blocks"]):
            problems.append(f"{ch['file']}: keine Überschrift im Kapitel")

    print(f"CHECK -> {len(problems)} Problem(e)")
    for p in problems[:50]:
        print("  -", p)


def main() -> None:
    args = sys.argv[1:]
    if not args:
        args = ["html", "epub", "pdf", "anki"]
    what = []
    for a in args:
        if a in ("--html",):
            what.append("html")
        elif a in ("--epub",):
            what.append("epub")
        elif a in ("--pdf",):
            what.append("pdf")
        elif a in ("--anki",):
            what.append("anki")
        elif a in ("--check",):
            what.append("check")
        elif a in ("--all",):
            what += ["html", "epub", "pdf", "anki", "check"]
    build_all(what)


if __name__ == "__main__":
    main()
