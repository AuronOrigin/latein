# PLAN — „Latein verstehen“

**Arbeitstitel:** *Latein verstehen — ein modernes Lehrbuch zum Lesen, Übersetzen und Genießen*
**Untertitel (Entwurf):** Formenlehre, Syntax, Wortschatz und Übersetzungstechnik — mit Übungen, Veranschaulichungen und Glossar der Fachbegriffe
**Zielmedium:** Selbstlernbuch (Markdown als Quelle → HTML + EPUB), Zusatznutzung im Schulunterricht (Sachsen/Lehrplan Gymnasium 2019)
**Stand:** Plan v1 — zur Freigabe durch die Leserin / den Leser

---

## 0. Kurzfassung in einem Satz

Ein **deutschsprachiges, ausführlich kommentiertes Latein-Lehrbuch**, das die Sprache *nicht* als Regelwerk, sondern als **Werkzeug zum Lesen** aufbaut: jede Regel wird zuerst am Beispiel gezeigt, dann mit dem deutschen Fachbegriff benannt (Begriffsbox), in Kleinschritten geübt, durch Wortbildungs- und Alltagsbeispiele verankert und am Ende an echten lateinischen Texten geprüft — mit einem ausdrücklichen „Wichtig / Kann warten / Nur für Spezialisten“-System.

---

## 1. Ausgangslage

Das Repository `AuronOrigin/latein` ist leer (nur `README.md`). Es gibt also keine bestehende Struktur, der ich folgen müsste — das Buch wird neu aufgebaut. Die Recherche zeigt, dass es **kein** bestehendes deutschsprachiges Lehrwerk gibt, das alle vier vom Auftrag geforderten Dinge zugleich leistet:

1. eine **systematische Erklärung der Fachbegrifflichkeiten** (Begriffsdefinition *und* Herleitung *und* Nutzen),
2. **Übersetzung ins Deutsche inklusive Wort-für-Wort-Darstellung**,
3. **kleine Übungen** statt nur Drill,
4. **Veranschaulichungen** statt reiner Tabellen.

Genau diese Lücke soll das Buch füllen.

---

## 2. Recherche: Was machen andere Bücher?

### 2.1 Kurzprofile der wichtigsten Vorbilder

| Werk | Grundidee | Was ich übernehme | Was ich **nicht** übernehme |
|---|---|---|---|
| **Wheelock / „Learn to Read Latin“ (Keller & Russell)** [2](https://bmcr.brynmawr.edu/2005/2005.01.21/) | Morphologie zuerst, Syntax danach; Vokabeln kapitelweise; viele Originaltexte | Kapitel-Vokabular am Kapitelanfang, „Short Readings“ (Kurztexte) mit Vokabelhilfen, Übungsdrills | 15 Kapitel in 5 Jahren; Morphologie wird zum Selbstzweck; schwerfällige Drill-Struktur |
| **Ørberg, „Lingua Latina per se illustrata“** [6](https://en.wikipedia.org/wiki/Hans_%C3%98rberg) | **Induktiv**: erst Beispiele, dann Begriff; Illustrationen; „Grammatica Latina“-Abschnitt nach jeder Lektion; „Pensa“ | **Methode „erst das Muster, dann der Name“**; Marginalien; Kapitelende-Syntaxblock; Übungsabschnitt | Lehrbuch komplett auf Latein (für deutsche Leser: zu hohe Hürde); keine deutsche Erklärung der Fachbegriffe |
| **Cambridge Latin Course (4./6. Aufl.)** [1](https://cambridgelatin.org/wp-content/uploads/2015/09/Scope-and-Sequence-4th-Ed.pdf) | Durchgehende Erzählgeschichte (Caecilius, Pompeji); induktive Grammatik; **horizontale Präsentation** mehrerer Deklinationen/Konjugationen nebeneinander; Stages mit Vokabel-Checklisten; Kulturseiten | **Spiralförmiger Aufbau**, „Stage“-Lektionen mit Vokabel-Checkliste, gleichzeitige Einführung mehrerer Formen | Sehr englisch/großbritannisch geprägt; keine deutsche Fachterminologie; Cultural content stark an England gekoppelt |
| **Didaktik der deutschen Lehrpläne** (Sachsen 2019 [1](https://cms.sachsen.schule/fileadmin/_special/gruppen/90/pdf-dateien/faecher/Latein/2407_lp_gy_latein_2019.pdf), Bayern [3](https://www.lehrplanplus.bayern.de/sixcms/media.php/71/Grundkenntnisse_Latein.pdf), Hessen [5](https://kultus.hessen.de/sites/kultus.hessen.de/files/2021-06/g9-latein.pdf)) | Modularisierung, Kompetenzorientierung, **„Multivalenz“** (Sprache + Literatur + Kultur + Staat/Gesellschaft), Wegfall der Hinübersetzung, aktives Sprechen | Modularer Kapitelaufbau, Lernbereich „Wortkunde/Lexik/Syntax/Morphologie“, Ausrichtung an Lateinums-Kompetenzen | Nüchterne Bildungsplan-Sprache; für Selbstlerner zu trocken |
| **Lehrbuchgenerationen der letzten 20 Jahre** [9](https://doczz.net/doc/5699287/handout) | 4. Generation: „neuer Schüler im Mittelpunkt“, **horizontale Präsentation**, Formenlehre + Syntax verknüpft, **Visualisierung**, aktives Sprechen, eigenständige Übungsformen | Methodische Checkliste als Qualitätsmaßstab für mein Buch | Schulbuch-Didaktik mit festen Lehrer-/Klassenbezug |
| **Duden / „Lateinische Grammatik kompakt“ (Senecio)** [5](https://www.buerche.de/book/9793504040639) | Kompakte Nachschlage-Grammatik, Schwerpunkt auf den Latinums-Prüfungsstoff | „Prüfungsrelevanz“ als Auswahlkriterium (Fokus auf AcI, NcI, PC, Abl. abs., Gerundium/Gerundiv) [3](https://www.amazon.de/Lateinische-Grammatik-kompakt-Schnell-Latinum/dp/3844812911) | Keine systematische Erklärung, kein Vokabelaufbau, keine Lektüre |
| **„Latein kompakt“ (Stark), „Artes. Latein-Grammatik kompakt“** [4](https://www.stark-verlag.de/latein-kompakt-kurzgrammatik-9783849037871) | Übersichtstabellen, Merksprüche, Lernvideos, Schritt-für-Schritt-Anleitungen zum Übersetzen | **Schritt-für-Schritt-Übersetzungsanleitung**, Merksprüche, Videohinweis | rein kompendialisch, keine Grundlegung |
| **Haptik / Wortkunde: Vokabel-Frequenzlisten** (Dickinson DCC Core Vocabulary [8](https://dcc.dickinson.edu/vocab/core-vocabulary); Diederich 1939 [4](https://www.scribd.com/document/418233810/Diederich-Main); Williams, *Essential Latin Vocabulary* [9](https://www.readingroads.com/product/essential-latin-vocabulary-the-1-425-most-common-words-occurring-in-the-actual-writings-of-over-200-latin-authors53392/)) | 1.000 Wörter ≈ 70 % des Textes; 1.425–1.471 Wörter ≈ 84–95 %; ca. 250 Wörter = 50 % | **Frequenzbasiertes Kernvokabular** als rotes Garn, „Fundament“ (Top 200) / „Grundwortschatz“ / „Erweiterung“ | Auswendiglernen langer Listen ohne Kontext |
| **Lernforschung** (Ebbinghaus; Cepeda et al. 2006; Dunlosky et al. 2013; Kim & Webb 2022 [10](https://www.researchgate.net/publication/358406370_The_Effects_of_Spaced_Practice_on_Second_Language_Learning_A_Meta-Analysis)) | **Spaced Repetition** + **aktives Abrufen** schlagen Massed Practice deutlich; Vokabeln profitieren am stärksten | 12-Wochen-Lernplan, tägliche 10–15-Minuten-Einheit, Abrufpraxis, Anki-CSV, „Wiederholungsfächer“ am Kapitelende | — |
| **Neue Lehrwerke/Wikibooks, Apps (lernapps „Deklinationsbaukasten“)** [10](https://github.com/lernapps/apps/issues/529) | **Baukasten-Metapher**: Stamm = fester Stein, Endung = austauschbarer Stein; „Drehräder“ Kasus/Numerus/Genus | Diese Metapher wird zum roten Faden der Veranschaulichungen | — |

### 2.2 Was daraus folgt (die 7 Leitentscheidungen)

1. **Induktion vor Definition** (Ørberg + CLC): Erst 10 Beispiele, dann der Fachbegriff — aber *sofort* mit Erklärung, Herleitung und „Wozu brauche ich das?“. So bleibt der Begriffsschatz der Schul-/Prüfungssprache erhalten, ohne dass das Buch zur Wörterbuchlese wird.
2. **Spiralaufbau statt Einmal-Einführung**: Deklinationen werden nicht nacheinander „abgearbeitet“, sondern in Wellen (1. + 2. Deklination → 3. Deklination → 4./5.) mit wiederkehrenden „Baustellen“-Rückblicken. (Horizontalprägung der modernen Lehrbuchgeneration, [9](https://doczz.net/doc/5699287/handout).)
3. **Deutsch ist die Zielsprache, aber Latein bleibt die Denksprache**: Wort-für-Wort-Übersetzung und sinngemäße Übersetzung stehen immer nebeneinander; Fehler der literalen Fassung werden markiert („So sagt man nicht — warum?“).
4. **Auswahl nach Prüfungs- und Leserelevanz**: Die 2. Deklination und die 1./2. Konjugation bekommen 3× so viel Platz wie die 5. Deklination. Alles, was selten ist, wird als „Rarität“ gekennzeichnet, nicht weggelassen (Nachschlagewert bleibt).
5. **Frequenzbasierter Wortschatz**: Kernvokabular nach Frequenzstufen, nicht alphabetisch; Wortfamilien statt Einzellernwörter (Präfix/Suffix-Kapitel).
6. **Didaktische Maschen**: Jedes Kapitel endet mit „Wiederholungsfach“ (retrieval, nicht Wiederholung), „Mikroübung“ (30 Sekunden), „Stolperfallen“ und „Prüfungscheck“.
7. **Veranschaulichung als eigenes Kapitelprinzip**: „Kasus-Drehscheibe“, „Stamm-Endungs-Werkbank“, Satzdiagramme, Text-Baupläne — als ASCII/Mermaid-Diagramme im Markdown (im HTML farbig, mit Druckstil).

---

## 3. Was ist wichtig — und was nicht?

Diese Tabelle wird im Buch **mehrmals** auftauchen (pro Kapitel als Kurzmarke, im Anhang als Gesamtübersicht). Sie ist die direkte Antwort auf die Aufgabenstellung „was ist wichtig, was nicht“.

| Stufe | Inhalt | Begründung |
|---|---|---|
| **A — Muss** | 1./2. Deklination, 3. Deklination (kernig), 1./2. Konjugation, Präsens/Imperfekt/Perfekt (+Plusquamperfekt), Indikativ, Aktiv/Passiv, Akkusativ-/Dativ-/Genitiv-/Ablativgebrauch, Adjektivdeckung, Infinitiv, AcI, Konjunktiv (Grundfunktionen), Subjunktiv (Hauptsatz), Pronomina, Präpositionen mit Akk./Abl., Stammformen der Top-30-Verben | deckt ca. 95 % aller Texte ab; Kern des Latinums |
| **B — Soll** | 4./5. Deklination, 3. Deklination (voll), 3./4./5. Konjugation, Futur, Futur II, Gerundium/Gerundiv, Participium coniunctum, Abl. absolutus, NcI, indirekte Rede, ut-/cum-/quod-Sätze, Komparation, Zahlwörter | nötig für Originallektüre und Abitur |
| **C — Kann warten** | Deponentien im Detail, unregelmäßige Formen (fio/fieri, fero), Ausnahmen der 3. Deklination, Adjektive aus 3. Deklination, Comparativus/Superlativus-Sonderformen, Pronomen-/Adverb-Sonderformen | tritt selten auf, nachschlagbar |
| **D — Rarität / Spezialist** | Poetik/Metrik (Hexameter, Daktyl), Prosodie, Oratio obliqua-Periphrase, Gerundiv als Passiv-Periphrase (selten), archaische und mittellateinische Sonderformen, mittellateinige Schreibweisen | nur fürs Abitur/Studium/Philologie; im Buch als kompakter „Briefkasten“-Abschnitt |
| **E — Bewusst weggelassen** | vollständige antike Aussprache-Rekonstruktion (nur Prinzipien), Theater-Vokabular, Ptolemäische Geographie, moderne Pseudolateinismen | kein Nutzen für das Lesen klassischer Texte |

> Das Buch sagt an jeder Stelle **explizit**, in welcher Stufe (A–E) ein Thema steht — das ist der ehrlichste Weg, „was nicht wichtig ist“ sichtbar zu machen.

---

## 4. Zielgruppe, Umfang, Lernpfad

* **Zielgruppe A:** Lernende ohne Vorkenntnisse (Schüler:innen Kl. 8 ff. bzw. ab Kl. 5 als 2./3. Fremdsprache; Erwachsene im Selbststudium).
* **Zielgruppe B:** „Wiedereinsteiger“ mit Schul-Latein, die die Grammatik *wirklich* verstehen wollen.
* **Umfang:** ca. **38 Kapitel**, rund **200–260 Seiten** Fließtext, **~700 Einzelsätze/Beispiele**, **~500–700 Übungsaufgaben** (davon ~60 % mit Musterlösung direkt im Kapitel), **~130 Fachbegriffe** im Glossar, **~600 Kernvokabeln** in fünf Frequenzstufen.
* **Lernpfad:** 12-Wochen-Plan (30–45 Min./Tag) als umsetzbarer Fahrplan + 6-Monats-Plan als Langzeitvariante.
* **Zusatznutzen:** Der Stoff deckt sich bewusst mit dem sächsischen Lehrplan (Spracherwerbsphase Kl. 8–10, Lektürephase) [1](https://cms.sachsen.schule/fileadmin/_special/gruppen/90/pdf-dateien/faecher/Latein/2407_lp_gy_latein_2019.pdf) und mit dem Latinum (Bund: 12 Lektionen Prüfungsvorbereitung) — jedes Kapitel endet mit einem „Prüfungscheck“-Kasten.

---

## 5. Vollständige Gliederung (Endstand)

```
VORWORT
  0  Für wen dieses Buch ist · wie man es liest · Lernplan (12 Wochen) · Karte des Buches
  1  Warum Latein? Nutzen, Mythen, Erwartungsmanagement

TEIL I — DIE SPRACHE IM KOPF (Einführung)
  2  Wie Latein klingt: Aussprache, Betonung, Silben, Schrift (Übungen: Vorlesen)
  3  Wie Latein denkt: Subjekt-Objekt-Verb statt Verb-Subjekt-Objekt; Merksatz „Akkusativ ist der Lieblingsfall“
  4  Der Baukasten: Stamm + Endung, Wortarten-Überblick, die acht Bausteine eines Satzes
  5  Das Skelett: der einfache lateinische Satz (Satzmodell, erste Sätze, erste 30 Wörter)

TEIL II — FORMENLEHRE (Morphologie)
  6  Nomen I: 1. Deklination (a-Deklination) + Genusregeln
  7  Nomen II: 2. Deklination (o-Deklination) + Genusregeln
  8  Adjektiv I: a-/o-Deklination, Adjektivdeckung, Adjektiv als Nomen
  9  Verb I: Präsensstamm, 1. Konjugation, Stammformen
 10  Verb II: 2. + 3. + 4. + Mischkonjugation im Vergleich (horizontale Präsentation)
 11  Verb III: irregulares sum/esse, posse, ferre, fieri, ire
 12  Pronomen: Personal-, Possessiv-, Demonstrativ-, Relativ-, Interrogativ-, Indefinitpronomen
 13  Nomen III: 3. Deklination (Konsonantisch/i) + die wichtigsten Ausnahmen
 14  Adjektiv II: Adjektive der 3. Deklination
 15  Nomen IV: 4. + 5. Deklination (u-/e-Deklination), Sonderformen (domus, finis …)
 16  Adverb, Konjunktion, Präposition, Interjektion, Zahlwörter
 17  Tempora I: Präsens, Imperfekt, Perfekt, Plusquamperfekt (Aktiv + Passiv)
 18  Tempora II: Futur I/II, periphrastische Ausdrücke
 19  Modi I: Indikativ, Imperativ, Infinitiv
 20  Modi II: Konjunktiv (Aktiv/Passiv, alle Tempora), Subjunktiv
 21  Wortbildung: Präfixe, Suffixe, Komposita, Wortfamilien (Brücke zum Vokabular)

TEIL III — SYNTAX (Satzlehre)
 22  Satzglieder: Subjekt, Prädikat, Objekt, Adverbialia
 23  Genitiv: Besitz, Abhängigkeit, Definition, Vergleich
 24  Akkusativ: Objekt, Adressat, Ausdehnung (Ort wohin), Betonung
 25  Dativ: indirektes Objekt, possessorisch, Interessen, doppelter Dativ
 26  Ablativ: Mittel, Ursache, Trennung, Herkunft, Ort wo, Vergleich, Subjekt beim Passiv
 27  Locativ, „in + Akk./Abl.“, Adverbien als Kasusformer
 28  Passiv, Deponentien, unpersönliches Passiv
 29  Infinitiv-System: Infinitiv als Objekt/Subjekt, AcI, NcI, AcP, PC, Infinitiv mit Auslassungen
 30  Gerundium und Gerundivum (incl. „Pflicht, zu …“)
 31  Participium coniunctum, Ablativus absolutus, Partizipialadjektive
 32  Pronomen-Sätze: Relativsätze (mit Attribut vs. Objekt), Demonstrativpronomen als Subjekt
 33  Konjunktionalsätze: ut, ne, cum, quod, quoniam, quamquam, dum, postquam, antequam
 34  Indirekte Rede: NcI, Konjunktiv, obliqua, Konjunktiv im Hauptsatz (hortativ, optativ, potential, jussiv, prohibitiv)
 35  Conditionalis: vier Arten, Konjunktiv im Hauptsatz
 36  Ellipse, Auslassungen, Auslassung des Subjekts, Unterscheidung Präposition/Adverb

TEIL IV — DIE KUNST DER ÜBERSETZUNG
 37  Übersetzungswerkzeug: Fragebaum, Gradatim, Einrücken, Satzanalyse in 7 Schritten
 38  Fehlerquellen und ihre Behebung (Kasus-Sünden, Tempus-Sünden, Subjekt-Sünden …)
 39  Tempusprofil & Modalität: „Was weiß der Erzähler?“

TEIL V — LEKTÜRE (10 Texte, je ein Kapitel)
 40  Lektüre I   Ein Tag in Rom — erfundener Alltagsdialog in der Taberna (Wortschatz, Münzen, Maße)
 41  Lektüre II  Phaedrus, Fabulae I.1 — Lupus et agnus (Senarien, Pointe, Redewendungen)
 42  Lektüre III Cicero, Tusculanae disputationes I.9–11 (Sprecherwechsel, Argumentationsanalyse)
 43  Lektüre IV  Seneca, Epistulae morales I — Briefschema, Sentenzen, Nominalstil
 44  Lektüre V   Caesar, De bello Gallico I.1–2 (historisches Präsens, Passiv, Parallelismus)
 45  Lektüre VI  Livius, Ab urbe condita I.1–8 (Quellenvarianten, AcI, Zeitfolge)
 46  Lektüre VII Ovid, Metamorphosen I.1–5 und I.89–95 (Hexameter, Goldenes Zeitalter)
 47  Lektüre VIII Vergil, Aeneis I.1–11 (Hyperbaton, Enallage, epischer Prolog)
 48  Lektüre IX  Die Vulgata: Psalmus 22/23 (Bibelübersetzungs-Latein, Gleichnisse)
 49  Lektüre X   Die Brücke: Beda (Mittellatein) und Erasmus (Neulatein)

TEIL VI — ANHÄNGE
 50  Anhang I   Vokabelverzeichnis: 893 Kernvokabeln in fünf Stufen (A–E)
 51  Anhang II  Glossar der Fachbegriffe: 182 Begriffe mit Herkunft und Kapitelverweis
 52  Anhang III Formenspiegel: Deklinationen, Steigerung, Pronomina, Konjugation, Tempus/Modus
 53  Anhang IV  Gesamtprüfung: 43 Aufgaben aus allen Teilen (100 Punkte)
 54  Anhang V   Lösungen zu allen Übungen: Übungsblöcke, Wiederholungsfächer,
                Prüfungschecks und der Lösungsband zur Gesamtprüfung

*(Endstand: 55 Kapitel in `book/00-…` bis `book/54-…`. Die Lektüre wurde gegenüber dem Entwurf von „12 Texte" auf **zehn** konkretisierte Texte in **je einem eigenen Kapitel** umgesetzt; Vokabel-Lernsystem, Wortbildungs-Übungen, Literaturverzeichnis und 12-Wochen-Plan sind in die Anhänge 50–54 sowie das Vorwort integriert. Die Lösungen stehen
nicht beim Aufgabentext, sondern gesammelt in Anhang V — so dient das Buch zugleich als
Arbeitsheft und als Lösungsbuch.)*

### 6a. Der Lösungs-Werkzeugbau (`build/loesungen/`)

Damit Anhang V jederzeit **reproduzierbar** bleibt, liegen Generator und Daten
im Repository statt in `/tmp`:

| Datei | Inhalt |
|---|---|
| `moved.json` | die 122 aus den Kapiteln migrierten Lösungen (Übungsblöcke, Wiederholungsfächer, Mikroübungen, Check-Lösungen der Kapitel 02–10) |
| `stripped.json` | die 123 beim Bereinigen der Kapitel entfernten Inline-Antworten (Prüfungscheck-Aufgaben 1 und 2) |
| `check_answers_a/b/c.py` | die fachlichen Musterantworten auf die offenen Prüfungscheck-Fragen der Kapitel 01 und 11–53 |
| `teil_e_block.md` | der Lösungsband zur Gesamtprüfung (Teil E) |
| `strip_answers.py` | entfernt die Antwortmarker aus den Kapiteldateien (`--check` = Probelauf) |
| `build_anhang.py` | erzeugt `book/54-anhang-loesungen.md` aus allen Quellen |

Ablauf: `python3 build/loesungen/strip_answers.py` → `python3 build/loesungen/build_anhang.py` → `python3 build/build.py --all`.
Ergebnis: **171 Lösungskästen** (53 Übungsblöcke, 53 Wiederholungsfächer, 54 Prüfungschecks, 6 Mikroübungen, 1 Wort-für-Wort-Übersetzung, 4 Gesamtprüfungsteile, 2 anhangseigene) — **jede** Bausteinaufgabe aller 53 Kapitel hat genau eine Lösung.

---

## 6. Feste Bausteine jedes Kapitels (Layoutvertrag)

Jedes Kapitel folgt demselben Muster — das macht das Buch scanbar und „lehrbar“:

1. **Lernziele** (3–5 Punkte, „Du kannst danach …“)
2. **Wortschatz** (10–15 Wörter mit Stamm, Aussprache, Beispiel)
3. **Der Stoff** — Erklärung in klarer Deutschsprache, max. 2–3 Sätze pro Regelabschnitt
4. **Begriffsbox** — der Fachbegriff: Definition · Herleitung (Etymologie) · Beispiel · „Wozu?“ · Verweiskasten (verwandte Begriffe)
5. **Veranschaulichung** — mindestens 1 Diagramm/Schema je Kapitel (Kasus-Drehscheibe, Werkbank, Satzbaum, Tabelle, Zeitleiste)
6. **Stolperfallen** (typische Fehler, 2–4 pro Kapitel)
7. **Mikroübungen** (2–3 Aufgaben, 30 Sekunden, sofort lösbar)
8. **Übungsblock** (10–20 Aufgaben: Formenbildung, Übersetzung, Vokabel, Analyse)
9. **Wiederholungsfach** (Abrufpraxis: Formen, Vokabel, Regeln — ohne Hinsehen lösbar)
10. **Prüfungscheck** (3 Aufgaben im Latinum-/Klausurformat)
11. **Quelle/Vertiefung** (2–3 Literaturempfehlungen)

---

## 7. Terminologie-Strategie (Kernauftrag „Beschreibung der Begrifflichkeiten“)

* Jeder Fachbegriff wird **an der Stelle eingeführt, an dem er gebraucht wird**, in einer gleich aufgebauten **Begriffsbox**:
  `Begriff (latin. / griech. Herkunft) → Definition in 1–2 Sätzen → Beispiel → „Wozu brauche ich das?“ → verwandte Begriffe`.
* Ein zusätzliches **Glossar (Teil VII)** sortiert alle ~130 Begriffe alphabetisch und erläutert sie kompakt mit Verweis auf die Kapitelnummer.
* Fachbegriffe erhalten durchgehend **deutsche Klartext-Gegenüberstellung** („Akkusativ = ‚Worauf zeigt der Pfeil?‘“), damit der Begriff *hängen bleibt*.
* Ein eigener Abschnitt behandigt **Etymologie als Lernhilfe**: *agricultura* = *ager* (Feld) + *-cultūra* (Pflege); *ordo, ordinis* → Ordination; *firmus* → Firma; *vulnus* → vulnerarisch.
* Nicht-lateinische Fachbegriffe (z. B. „Diathese“, „Allomorph“, „Diachronie“) werden erklärt, aber als **Werkzeug**, nicht als Selbstzweck.

---

## 8. Übungs- und Visualisierungskonzept

**Übungsarten (rotierend, immer mit variierender Anforderung):**
Formenbildung · Deklinationsanalyse (Form → Funktion) · Übersetzung DE→LAT · Übersetzung LAT→DE (Wort-für-Wort + sinngemäß) · Satzbau · Vokabelzuordnung · Wortbildung · Lückentext · Fehlerkorrektur („Was ist falsch?“) · Tempusprofil · Übersetzungs-Fehlernanalyse (Übersetzung prüfen und verbessern) · Zuordnungsaufgabe lateinisch↔deutsch (Gegensinn, Antonym) · kurze Multiple-Choice-Tests.

**Übungsumfang:** ~500–700 Aufgaben, davon 60 % direkt im Kapitel mit Musterlösung, 40 % als „Übungsdepot“ mit Lösungen in Teil VII.

**Veranschaulichungen:**
* ASCII-/Unicode-Diagramme (druckbar, GitHub-tauglich) — z. B. „Kasus-Drehscheibe“ (Numerus × Genus × Kasus), „Endungs-Baukasten“ (Stamm + Endung), „Satz-Bauplan mit Pfeilen“, „Konjugationsrad“.
* **Mermaid-Diagramme** für Abläufe (z. B. „so gewinnt man eine Form“).
* **HTML-Ausgabe mit Syntax-Hervorhebung** (Subjekt grün, Verb blau, Objekte rot) — die „farbige Satzanalyse“, wie sie an Schulwänden hängt.
* Optional: **AI-generierte Illustrationen** (Forumsszene, Drehscheibe als Poster, Römerkind im Garten) — *nur nach Freigabe* (siehe Frage 5).
* Alle Bilder werden als **SVG/PNG mit Quellenangabe** eingebunden, damit das Buch auch offline als EPUB funktioniert.

---

## 9. Wortschatz-Strategie

| Stufe | Umfang | Abdeckung klassischer Texte | Quelle |
|---|---|---|---|
| Fundament (Top 100–200) | ~150 Wörter | ~40–50 % | [8](https://dcc.dickinson.edu/vocab/core-vocabulary) |
| Grundwortschatz (Top 500) | ~500 Wörter | ~65–70 % | Dickinson DCC |
| Lesewortschatz (Top 1.000) | ~1.000 Wörter | ~70 % der Wortformen | [8](https://dcc.dickinson.edu/vocab/core-vocabulary) |
| Ergänzung (Top 1.500) | ~1.500 Wörter | ~84–95 % | Diederich 1939 [4](https://www.scribd.com/document/418233810/Diederich-Main) |
| Plus 100 Mittellatein | 100 | öffnet 1.000 Jahre Literatur | Williams [9](https://www.readingroads.com/product/essential-latin-vocabulary-the-1-425-most-common-words-occurring-in-the-actual-writings-of-over-200-latin-authors53392/) |

Das Buch liefert: **~600 Vokabeln im Kernteil** (Fundament + Grundwortschatz + ausgewählte Lesewortschatz-Wörter), jeweils mit **Zahlform**, **Stammherkunft**, **dt. Übersetzung**, **Beispielsatz**, **Wortfamilie**; plus **Anki-CSV** (Deutsch→Latein und Latein→Deutsch, getrennt) und ein **Selbsttest** mit 25 Wörtern.

---

## 10. Lektüre-Plan (Teil V)

Alle Texte sind **gemeinfrei** (antike Autoren bzw. Public Domain). Auswahl:

| Stufe | Text | Zweck |
|---|---|---|
| 1 | Eigene Mini-Geschichten (römischer Alltag: Haus, Schule, Markt) | Gefühl für Wortstellung & Rhythmus |
| 2 | Phaedrus, Aesop-Fabeln (lat. Adaptation) | kurze, pointierte Sätze, viele Redewendungen |
| 3 | Cicero, *De amicitia* / *Tusculanae* (Auszug) | Prosa, philosophisch, viele Zitate |
| 3 | Seneca, *Epistulae* 1 & 7 | kurze, direkte Prosa |
| 3 | Caesar, *De bello Gallico* 1 | klassischer Schultext |
| 3 | Livius, *Ab urbe condita* 1 (Auszug) | Gründungsmythos |
| 4 | Ovid, *Metamorphosen* 1 (Prose-Epitome) | Mythenstoff |
| 4 | Hieronymus, *Vulgata* Ps 23 / Sprüche 31 |bibelübergreifend |
| 4 | Beda, *Historia ecclesiastica* (Auszug) | Mittellatein-Brücke |
| 4 | Erasmus, *De remediis utriusque fortunae* (Auszug) | Neulatein-Brücke |

Jeder Text bekommt dasselbe Paket: **Vokabelhilfe vor dem Text** (Randglossen) → **Wort-für-Wort-Übersetzung** (mit Zeilennummern) → **sinngemäße Übersetzung** → **Satzdiagramm** → **Kulturbox** → **5 Verständnisfragen** → **eine Stilfrage**.

---

## 11. Technik, Repo-Struktur, Ausgabeformate

```
latein/
├── README.md                 (Einstieg, Inhaltsverzeichnis, Nutzungsanleitung)
├── PLAN.md                   (dieser Plan)
├── QUELLEN.md                (Rechercheprotokoll mit allen Quellen/URLs)
├── book/                     (Buchquellen, Markdown)
│   ├── 00-vorwort.md … 48-literatur.md
│   ├── part-1/ … part-7/    (Kapitel nach Teil, für sinnvolle Dateigrößen)
│   └── assets/               (SVG/PNG-Illustrationen, Mermaid-Quellen)
├── glossar/
│   ├── begriffe.csv          (Begriff | Definition | Herleitung | Kapitel | Beispiel)
│   └── vokabeln.csv          (Lemma | dt. | Stamm | Frequenzstufe | Wortfamilie)
├── build/
│   ├── build.py              (Markdown → HTML + EPUB, ohne externe Abhängigkeiten)
│   ├── style.css             (Druckstil, Syntax-Hervorhebung)
│   └── anki/                 (CSV → Anki-Import, Text ↔ Text-Dateien)
├── dist/                     (latein.epub, latein.html — Build-Artefakte, gitignoriert)
└── Makefile                  (make build / make check)
```

**Ausgabeformate:** Markdown (Quelle) → **HTML** (self-contained, druckbar, mit Syntaxfarben) → **EPUB 3** (für E-Reader/Tablet; reines Python, ohne Fremdpakete). Optional PDF, falls im Sandbox-System ein Renderer verfügbar wird (Prüfung in Umsetzungsphase).

---

## 12. Qualitätssicherung

1. **Fachlicher Durchgang:** Alle lateinischen Beispiele, Endungen, Paradigmen und Übersetzungen werden gegen Standardwerke geprüft (Allen & Greenough, Menge/Harold, Ørberg, DCC-Liste).
2. **Konsistenz-Check-Skript** (`build/check.py`): prüft Endungs-Arrays in den Paradigmen-Tabellen, sucht unmarkierte Makronen, doppelte Kapitelnummern, tote Querverweise.
3. **Übungs-Plausibilität:** Jede Musterlösung wird mindestens einmal nachgerechnet (maschinelle Formenprüfung bei Deklination/Konjugation).
4. **Einheitliche Makronen:** Längenvokale durchgehend mit Makron (wie in Schulbüchern), Ausnahmen in einem Kasten „Womit die Schulbücher sich unterscheiden“.
5. **Vokabelabgleich:** Alle im Buch verwendeten Vokabeln werden gegen `glossar/vokabeln.csv` geprüft (keine unbelegten Wörter).
6. **Rechtschreib-/Größencheck** für Deutsch und Latein.

---

## 13. Umsetzung: Meilensteine

| Meilenstein | Inhalt | Umfang |
|---|---|---|
| **M1 — Gerüst + Muster** | Repo-Struktur, Layoutvertrag, Build-Skript (HTML/EPUB), 3 Musterkapitel (Teil I) | ~2 Tage |
| **M2 — Teil I + II** | Kapitel 2–21 (Einführung, Formenlehre) | Hauptarbeit |
| **M3 — Teil III** | Kapitel 22–36 (Syntax) | Hauptarbeit |
| **M4 — Teil IV + V** | Übersetzungstechnik + 10 Lektüren mit Vollpaket | Hauptarbeit |
| **M5 — Teil VI + VII + Anhang** | Vokabel, Glossar, Lösungen, Literatur | mittel |
| **M6 — Finishing** | QA-Durchgang, Korrektur, Build, Illustrationen, Tagging, Release auf dem Branch | mittel |

Die Arbeit wird **kapitelweise** auf dem Branch `arena/e29c38ef-latein` committet, damit Fortschritt jederzeit sichtbar und rückgängig machbar ist. Nach jedem Meilenstein gibt es einen Zwischenstand zum Review.

---

## 14. Offene Entscheidungen (bitte entscheiden)

1. **Zielniveau / Fassung:** Ein Buch für **Null-Vorkenntnisse bis Latinum** (Schul- + Selbstlern-tauglich, ~200–260 Seiten) — oder ein **vertiefendes Kompendium** für Wiedereinsteiger (Fokus Grammatik/Syntax, ~150 Seiten)? *Empfehlung: die große Fassung, weil sie beide Gruppen bedient.*
2. **Schulbezug:** Soll der Schulbezug (Lateinum, sächsischer Lehrplan, Prüfungsformate) **explizit im Text** stehen (Lernzielcheck, Prüfungscheck) oder **nur als Beiwerk**? *Empfehlung: explizit, aber in separaten Kästen, damit das Buch auch außerhalb der Schule trägt.*
3. **Umfang/Stilisierung:** Sollen ** KI-generierte Illustrationen** (Römerwelten-Bilder, Poster-Diagramme) das Buch versehen, oder bleibt es rein typografisch (ASCII/Mermaid/HTML)? *Kosten: Zeit + Lizenzfragen (eigene Bilder = frei verwendbar).*
4. **Ausgabeformate:** HTML + EPUB genügen, oder ist **PDF/Papier** (Druck) wichtig? *(PDF nur mit zusätzlichem Renderer möglich.)*
5. **Lektüreumfang:** 10 (kompakt) oder 14 Texte inkl. Mittel-/Neulatein-Brücke?

---

## 15. Quellen der Recherche (Auszug)

- Wheelock/Learn to Read Latin — Rezension BMCR [2](https://bmcr.brynmawr.edu/2005/2005.01.21/), Inhaltsverzeichnis 2. Aufl. [2](https://dokumen.pub/learn-to-read-latin-second-edition-textbook-2nbsped-0300194943-9780300194944.html)
- Ørberg, *Lingua Latina* — Wikipedia/Hackett [6](https://en.wikipedia.org/wiki/Hans_%C3%98rberg) [4](https://hackettpublishing.com/lingua-latina-per-se-illustrata-series), Rezension BMCR [1](https://bmcr.brynmawr.edu/2017/2017.09.16/)
- Cambridge Latin Course — Scope & Sequence [1](https://cambridgelatin.org/wp-content/uploads/2015/09/Scope-and-Sequence-4th-Ed.pdf), Pädagogik [3](https://everyhomeschool.com/directory/publishers/cambridge-latin-course)
- Lehrplan Gymnasium Latein, Sachsen [1](https://cms.sachsen.schule/fileadmin/_special/gruppen/90/pdf-dateien/faecher/Latein/2407_lp_gy_latein_2019.pdf); Lehrplanplus Bayern, Grundkenntnisse [3](https://www.lehrplanplus.bayern.de/sixcms/media.php/71/Grundkenntnisse_Latein.pdf); Hessen [5](https://kultus.hessen.de/sites/kultus.hessen.de/files/2021-06/g9-latein.pdf); Sachsen-Anhalt [10](https://lisa.sachsen-anhalt.de/fileadmin/Bibliothek/Politik_und_Verwaltung/MK/LISA/Unterricht/Lehrplaene/Gym/Anpassung_2022/FLP_Lat_Gym_01082022_sw.pdf)
- Lehrbuchgenerationen/Handout [9](https://doczz.net/doc/5699287/handout); Handreichung Latein IV (RLP) [3](https://bildung.rlp.de/fileadmin/user_upload/rfb.bildung.rlp.de/Sprachen/Latein/Handreichung_Latein_IV.pdf)
- Vokabelfrequenz: Dickinson DCC Core Vocabulary [8](https://dcc.dickinson.edu/vocab/core-vocabulary); Diederich, *Frequency of Latin Words and Endings* [4](https://www.scribd.com/document/418233810/Diederich-Main); Hudson, *Latin Frequency Dictionary* [2](https://archive.org/stream/LatinGrammarForTheReadingScanlonA.M.CoraCarrollS5879/Latin%20Frequency%20Dictionary_%20Th%20-%20Hudson,%20Paul_5051_djvu.txt); Williams, *Essential Latin Vocabulary* [9](https://www.readingroads.com/product/essential-latin-vocabulary-the-1-425-most-common-words-occurring-in-the-actual-writings-of-over-200-latin-authors53392/)
- Lernforschung: Cepeda et al. 2006 (Meta-Analyse), Dunlosky et al. 2013, Kim & Webb 2022 [10](https://www.researchgate.net/publication/358406370_The_Effects_of_Spaced_Practice_on_Second_Language_Learning_A_Meta-Analysis)
- Deutschsprachige Referenzen: „Lateinische Grammatik kompakt“ (Senecio) [5](https://www.buerche.de/book/9793504040639), „Latein kompakt“ (Stark) [4](https://www.stark-verlag.de/latein-kompakt-kurzgrammatik-9783849037871), „Artes. Latein-Grammatik kompakt“ [4](https://www.hpt.at/verlagsprogramm/schulbuecher/artes-latein-grammatik-kompakt), Schulbuch „latein“ (HPT) [1](https://lp.hpt.at/LP_24512.pdf), Wikibooks Anfängerkurs [8](https://de.wikibooks.org/wiki/Latein/_Anf%C3%A4ngerkurs/_Lektionen), „Deklinationsbaukasten“ (lernapps) [10](https://github.com/lernapps/apps/issues/529)
