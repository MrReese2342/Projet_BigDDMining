#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

GOLD = Path("pubmed_mh_clean.tsv")         # PMID \t mh1;mh2;...
PRED = Path("yatea_predicted_terms.tsv")   # PMID \t term1;term2;...

def load(path: Path):
    d = {}
    with path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "\t" not in line:
                continue
            pmid, items = line.split("\t", 1)
            s = set(x.strip().lower() for x in items.split(";") if x.strip())
            d[pmid] = s
    return d

gold = load(GOLD)
pred = load(PRED)

pmids = sorted(set(gold.keys()) & set(pred.keys()))

p_sum = r_sum = f_sum = 0.0
n = 0

for pmid in pmids:
    G = gold[pmid]
    P = pred[pmid]
    if not G:
        continue
    tp = len(G & P)
    fp = len(P - G)
    fn = len(G - P)

    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0
    f1   = (2*prec*rec/(prec+rec)) if (prec+rec) else 0.0

    p_sum += prec
    r_sum += rec
    f_sum += f1
    n += 1

print("PMIDs évalués :", n)
print("Précision moyenne :", p_sum/n if n else 0)
print("Rappel moyen :", r_sum/n if n else 0)
print("F-score moyen :", f_sum/n if n else 0)

