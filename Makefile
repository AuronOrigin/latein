PY ?= python3

.PHONY: all html epub pdf anki check clean

all: html epub pdf anki check

html: ; $(PY) build/build.py --html
epub: ; $(PY) build/build.py --epub
pdf:  ; $(PY) build/build.py --pdf
anki: ; $(PY) build/build.py --anki
check: ; $(PY) build/build.py --check

clean:
	rm -rf dist build/anki/*.csv build/__pycache__
