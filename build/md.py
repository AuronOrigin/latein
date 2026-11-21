"""Minimaler Markdown-Parser für das Latein-Lehrbuch.

Erzeugt ein Dokumentmodell aus Blöcken und Inline-Knoten, das von den
Renderern (HTML, EPUB, PDF) gemeinsam genutzt wird.

Unterstützte Syntax:
  # Überschrift … ###### Überschrift
  Absätze (durch Leerzeile getrennt)
  - ungeordnete / 1. geordnete Listen (Einrückung = 2 Spaces)
  | Tabellen | mit | Kopfzeile |
  ``` fenced code ```
  > Zitatblöcke
  :::kind[ Titel] … :::   (eigene Kästen, s. BOX_KINDS)
  --- horizontale Linie
  <!-- pagebreak -->     (nur für den PDF-Umbruch)
  ![alt](pfad)           (Abbildungen)

Inline:
  **fett**  *kursiv*  `code`  ==hervorgehoben==  @farbe{…}  [Text](Link)
"""

from __future__ import annotations

import re

# --------------------------------------------------------------------------
# Bausteine
# --------------------------------------------------------------------------

BOX_KINDS = {
    "ziel": ("Lernziele", "ziel"),
    "wortschatz": ("Wortschatz", "wortschatz"),
    "begriff": ("Begriffsbox", "begriff"),
    "warn": ("Stolperfallen", "warn"),
    "merksatz": ("Merksatz", "merksatz"),
    "kultur": ("Kulturbox", "kultur"),
    "mikro": ("Mikroübung (30 Sekunden)", "mikro"),
    "uebung": ("Übungen", "uebung"),
    "loesung": ("Lösungen", "loesung"),
    "wiederholung": ("Wiederholungsfach", "wiederholung"),
    "check": ("Prüfungscheck", "check"),
    "vertiefung": ("Vertiefung & Quellen", "vertiefung"),
    "info": ("Hinweis", "info"),
}

COLORS = {
    "subj": "#1a7f37",
    "verb": "#1f4fd8",
    "obj": "#c2410c",
    "kasus": "#7c3aed",
    "wichtig": "#b45309",
    "rot": "#b91c1c",
    "gruen": "#1a7f37",
    "blau": "#1f4fd8",
    "grau": "#6b7280",
}

INLINE_RE = re.compile(
    r"(?P<code>`[^`]+`)"
    r"|(?P<link>\[[^\]]+\]\([^)]+\))"
    r"|(?P<image>!\[[^\]]*\]\([^)]+\))"
    r"|(?P<color>@(?P<cname>[a-z]+)\{[^}]*\})"
    r"|(?P<bold>\*\*[^*]+\*\*)"
    r"|(?P<italic>(?<!\*)\*[^*]+\*(?!\*))"
    r"|(?P<mark>==[^=]+==)"
)

COLOR_MAP = {
    "subj": COLORS["subj"], "verb": COLORS["verb"], "obj": COLORS["obj"],
    "kasus": COLORS["kasus"], "wichtig": COLORS["wichtig"], "rot": COLORS["rot"],
    "gruen": COLORS["gruen"], "blau": COLORS["blau"], "grau": COLORS["grau"],
}


# --------------------------------------------------------------------------
# Inline
# --------------------------------------------------------------------------

def parse_inline(text: str) -> list[dict]:
    """Zerlegt einen Text in Inline-Knoten."""
    out: list[dict] = []
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append({"t": "text", "v": text[pos:m.start()]})
        if m.group("code"):
            out.append({"t": "code", "v": m.group("code")[1:-1]})
        elif m.group("image"):
            inner = m.group("image")[2:-1]
            alt, _, path = inner.partition("]")
            out.append({"t": "image", "v": path.strip(), "alt": alt.strip()})
        elif m.group("link"):
            inner = m.group("link")[1:-1]
            label, _, href = inner.partition("](")
            out.append({"t": "link", "v": label, "href": href.rstrip(")")})
        elif m.group("color"):
            cname = m.group("cname")
            inner = m.group("color")
            body = inner[inner.index("{") + 1:inner.rindex("}")]
            out.append({"t": "color", "v": body, "c": COLOR_MAP.get(cname, COLORS["grau"])})
        elif m.group("bold"):
            out.append({"t": "bold", "v": m.group("bold")[2:-2]})
        elif m.group("italic"):
            out.append({"t": "italic", "v": m.group("italic")[1:-1]})
        elif m.group("mark"):
            out.append({"t": "mark", "v": m.group("mark")[2:-2]})
        pos = m.end()
    if pos < len(text):
        out.append({"t": "text", "v": text[pos:]})
    return out


def plain(nodes: list[dict]) -> str:
    """Inline-Knoten als reiner Text (für Inhaltsverzeichnisse u. a.)."""
    return "".join(n.get("v", "") for n in nodes)


# --------------------------------------------------------------------------
# Blöcke
# --------------------------------------------------------------------------

def _split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_table_sep(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return False
    cells = _split_table_row(stripped)
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c != "")


def parse(md: str) -> list[dict]:
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[dict] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()
        i_start = i

        # Leerzeile
        if not stripped:
            i += 1
            continue

        # Seitenumbruch-Marker
        if stripped == "<!-- pagebreak -->":
            blocks.append({"type": "pagebreak"})
            i += 1
            continue

        # Horizontale Linie
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            blocks.append({"type": "hr"})
            i += 1
            continue

        # Eigene Kästen
        m = re.match(r"^:::(\w+)(?:\s*\[(.*?)\]|\s+(.+?))?\s*$", stripped)
        if m:
            kind = m.group(1)
            title = m.group(2) or m.group(3)
            body: list[dict] = []
            i += 1
            depth = 1
            while i < n:
                s = lines[i].strip()
                if s == ":::":
                    i += 1
                    break
                body.append(lines[i])
                i += 1
            label, css = BOX_KINDS.get(kind, (kind.title(), kind))
            blocks.append({
                "type": "box",
                "kind": kind,
                "css": css,
                "label": title or label,
                "blocks": parse("\n".join(body)),
            })
            continue

        # Überschrift
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            blocks.append({"type": "heading", "level": level, "inlines": parse_inline(m.group(2))})
            i += 1
            continue

        # Codeblock
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append({"type": "code", "lang": lang, "v": "\n".join(buf)})
            continue

        # Tabelle
        if stripped.startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            header = [parse_inline(c) for c in _split_table_row(lines[i])]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([parse_inline(c) for c in _split_table_row(lines[i])])
                i += 1
            blocks.append({"type": "table", "header": header, "rows": rows})
            continue

        # Zitat
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append({"type": "quote", "blocks": parse("\n".join(buf))})
            continue

        # Listen
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            block, i = _parse_list(lines, i)
            blocks.append(block)
            continue

        # Absatz
        buf = []
        while i < n:
            s = lines[i].strip()
            if (not s or s.startswith(("#", "|", ">", "```", ":::"))
                    or re.match(r"^(\s*)([-*+]|\d+[.)])\s+", lines[i])
                    or re.fullmatch(r"-{3,}", s)):
                break
            buf.append(s)
            i += 1
        if buf:
            blocks.append({"type": "para", "inlines": parse_inline(" ".join(buf))})

        if i == i_start:  # Sicherheitsnetz gegen Endlosschleifen
            i += 1

    return blocks


def _parse_list(lines: list[str], i: int):
    """Parst eine Liste (mit zweistufiger Verschachtelung)."""
    start = i
    items: list[dict] = []
    ordered = bool(re.match(r"^\s*\d+[.)]\s", lines[i]))
    base_indent = len(lines[i]) - len(lines[i].lstrip())

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            # Leerzeile: Liste endet, wenn die nächste Zeile kein Listenpunkt ist
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and re.match(r"^\s*(?:[-*+]|\d+[.)])\s", lines[j]):
                i = j
                continue
            break
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if not m:
            break
        indent = len(m.group(1))
        if indent < base_indent:
            break
        if indent >= base_indent + 2:
            # verschachtelte Liste
            sub, i = _parse_list(lines, i)
            if items:
                items[-1].setdefault("children", []).append(sub)
            continue
        text = m.group(3)
        i += 1
        # Fortsetzungszeilen (eingerückt, kein eigener Punkt)
        extra = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(\s*)([-*+]|\d+[.)])\s+", lines[i]) and not lines[i].strip().startswith(("#", "|", ">")):
            extra.append(lines[i].strip())
            i += 1
        if extra:
            text += " " + " ".join(extra)
        items.append({"inlines": parse_inline(text)})

    return ({"type": "list", "ordered": ordered, "items": items}, i if i > start else start + 1)


def headings(blocks: list[dict]) -> list[dict]:
    """Sammelt Überschriften für das Inhaltsverzeichnis."""
    out = []
    for b in blocks:
        if b["type"] == "heading":
            out.append({"level": b["level"], "text": plain(b["inlines"])})
        elif b["type"] == "box":
            out.extend(headings(b["blocks"]))
        elif b["type"] == "quote":
            out.extend(headings(b["blocks"]))
    return out
