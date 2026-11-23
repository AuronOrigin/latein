# Latein verstehen

Ein modernes Lehrbuch zum Lesen, Übersetzen und Genießen der lateinischen Sprache —
auf Deutsch, schulneutral, als Arbeitsheft **und** Lösungsbuch in einem.

**56 Kapitel** von der Aussprache über Formenlehre, Syntax und Übersetzungskunst
bis zu zehn Lektüretexten mit Wort-für-Wort-Übersetzung. Kapitel 01–53 enthalten
Aufgaben **ohne** Lösungen; Anhang V (Kapitel 54) enthält die Lösung zu jeder
Bausteinaufgabe.

---

## Schnellstart: PDF erzeugen

```bash
git clone https://github.com/AuronOrigin/latein.git
cd latein
pip install reportlab
python3 build/build.py --pdf
```

Das Ergebnis liegt in `dist/latein.pdf`. Alle Formate auf einmal:

```bash
python3 build/build.py --all
```

| Datei | Inhalt | Größe |
|---|---|---|
| `dist/latein.pdf` | Druckfassung mit Lesezeichen, 329 Seiten | ~1,2 MB |
| `dist/latein.epub` | EPUB 3 für E-Reader und Tablets | ~319 KB |
| `dist/latein.html` | self-contained, druckoptimiert | ~958 KB |
| `build/anki/*.csv` | vier Anki-Stapel (siehe unten) | |

> **Ohne Python?** `dist/latein.html` ist vollständig selbstenthalten (keine
> externen CSS- oder Schriftdateien) und enthält ein `@media print`-Stylesheet.
> Datei im Browser öffnen → **Strg+P** → „Als PDF speichern“.

---

## Voraussetzungen

| | |
|---|---|
| Python | 3.9 oder neuer (getestet mit 3.11) |
| `reportlab` | **nur** für den PDF-Export: `pip install reportlab` |
| `fonttools` | **nur** zum Erneuern der Schriftschnitte: `pip install fonttools` |

HTML, EPUB und der Anki-Export laufen mit der Standardbibliothek allein —
keine Installation nötig. Fehlt `reportlab`, überspringt der Build den PDF-Teil
mit einer klaren Meldung und erzeugt alle anderen Formate.

---

## Build-Befehle

```bash
python3 build/build.py --html     # nur HTML
python3 build/build.py --epub     # nur EPUB
python3 build/build.py --pdf      # nur PDF
python3 build/build.py --anki     # nur Anki-CSV
python3 build/build.py --check    # Konsistenzprüfung
python3 build/build.py --all      # alles
```

oder über das Makefile:

```bash
make html epub pdf anki check
make all
make fonts        # mitgelieferte Schriftschnitte erneuern
make clean        # dist/ und erzeugte CSV-Dateien entfernen
```

`--check` prüft u. a.:

- doppelte Kapitelüberschriften und Sprünge in den Überschriftenebenen,
- unbekannte Kastenarten und fehlende Pflichtbausteine je Kapitel,
- leere Kapitel,
- **Glyphenabdeckung**: jedes Zeichen des Buches muss in den PDF-Schriften
  darstellbar sein — sonst verschwände es stillschweigend im PDF.

Beispielausgabe:

```
CHECK -> Hinweis: 2 Zeichen fehlen in einzelnen Schriften (unkritisch, solange
  sie dort nicht gesetzt werden): serif: ✓✗, serif-bold: ✓✗
CHECK -> 0 Problem(e)
```

---

## Schriften

Das Buch braucht für den PDF-Export Unicode-Schriften: Makronen (`ā ē ī ō ū`),
griechische Buchstaben in den Formenlehre-Tabellen, Rahmenzeichen in den Kästen
und metrische Zeichen. Die eingebauten Schriften von ReportLab decken davon
fast nichts ab.

`build/fonts.py` sucht deshalb in dieser Reihenfolge:

1. **mitgelieferte Schnitte** aus `build/fontfiles/` — zugeschnittene Ableitungen
   von DejaVu, die frei weiterverteilbar sind (Lizenz: Bitstream Vera, siehe
   `build/fontfiles/LICENSE.txt`). Das ist der Normalfall: der Build läuft auf
   jedem System gleich, ohne dass eine Schrift installiert sein muss.
2. **Systemschriften** — DejaVu (Linux, macOS, Windows), danach Times New Roman,
   Arial, Liberation, FreeSerif.
3. **ReportLabs eingebaute Schriften** (Helvetica, Times, Courier) als Notnagel.
   Sie decken weder Makronen noch griechische Buchstaben ab; der Build warnt
   dann und die Glyphenprüfung schlägt an.

Eigene Schriften legt man als `.ttf` unter `build/fontfiles/` ab — sie werden
bevorzugt verwendet. Die Schnitte lassen sich erneuern mit:

```bash
python3 build/make_fonts.py                # sucht DejaVu selbst
python3 build/make_fonts.py /pfad/zu/dejavu
```

---

## Repository-Aufbau

```
latein/
├── book/                    56 Kapitel als Markdown (die Quelle des Buchs)
│   ├── 00-vorwort.md … 53-gesamtpruefung.md
│   └── 54-anhang-loesungen.md   generierter Lösungsband
├── build/
│   ├── build.py             Build-CLI und Konsistenzprüfung
│   ├── md.py                Markdown-Parser (verschachtelte Inline-Auszeichnung)
│   ├── render.py            HTML-, EPUB- und PDF-Renderer
│   ├── fonts.py             portable Schriftenauflösung
│   ├── make_fonts.py        erzeugt die mitgelieferten Schnitte
│   ├── fontfiles/           mitgelieferte Schriftschnitte + Lizenz
│   ├── style.css            Druckstil
│   ├── loesungen/           Werkzeuge der Lösungsmigration (siehe unten)
│   └── anki/                erzeugte Anki-CSV-Dateien
├── glossar/                 vokabeln.tsv/csv (1057 Wörter), begriffe.tsv/csv (194 Begriffe)
├── tools/gen_glossar.py     erzeugt die CSV-Dateien aus den TSV-Quellen
├── dist/                    Build-Artefakte (nicht eingecheckt)
├── Makefile
└── PLAN.md                  Projektplan mit Recherche und Begründungen
```

---

## Der Lösungsanhang ist reproduzierbar

Kapitel 01–53 tragen Aufgaben ohne Lösungen; Anhang V enthält sie. Beides wird
von Werkzeugen erzeugt, die im Repository liegen:

```bash
python3 build/loesungen/strip_answers.py    # Antwortmarker aus den Kapiteln entfernen
python3 build/loesungen/build_anhang.py     # Anhang V neu erzeugen
```

`build/loesungen/stripped.json` hält die entfernten Antworten fest,
`build/loesungen/moved.json` die migrierten Lösungsleiber, und
`build/loesungen/check_answers_*.py` die Musterantworten der Prüfungschecks.

---

## Anki-Import

Vier Stapel in `build/anki/`, je Stapel eine Richtung:

| Datei | Einträge | Richtung |
|---|---|---|
| `latein_de_lat.csv` / `latein_lat_de.csv` | 1057 | Deutsch → Latein / Latein → Deutsch, alle Stufen A–E |
| `latein_kern_de_lat.csv` / `latein_kern_lat_de.csv` | 694 | nur der Kern A–C |

CSV mit Kopfzeile `Front,Back,Tags,Hinweis` — direkt importierbar.

---

## Aufbau des Buchs

| Teil | Kapitel | Inhalt |
|---|---|---|
| Vorwort / Einleitung | 00–01 | Zielgruppe, Lernweg, Widerlegung verbreiteter Mythen |
| Teil I — Die Sprache im Kopf | 02–04 | Aussprache, lateinische Denkweise, Wortbaukasten |
| Teil II — Formenlehre | 05–20 | Deklination, Adjektive, Pronomina, Verb, Tempora, Modi |
| Teil III — Syntax | 21–36 | Wortbildung, Satzglieder, Kasus, Passiv, Infinitiv, Partizip, Konjunktiv, indirekte Rede |
| Teil IV — Die Kunst der Übersetzung | 37–39 | Übersetzungstechnik, Fehlerquellen, Tempusprofil |
| Teil V — Lektüre | 40–49 | zehn Originaltexte mit Wort-für-Wort-Übersetzung |
| Teil VI — Anhänge | 50–55 | Vokabelverzeichnis, Glossar, Formenspiegel, Gesamtprüfung, **Lösungen**, Literatur |

Jedes Kapitel trägt dieselben Bausteine: *Ziel*, *Wortschatz*, *Übung*,
*Wiederholungsfach* und *Prüfungscheck*. Die Gesamtprüfung in Kapitel 53
umfasst 43 Aufgaben in den Teilen A–D (100 Punkte).

---

## Veröffentlichung

Die fertigen Dateien liegen als Release bereit:
**[github.com/AuronOrigin/latein/releases/tag/v1.0.0](https://github.com/AuronOrigin/latein/releases/tag/v1.0.0)**

Jedes Release dieses Repositories enthält alle Ausgabeformate als
downloadbare Dateien:

| Datei | Inhalt |
|---|---|
| `latein.pdf` | das vollständige Buch mit Lesezeichen |
| `latein.epub` | EPUB 3 für E-Reader und Tablets |
| `latein.html` | eine einzelne, in sich geschlossene HTML-Datei |
| `latein_de_lat.csv`, `latein_lat_de.csv` | Anki-Stapel, alle Stufen A–E |
| `latein_kern_de_lat.csv`, `latein_kern_lat_de.csv` | Anki-Stapel, Kern A–C |

Die Artefakte werden bei jedem Tag-Push von GitHub Actions neu gebaut und
automatisch an das Release gehängt. Binärdateien liegen deshalb **nicht** im
Repository — `dist/` und `build/anki/*.csv` sind in `.gitignore` ausgenommen.

Eigenes Release bauen:

```bash
git tag v1.0.1 && git push origin v1.0.1
```

Der Workflow baut PDF, EPUB, HTML und die vier Anki-CSVs und hängt sie an das
Release; der Build bricht ab, wenn die Konsistenzprüfung einen Fehler meldet.

---

## Fehlersuche

| Symptom | Ursache und Abhilfe |
|---|---|
| `PDF -> übersprungen (reportlab nicht installiert)` | `pip install reportlab` |
| `Keine Unicode-Schrift gefunden` | `build/fontfiles/` prüfen (muss sechs `.ttf` enthalten) oder DejaVu installieren |
| Im PDF fehlen Makronen | Die Prüfung `--check` meldet das als Problem; Schriftenpfad prüfen |
| `ModuleNotFoundError: reportlab` | Virtuenv aktivieren oder `pip install --user reportlab` |
| HTML öffnet sich nicht korrekt | Die Datei ist selbstenthalten — im Browser öffnen, nicht im Texteditor |

---

## Lizenz und Quellen

Die mitgelieferten Schriftschnitte stammen von
[DejaVu Fonts](https://dejavu-fonts.github.io/) und stehen unter der
Bitstream-Vera-Lizenz (`build/fontfiles/LICENSE.txt`).

Die Texte der Lektürekapitel folgen den maßgeblichen Ausgaben; Abweichungen
und textkritische Hinweise sind im jeweiligen Kapitel vermerkt. Die
Recherchegrundlage steht in `PLAN.md`, die Quellenliste in dessen Abschnitt 15.
