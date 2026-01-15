#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

CORPUS = Path("corpus_clean.tsv")            # PMID \t texte
TERMS = Path("yatea_terms_lemmas.txt")       # liste globale YaTeA
OUT = Path("yatea_predicted_terms.tsv")      # PMID \t term1;term2;...

# Charge termes (on garde ceux de longueur >= 4 pour réduire le bruit)
terms = []
with TERMS.open(encoding="utf-8") as f:
    for t in f:
        t = t.strip().lower()
        if len(t) >= 4:
            terms.append(t)

# Pour accélérer un peu: trier par longueur desc (match des gros termes d'abord)
terms.sort(key=len, reverse=True)

def normalize(txt: str) -> str:
    return " " + txt.lower() + " "

n_docs = 0
n_nonempty = 0

with CORPUS.open(encoding="utf-8", errors="ignore") as f, OUT.open("w", encoding="utf-8") as g:
    for line in f:
        line = line.rstrip("\n")
        if not line:
            continue
        pmid, text = line.split("\t", 1)
        n_docs += 1
        txt = normalize(text)

        found = []
        # match très simple: substring
        for t in terms:
            if t in txt:
                found.append(t)

        # déduplique + limite (sinon énorme)
        found = sorted(set(found))[:200]
        if found:
            n_nonempty += 1
        g.write(pmid + "\t" + ";".join(found) + "\n")

print("OK:", n_docs, "docs traités")
print("Docs avec au moins 1 terme YaTeA matché:", n_nonempty)
print("Fichier:", OUT)

