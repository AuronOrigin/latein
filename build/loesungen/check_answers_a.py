# -*- coding: utf-8 -*-
"""Fachliche Musterantworten auf die offenen Prüfungscheck-Fragen.

Kapitel 01 sowie 11 bis 53.  Je Kapitel ein dict: Nummer -> Antworttext.
Nummer 1 und 2 sind Form- bzw. Übersetzungsaufgaben (Antwort steht bereits
inline im Kapitel); Nummer 3 ist in der Regel die Erklärfrage.

Dieses Modul ist die Datenquelle für ``build/build_anhang.py``.
"""

CHECK_ANSWERS = {

# ---------------------------------------------------------------- Kapitel 01
"1": {
 "1": "Musterantwort: Latein ist gut für **genaues Denken in klaren Strukturen** — es zwingt zu Form, Funktion und Bedeutung, es schärft die Argumentation und es erschließt die Originalquellen. Es ist *nicht* gut für Alltagssprache, für schnelles Sprechen oder für emotionalen Ausdruck; dafür gibt es bessere Werkzeuge.",
 "2": "Musterantwort: (1) „Latein ist eine tote Sprache\" — sie wird gesprochen, nur bewegt sie sich nicht weiter mit der Welt: Klerus, Juristen, Historiker, Diplomaten. (2) „Latein ist voller Ausnahmen\" — die Ausnahmen sind systematisch und in den Paradigmen sichtbar (Kapitel 6–15). (3) „Nach einem Jahr kann ich Cäsar lesen\" — das ist die Folge von *nicht* beherrschen; für solides Lese-Latein braucht es 500–600 Stunden.",
 "3": "Musterantwort: Ja, wenn der Plan real ist: rund **500–600 Stunden** für solides Lese-Latein, also bei 4 Stunden pro Woche etwa **25–30 Wochen** — ein halbes Jahr, ehrlich gerechnet. Ein unrealistischer Plan fällt beim ersten Rückfall in sich zusammen.",
 "4": "Musterantwort: Beide müssen **griffbereit** sein, nicht bloß vorhanden: der Formenspiegel (Anhang III) beim Bilden von Formen, das Vokabelverzeichnis (Anhang I) beim Lesen. Wer sie erst suchen muss, verliert den Faden.",
},

# ---------------------------------------------------------------- Kapitel 11
"11": {
 "3": "Musterantwort: *fīō* ist die aktivere Form: Sie trägt die Endung **-ō** (1. Person Singular Aktiv) und bezeichnet den **Übergang**: „ich werde zu etwas\". *fītur* trägt die Endung **-tur** (3. Person Singular Passiv) und ist unpersönlich gemeint: „es geschieht\". Das *-or, -eris, -itur* ist das Passivkennzeichen — die Handlung geht **nicht** vom Subjekt aus, sondern trifft es. Also: *fīō* = „ich werde (etwas)\", *fītur* = „es geschieht\".",
},

# ---------------------------------------------------------------- Kapitel 12
"12": {
 "3": "Musterantwort: *eius* ist das **Possessivpronomen der 3. Person** und wird **nicht dekliniert** — es hat nur die eine Form *eius* für alle Fälle: *eius librum legit* = „(er/sie) liest sein Buch\". *eiusdem* ist die **dative Form** desselben Pronomens: *eiusdem puerō librum dedit* = „er gab **demselben** Jungen das Buch\". Der Unterschied ist also **Nominativbesitz** (*eius* = „sein\") gegenüber **Dativ** (*eiusdem* = „demselben\") — das *-dem* ist das Kennzeichen des Dativs.",
},

# ---------------------------------------------------------------- Kapitel 13
"13": {
 "3": "Musterantwort: Der Unterschied liegt im **Stammvokal**: *mīlit-* hat einen kurzen, geschlossenen Vokal → **i-Stamm** → Genitiv Plural **-ium**. *cōnsul-* hat einen langen Vokal → konsonantischer Stamm → Genitiv Plural **-um**. Man kann das nie aus der Endung allein entscheiden, sondern immer nur aus dem Stamm: kurzer Vokal → *-ium*, langer Vokal → *-um*. Merke: *mīlitum* (mit langem ū) wäre der Genitiv Singular.",
},

# ---------------------------------------------------------------- Kapitel 14
"14": {
 "3": "Musterantwort: *Nihil pulchrius est* ist **kein echter Vergleich**, weil das Vergleichsglied fehlt. *Pulchrius* ist hier der **absolute Superlativ** (Elativ) und heißt „so schön wie möglich\" — „Nichts ist so schön\". Der deutsche Komparativ „nichts ist schöner\" verlangt dagegen ein *quam* + Vergleichspartner: *nihil pulchrius est quam …*. Ohne dieses *quam* liest das Deutsche fälschlich einen Vergleich, den das Latein gar nicht macht.",
},

# ---------------------------------------------------------------- Kapitel 15
"15": {
 "3": "Musterantwort: *domus* sieht nur **oberflächlich** wie 2. Deklination aus: Endung *-us* im Nominativ Singular wie *servus*. Tatsächlich ist es **4. Deklination** — erkennbar am **Genitiv Singular *domūs*** (nicht *domus*) und am **Genitiv Plural *domuum*** (nicht *domōrum*). Das Genus ist **feminin** (wie *manus, -ūs* *f.*), nicht maskulin: *domus* = „das Haus\" gehört zum weiblichen Bereich (Haus, Herd, Familie).",
},

# ---------------------------------------------------------------- Kapitel 16
"16": {
 "3": "Musterantwort: Der Unterschied macht die **Präposition**, nicht das Nomen: *in* + **Ablativ** = **WO?** (*in urbe* = „in der Stadt\", *wo?*); *in* + **Akkusativ** = **WOHIN?** (*in urbem* = „in die Stadt\", *wohin?*). Im Deutschen ist beides „in\" + Akkusativ, deshalb muss man den Kasus im Latein selbst setzen: *in urbe* (Abl.) = *in der Stadt*, *in urbem* (Akk.) = *in die Stadt*.",
},

# ---------------------------------------------------------------- Kapitel 17
"17": {
 "3": "Musterantwort: Beide Formen gehören zum selben Verb, aber zu **verschiedenen Tempora**: *monet* ist **Präsens** („er ermahnt\"), *monuit* ist **Perfekt** („er hat ermahnt\"). Das lateinische Perfekt drückt nicht nur die Vergangenheit aus, sondern das **Ergebnis**: „er hat ermahnt — und der Ermahnung wirkt noch\". Das deutsche „ermahnen\" (Präsens) und „ermahnte\" (Präteritum) zeigen diesen Ergebnisbezug nicht; deshalb entscheidet der Kontext: *Magister discipulōs monuit* = „der Lehrer hat die Schüler ermahnt (und sie wissen es noch)\", *monet* = „der Lehrer ermahnt (gerade)\".",
},

# ---------------------------------------------------------------- Kapitel 18
"18": {
 "3": "Musterantwort: Weil das **Futursystem** im Latein nur **aktiv** ausgebildet ist: Präsensstamm + Futurendung (*amābō, dūcō, capiam*). Für das Passiv gibt es keine eigene Endungsreihe. Man umschreibt deshalb: **Partizip Perfekt Passiv + *irī*** = *amātum irī* = „es wird geliebt werden\". Die Umschreibung ist nicht nur Notlösung, sondern der **normale** Ausdruck — besonders in der indirekten Rede und in der Betonung des Vorgangs (*amātūrus est* = „der wird lieben\").",
},

# ---------------------------------------------------------------- Kapitel 19
"19": {
 "3": "Musterantwort: *amātum esse* ist eine **Infinitivform aus zwei Wörtern**: dem Partizip Perfekt Passiv *amātum* und dem Infinitiv *esse*. Ein echter Infinitiv wäre nur **ein** Wort: *amāre*, *esse*, *venīre*. Die Zweiteiligkeit ist das Merkmal der **periphrastischen Form**: *amātum esse* = Futur Passiv, *amātum fuisse* = Plusquamperfekt Passiv. Einen Infinitiv wie *amāre* erkennt man dagegen an der Endung: *-āre, -ēre, -ere, -īre*.",
},

# ---------------------------------------------------------------- Kapitel 20
"20": {
 "3": "Musterantwort: In *Vēnit, ut vidēret* ist der Konjunktiv **Imperfekt**, weil die Absicht **in der Vergangenheit** liegt: „er kam, um zu sehen\" — das Sehen war sein damaliger Plan. Der Imperfekt ist die **Nebensatzform des Präsenssystems** und bildet daher alle Zeiten des Präsenssystems ab: Präsens *vidēat*, Imperfekt *vidēret*, Perfekt *vidērit*. Analog: *Vēnit, ut vidēbit* = „er wird kommen, um zu sehen\" (Zukunft) → Konjunktiv Präsens; *Vēnerat, ut videret* = „er war gekommen, um zu sehen\" → Konjunktiv Plusquamperfekt.",
},

# ---------------------------------------------------------------- Kapitel 21
"21": {
 "3": "Musterantwort: *adferō* ist ein **Verb mit dem Präfix *ad-*** und heißt „herbringen, zuführen\" — das *ad-* gehört zum Stamm, es gibt kein Leerzeichen, und das Wort steht **für sich allein**. *ad puellam* sind **zwei Wörter**: die Präposition *ad* („zu\") und das Nomen *puellam* („das Mädchen\"). Das eine ist ein unselbständiger Wortteil, das andere ein selbständiges Wort mit eigener Bedeutung. Im Deutschen sieht beides gleich aus („ankommen\" / „zu ihr\"), im Latein nicht — deshalb ist *adferō puellam* (ich bringe das Mädchen) etwas anderes als *ad puellam* (zu dem Mädchen).",
},

# ---------------------------------------------------------------- Kapitel 22
"22": {
 "3": "Musterantwort: Weil beide Formen **gleich dekliniert** sind: *tablinum* kann Nominativ Singular (das Arbeitszimmer) **oder** Akkusativ Singular (das Arbeitszimmer) sein, und *est* kann von *tablinum* oder vom vorausgehenden Nomen ausgehen. Erst der **Kontext** entscheidet: *est in atriō tablinum* = „das Arbeitszimmer **ist** im Atrium\" (Nom. + *est*) gegenüber *est in atriō tablinum …* = „**im** Arbeitszimmer **ist** …\" (Akk. als adverbialer Ort). Die Form allein genügt nie — man muss den **Satzbau** prüfen: wer Subjekt und wer Objekt ist.",
},

# ---------------------------------------------------------------- Kapitel 23
"23": {
 "3": "Musterantwort: *magnae sapientiae* ist ein **Genitiv der Art und Beschaffenheit** (Qualitätsgenitiv), nicht ein Besitzgenitiv: „ein Mann **von** großer Weisheit\". Der Besitzgenitiv stünde bei *vir magnus sapientiae* — „ein Mann, **der** große Weisheit **besitzt**\". Der Unterschied: Beim Besitzgenitiv gehört die Weisheit **dem Mann** (er hat sie); beim Qualitätsgenitiv ist die Weisheit **eine Eigenschaft** (er *ist* weise). Beide stehen im Genitiv — die Funktion zeigt erst der Kontext.",
},

# ---------------------------------------------------------------- Kapitel 24
"24": {
 "3": "Musterantwort: Der Unterschied liegt in der **Präposition**: *in Rōmam* heißt „**in** Rom **hinein**\" — Akkusativ der Richtung *innerhalb* einer Grenze (der Akkusativ bei *in* mit Bewegungsverben). *Rōmam* (ohne Präposition) heißt „**nach** Rom\" — der Akkusativ der Richtung **auf ein Ziel** hin, wie bei Städte-, Länder- und Inselnamen (*Rōmam īre* = „nach Rom gehen\"). Das eine betont das Hineingehen in einen Raum, das andere das Auf-ein-Ziel-zu-Gehen.",
},

# ---------------------------------------------------------------- Kapitel 25
"25": {
 "3": "Musterantwort: *Est mihi liber* ist eine **Dativkonstruktion**: *mihi* ist der Dativ (Besitzer), *liber* der Nominativ (Sache) — wörtlich „Mir ist ein Buch\", also „Ich habe ein Buch\". Das ist kein Fehler, sondern die **regelmäßige lateinische Possessivform**. Deutsch hat diese Konstruktion nicht, deshalb wirkt sie fremd; das Lateinische besitzt sie für alle Verben des Seins und Habens: *est mihi frāter* = „ich habe einen Bruder\".",
},
}
