PY ?= python3

.PHONY: all html epub pdf anki check glossar clean

all: html epub pdf anki check

html: ; $(PY) build/build.py --html
epub: ; $(PY) build/build.py --epub
pdf:  ; $(PY) build/build.py --pdf
anki: ; $(PY) build/build.py --anki
check: ; $(PY) build/build.py --check

# Glossar: erzeugt glossar/vokabeln.csv und glossar/begriffe.csv
# aus den handgepflegten TSV-Quellen glossar/*.tsv
glossar: ; $(PY) tools/gen_glossar.py

clean:
	rm -rf dist build/anki/*.csv build/__pycache__ tools/__pycache__
