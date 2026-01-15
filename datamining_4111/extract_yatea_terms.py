#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

TERM_LIST = Path("yatea_run/docs/default/raw/termList.txt")
OUT = Path("yatea_terms_lemmas.txt")

terms = set()

with TERM_LIST.open(encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        # termList format: ID, inflected, lemma, freq, ...
        if len(parts) < 3:
            continue
        lemma = parts[2].strip().lower()
        if lemma:
            terms.add(lemma)

OUT.write_text("\n".join(sorted(terms)) + "\n", encoding="utf-8")
print(f"OK: {len(terms)} termes (lemmes) écrits dans {OUT}")

