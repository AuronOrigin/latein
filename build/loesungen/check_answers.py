# -*- coding: utf-8 -*-
"""Vereinigt die drei Teile der fachlichen Prüfungscheck-Musterantworten.

Aufruf::

    from check_answers import CHECK_ANSWERS
"""

from check_answers_a import CHECK_ANSWERS as _A
from check_answers_b import CHECK_ANSWERS_B as _B
from check_answers_c import CHECK_ANSWERS_C as _C

CHECK_ANSWERS: dict[str, dict[str, str]] = {}
for _src in (_A, _B, _C):
    for _kap, _items in _src.items():
        CHECK_ANSWERS.setdefault(_kap, {}).update(_items)

__all__ = ["CHECK_ANSWERS"]
