"""Renderer: Dokumentmodell -> HTML, EPUB 3, PDF.

Alle drei Ausgabeformate entstehen aus demselben Blockmodell (build/md.py),
damit Inhalt und Struktur garantiert identisch sind.
"""

from __future__ import annotations

import html as _html
import os
import re
import zipfile
from typing import Any

# --------------------------------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------------------------------

def slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", s).strip("-") or "abschnitt"


def esc(text: str) -> str:
    return _html.escape(text, quote=False)


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

def inline_html(nodes: list[dict]) -> str:
    out = []
    for n in nodes:
        t = n["t"]
        if t == "text":
            out.append(esc(n["v"]))
        elif t == "bold":
            out.append(f"<strong>{_inner_html(n)}</strong>")
        elif t == "italic":
            out.append(f"<em>{_inner_html(n)}</em>")
        elif t == "code":
            out.append(f"<code>{esc(n['v'])}</code>")
        elif t == "mark":
            out.append(f"<mark>{_inner_html(n)}</mark>")
        elif t == "color":
            out.append(f'<span style="color:{n["c"]};font-weight:600">{esc(n["v"])}</span>')
        elif t == "link":
            out.append(f'<a href="{esc(n["href"])}">{esc(n["v"])}</a>')
        elif t == "image":
            out.append(f'<img src="{esc(n["v"])}" alt="{esc(n.get("alt", ""))}" />')
    return "".join(out)


def _inner_html(node: dict) -> str:
    """Innerhalb einer Hervorhebung: verschachtelte Knoten oder reiner Text."""
    if "children" in node:
        return inline_html(node["children"])
    return esc(node.get("v", ""))


def blocks_html(blocks: list[dict]) -> str:
    out = []
    for b in blocks:
        t = b["type"]
        if t == "heading":
            lvl = b["level"]
            out.append(f'<h{lvl} id="{slug(_plain(b["inlines"]))}">{inline_html(b["inlines"])}</h{lvl}>')
        elif t == "para":
            out.append(f"<p>{inline_html(b['inlines'])}</p>")
        elif t == "list":
            tag = "ol" if b["ordered"] else "ul"
            items = []
            for it in b["items"]:
                inner = f"<li>{inline_html(it['inlines'])}"
                if it.get("children"):
                    inner += blocks_html(it["children"])
                items.append(inner + "</li>")
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
        elif t == "table":
            head = "".join(f"<th>{inline_html(c)}</th>" for c in b["header"])
            rows = "".join("<tr>" + "".join(f"<td>{inline_html(c)}</td>" for c in r) + "</tr>"
                           for r in b["rows"])
            out.append(f'<div class="tw"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif t == "code":
            out.append(f'<pre><code>{esc(b["v"])}</code></pre>')
        elif t == "quote":
            out.append(f'<blockquote>{blocks_html(b["blocks"])}</blockquote>')
        elif t == "box":
            out.append(
                f'<div class="box box-{b["css"]}"><div class="box-label">{inline_html(b.get("label_nodes") or [])}</div>'
                f'{blocks_html(b["blocks"])}</div>')
        elif t == "hr":
            out.append("<hr />")
        elif t == "pagebreak":
            out.append('<div class="pagebreak"></div>')
    return "\n".join(out)


def _plain(nodes: list[dict]) -> str:
    return "".join(n.get("v", "") for n in nodes)


def build_html(chapters: list[dict], meta: dict, css: str) -> str:
    parts: dict[str, list[dict]] = {}
    order: list[str] = []
    for ch in chapters:
        p = ch.get("part", "")
        if p not in parts:
            parts[p] = []
            order.append(p)
        parts[p].append(ch)

    toc = []
    for p in order:
        if p:
            toc.append(f'<li class="toc-part">{esc(p)}</li>')
        for ch in parts[p]:
            if ch.get("hidden"):
                continue
            toc.append(f'<li><a href="#{ch["anchor"]}">{esc(ch["title"])}</a></li>')

    body = []
    for p in order:
        if p:
            body.append(f'<h1 class="part-title">{esc(p)}</h1>')
        for ch in parts[p]:
            body.append(f'<section class="chapter" id="{ch["anchor"]}">')
            body.append(f'<h2 class="ch-title">{esc(ch["title"])}</h2>')
            if ch.get("subtitle"):
                body.append(f'<p class="ch-sub">{inline_html(ch.get("subtitle_nodes") or [])}</p>')
            body.append(blocks_html(ch["blocks"]))
            body.append("</section>")

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(meta.get('title', 'Latein verstehen'))}</title>
<style>
{css}
</style>
</head>
<body>
<div class="cover">
  <h1>{esc(meta.get('title', 'Latein verstehen'))}</h1>
  <p class="cover-sub">{esc(meta.get('subtitle', ''))}</p>
  <p class="cover-meta">{esc(meta.get('meta', ''))}</p>
</div>
<nav class="toc">
  <h2>Inhalt</h2>
  <ul>
  {''.join(toc)}
  </ul>
</nav>
{''.join(body)}
</body>
</html>
"""


# --------------------------------------------------------------------------
# EPUB 3
# --------------------------------------------------------------------------

def build_epub(chapters: list[dict], meta: dict, css: str) -> bytes:
    import io

    files: dict[str, str] = {}
    spine = []
    nav_items = []

    parts_order: list[str] = []
    for ch in chapters:
        p = ch.get("part", "")
        if p not in parts_order:
            parts_order.append(p)

    for idx, ch in enumerate(chapters):
        fname = f"ch{idx:02d}.xhtml"
        body = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<!DOCTYPE html>',
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">',
            "<head>",
            '<meta charset="utf-8" />',
            f'<title>{esc(ch["title"])}</title>',
            '<link rel="stylesheet" type="text/css" href="style.css" />',
            "</head><body>",
        ]
        if ch.get("part"):
            body.append(f'<p class="part">{esc(ch["part"])}</p>')
        body.append(f'<h1 id="{ch["anchor"]}">{esc(ch["title"])}</h1>')
        if ch.get("subtitle"):
            body.append(f'<p class="subtitle">{inline_html(ch.get("subtitle_nodes") or [])}</p>')
        body.append(blocks_html(ch["blocks"]))
        body.append("</body></html>")
        files[f"OEBPS/{fname}"] = "\n".join(body)
        spine.append(fname)
        nav_items.append((ch["title"], fname))

    nav = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">',
        "<head><meta charset=\"utf-8\" /><title>Inhalt</title>"
        '<link rel="stylesheet" type="text/css" href="style.css" /></head><body>',
        '<nav epub:type="toc" id="toc"><h1>Inhalt</h1><ol>',
    ]
    for title, fname in nav_items:
        nav.append(f'<li><a href="{fname}">{esc(title)}</a></li>')
    nav.append("</ol></nav></body></html>")
    files["OEBPS/nav.xhtml"] = "\n".join(nav)

    files["OEBPS/style.css"] = css

    opf = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">',
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">',
        f'<dc:identifier id="uid">urn:uuid:{meta.get("uuid", "latein-verstehen")}</dc:identifier>',
        f'<dc:title>{esc(meta.get("title", "Latein verstehen"))}</dc:title>',
        f'<dc:language>de</dc:language>',
        f'<dc:creator>{esc(meta.get("creator", "AuronOrigin"))}</dc:creator>',
        '<meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>',
        "</metadata>",
        "<manifest>",
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="css" href="style.css" media-type="text/css"/>',
    ]
    for i, (title, fname) in enumerate(nav_items):
        opf.append(f'<item id="c{i}" href="{fname}" media-type="application/xhtml+xml"/>')
    opf.append("</manifest>")
    opf.append("<spine>")
    for fname in spine:
        opf.append(f'<itemref idref="{fname}"/>')
    opf.append("</spine></package>")
    files["OEBPS/content.opf"] = "\n".join(opf)

    files["META-INF/container.xml"] = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '  <rootfiles>\n'
        '    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n'
        "  </rootfiles>\n</container>"
    )

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for name, content in files.items():
            z.writestr(name, content)
    return buf.getvalue()


# --------------------------------------------------------------------------
# PDF (reportlab)
# --------------------------------------------------------------------------

def build_pdf(chapters: list[dict], meta: dict, base_dir: str = ".") -> bytes:
    import io
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate,
                                    PageBreak, PageTemplate, Paragraph, Preformatted,
                                    Spacer, Table, TableStyle)

    # --- Schriften ---
    fonts = {
        "DejaVu": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVu-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuMono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "DejaVuMono-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "DejaVuSerif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "DejaVuSerif-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    }
    for name, path in fonts.items():
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold",
                                   italic="DejaVu", boldItalic="DejaVu-Bold")
    pdfmetrics.registerFontFamily("DejaVuSerif", normal="DejaVuSerif", bold="DejaVuSerif-Bold",
                                   italic="DejaVuSerif", boldItalic="DejaVuSerif-Bold")
    pdfmetrics.registerFontFamily("DejaVuMono", normal="DejaVuMono", bold="DejaVuMono-Bold",
                                   italic="DejaVuMono", boldItalic="DejaVuMono-Bold")

    F, FB, FM, FS = "DejaVu", "DejaVu-Bold", "DejaVuMono", "DejaVuSerif"

    BOX_BG = {
        "ziel": colors.HexColor("#eef6ff"), "wortschatz": colors.HexColor("#f2f7f2"),
        "begriff": colors.HexColor("#fdf6e3"), "warn": colors.HexColor("#fdeceb"),
        "merksatz": colors.HexColor("#eaf7ee"), "kultur": colors.HexColor("#f3eefb"),
        "mikro": colors.HexColor("#f4f7f9"), "uebung": colors.HexColor("#f7f7f7"),
        "loesung": colors.HexColor("#f0f7f4"), "wiederholung": colors.HexColor("#f2f2fb"),
        "check": colors.HexColor("#fdf1e7"), "vertiefung": colors.HexColor("#f5f5f5"),
        "info": colors.HexColor("#f5f5f5"),
    }
    BOX_BAR = {
        "ziel": colors.HexColor("#1f4fd8"), "wortschatz": colors.HexColor("#1a7f37"),
        "begriff": colors.HexColor("#b45309"), "warn": colors.HexColor("#b91c1c"),
        "merksatz": colors.HexColor("#1a7f37"), "kultur": colors.HexColor("#7c3aed"),
        "mikro": colors.HexColor("#334155"), "uebung": colors.HexColor("#111827"),
        "loesung": colors.HexColor("#0f766e"), "wiederholung": colors.HexColor("#4338ca"),
        "check": colors.HexColor("#c2410c"), "vertiefung": colors.HexColor("#6b7280"),
        "info": colors.HexColor("#6b7280"),
    }

    styles = getSampleStyleSheet()
    S = {
        "body": ParagraphStyle("body", parent=styles["BodyText"], fontName=F, fontSize=9.6,
                                leading=13.6, alignment=TA_JUSTIFY, spaceAfter=5),
        "h1": ParagraphStyle("h1", parent=styles["Heading1"], fontName=FS, fontSize=17,
                              leading=21, spaceBefore=2, spaceAfter=10, textColor=colors.HexColor("#1f2937")),
        "h2": ParagraphStyle("h2", parent=styles["Heading2"], fontName=F, fontSize=12.4,
                              leading=15, spaceBefore=11, spaceAfter=5, textColor=colors.HexColor("#1f4fd8")),
        "h3": ParagraphStyle("h3", parent=styles["Heading3"], fontName=F, fontSize=10.6,
                              leading=13.4, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#334155")),
        "part": ParagraphStyle("part", parent=styles["Heading1"], fontName=FS, fontSize=20,
                               leading=24, spaceBefore=0, spaceAfter=14, alignment=TA_CENTER,
                               textColor=colors.HexColor("#7c2d12")),
        "sub": ParagraphStyle("sub", parent=styles["BodyText"], fontName=F, fontSize=10.4,
                              leading=14, textColor=colors.HexColor("#4b5563"), spaceAfter=10),
        "li": ParagraphStyle("li", parent=styles["BodyText"], fontName=F, fontSize=9.6,
                             leading=13.4, spaceAfter=2, alignment=TA_JUSTIFY),
        "code": ParagraphStyle("code", parent=styles["Code"], fontName=FM, fontSize=8.2,
                                leading=11, backColor=colors.HexColor("#f4f4f5"), borderPadding=4,
                                spaceBefore=4, spaceAfter=7),
        "cell": ParagraphStyle("cell", parent=styles["BodyText"], fontName=F, fontSize=8.6,
                               leading=11.4, spaceAfter=0),
        "cellh": ParagraphStyle("cellh", parent=styles["BodyText"], fontName=FB, fontSize=8.6,
                                leading=11.4, spaceAfter=0, textColor=colors.white),
        "boxlabel": ParagraphStyle("boxlabel", parent=styles["BodyText"], fontName=FB,
                                   fontSize=8.6, leading=11, textColor=colors.white, spaceAfter=0),
        "quote": ParagraphStyle("quote", parent=styles["BodyText"], fontName=FS, fontSize=10.4,
                                leading=14.4, alignment=TA_CENTER, leftIndent=12, rightIndent=12,
                                textColor=colors.HexColor("#374151")),
        "toc": ParagraphStyle("toc", parent=styles["BodyText"], fontName=F, fontSize=9.4, leading=13),
        "tocpart": ParagraphStyle("tocpart", parent=styles["BodyText"], fontName=FB, fontSize=11,
                                  leading=16, spaceBefore=7),
        "covertitle": ParagraphStyle("covertitle", parent=styles["Title"], fontName=FS, fontSize=26,
                                     leading=32, alignment=TA_CENTER, textColor=colors.HexColor("#1f2937")),
        "coversub": ParagraphStyle("coversub", parent=styles["BodyText"], fontName=F, fontSize=12.5,
                                   leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#4b5563")),
    }

    # --- Inline -> reportlab-Markup ---
    def rl(nodes: list[dict]) -> str:
        out = []
        for n in nodes:
            t = n["t"]
            if t == "text":
                out.append(esc(n["v"]).replace(" ", "&nbsp;"))
            elif t == "bold":
                out.append(f'<b>{rl_inner(n)}</b>')
            elif t == "italic":
                out.append(f'<i>{rl_inner(n)}</i>')
            elif t == "code":
                out.append(f'<font face="{FM}">{esc(n["v"])}</font>')
            elif t == "mark":
                out.append(f'<font backColor="#fff2b2">{rl_inner(n)}</font>')
            elif t == "color":
                out.append(f'<font color="{n["c"]}"><b>{esc(n["v"])}</b></font>')
            elif t == "link":
                out.append(f'<link href="{esc(n["href"])}" color="#1f4fd8">{esc(n["v"])}</link>')
            elif t == "image":
                out.append(f'<i>[{esc(n.get("alt", "Abbildung"))}]</i>')
        return "".join(out)

    def rl_upper(nodes: list[dict]) -> str:
        """Wie rl(), aber der Text wird in Grossbuchstaben gesetzt."""
        out = []
        for n in nodes:
            if n["t"] == "text":
                out.append(esc(n["v"].upper()).replace(" ", "&nbsp;"))
            elif n["t"] == "bold":
                out.append(f'<b>{rl_upper(n.get("children") or [])}</b>')
            elif n["t"] == "italic":
                out.append(f'<i>{rl_upper(n.get("children") or [])}</i>')
            elif n["t"] == "mark":
                out.append(f'<font backColor="#fff2b2">{rl_upper(n.get("children") or [])}</font>')
            else:
                out.append(rl([n]))
        return "".join(out)

    def rl_inner(node: dict) -> str:
        if "children" in node:
            return rl(node["children"])
        return esc(node.get("v", ""))

    # --- Block -> Flowables ---
    def flow(blocks: list[dict], level: int = 0) -> list[Any]:
        story: list[Any] = []
        for b in blocks:
            t = b["type"]
            if t == "heading":
                lvl = min(b["level"], 3)
                story.append(Paragraph(rl(b["inlines"]), S[f"h{lvl}"]))
            elif t == "para":
                story.append(Paragraph(rl(b["inlines"]), S["body"]))
            elif t == "list":
                for it in b["items"]:
                    txt = rl(it["inlines"])
                    story.append(Paragraph(txt, S["li"], bulletText="•"))
                    if it.get("children"):
                        story.append(Spacer(1, 2))
                        story.extend(flow(it["children"], level + 1))
            elif t == "table":
                data = [[Paragraph(rl(c), S["cellh"]) for c in b["header"]]]
                for r in b["rows"]:
                    data.append([Paragraph(rl(c), S["cell"]) for c in r])
                ncols = len(b["header"])
                avail = A4[0] - 2 * 20 * mm
                widths = [avail / ncols] * ncols
                tb = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
                tb.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#374151")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9ca3af")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f7f9")]),
                ]))
                story.append(Spacer(1, 3))
                story.append(tb)
                story.append(Spacer(1, 7))
            elif t == "code":
                story.append(Preformatted(b["v"], S["code"]))
            elif t == "quote":
                inner = flow(b["blocks"])
                for el in inner:
                    if isinstance(el, Paragraph):
                        el.style = S["quote"]
                story.extend(inner)
            elif t == "box":
                inner = flow(b["blocks"])
                label = Table([[Paragraph(rl_upper(b.get("label_nodes") or []), S["boxlabel"])]],
                              colWidths=[A4[0] - 2 * 20 * mm - 8])
                label.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), BOX_BAR.get(b["css"], colors.HexColor("#4b5563"))),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]))
                inner_table = Table([[inner]], colWidths=[A4[0] - 2 * 20 * mm - 8])
                inner_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), BOX_BG.get(b["css"], colors.HexColor("#f7f7f7"))),
                    ("BOX", (0, 0), (-1, -1), 0.6, BOX_BAR.get(b["css"], colors.HexColor("#4b5563"))),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]))
                story.append(Spacer(1, 3))
                story.append(label)
                story.append(inner_table)
                story.append(Spacer(1, 7))
            elif t == "hr":
                story.append(Spacer(1, 5))
            elif t == "pagebreak":
                story.append(PageBreak())
        return story

    # --- Dokument ---
    class BookDoc(BaseDocTemplate):
        def __init__(self, filename, **kw):
            BaseDocTemplate.__init__(self, filename, **kw)
            frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
            self.addPageTemplates([PageTemplate(id="normal", frames=[frame], onPage=self.deco)])
            self.chapter_title = ""

        def deco(self, canv, doc):
            canv.saveState()
            canv.setFont(F, 7.5)
            canv.setFillColor(colors.HexColor("#6b7280"))
            canv.drawString(self.leftMargin, 11 * mm, meta.get("title", ""))
            canv.drawRightString(A4[0] - self.rightMargin, 11 * mm, str(doc.page))
            canv.setStrokeColor(colors.HexColor("#d1d5db"))
            canv.setLineWidth(0.4)
            canv.line(self.leftMargin, 14 * mm, A4[0] - self.rightMargin, 14 * mm)
            canv.restoreState()

        def afterFlowable(self, flowable):
            if isinstance(flowable, Paragraph):
                style = flowable.style.name
                if style in ("h1", "h2"):
                    txt = re.sub(r"<[^>]+>", "", flowable.getPlainText())
                    key = f"bk{self.seq.nextf('bm')}"
                    self.canv.bookmarkPage(key)
                    self.canv.addOutlineEntry(txt, key, 0 if style == "h1" else 1)
                    self.notify("TOCEntry", (0, txt, self.page))
                if style == "h1":
                    self.chapter_title = flowable.getPlainText()

    buf = io.BytesIO()
    doc = BookDoc(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=18 * mm,
                  topMargin=18 * mm, bottomMargin=20 * mm,
                  title=meta.get("title", "Latein verstehen"),
                  author=meta.get("creator", "AuronOrigin"),
                  subject=meta.get("subtitle", ""),
                  creator="build/build.py")
    story: list[Any] = []

    # Titelseite
    story.append(Spacer(1, 55 * mm))
    story.append(Paragraph(esc(meta.get("title", "Latein verstehen")), S["covertitle"]))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(esc(meta.get("subtitle", "")), S["coversub"]))
    story.append(Spacer(1, 14 * mm))
    story.append(Paragraph(esc(meta.get("meta", "")), S["coversub"]))
    story.append(PageBreak())

    # Inhaltsverzeichnis
    story.append(Paragraph("Inhalt", S["h1"]))
    for ch in chapters:
        if ch.get("part"):
            story.append(Paragraph(esc(ch["part"]), S["tocpart"]))
        story.append(Paragraph(esc(ch["title"]), S["toc"]))
    story.append(PageBreak())

    for ch in chapters:
        if ch.get("part"):
            story.append(Paragraph(esc(ch["part"]), S["part"]))
        story.append(Paragraph(esc(ch["title"]), S["h1"]))
        if ch.get("subtitle"):
            story.append(Paragraph(rl(ch.get("subtitle_nodes") or []), S["sub"]))
        story.extend(flow(ch["blocks"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    return buf.getvalue()
