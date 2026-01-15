# build_yatea_arff.py
from collections import Counter

INPUT = "yatea_predicted_terms.tsv"
MIN_DOC_FREQ = 5
OUTPUT_ARFF = "yatea_lemmas.arff"

docs = {}
df = Counter()

with open(INPUT, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if "\t" not in line:
            continue   # <-- ligne invalide, on ignore
        pmid, items = line.split("\t", 1)
        terms = [t.strip().lower() for t in items.split(";") if t.strip()]
        if not terms:
            continue
        terms = sorted(set(terms))
        docs[pmid] = terms
        df.update(terms)

vocab = sorted([t for t, c in df.items() if c >= MIN_DOC_FREQ])
vocab_set = set(vocab)

transactions = []
for pmid, terms in docs.items():
    kept = [t for t in terms if t in vocab_set]
    if kept:
        transactions.append(kept)

print("Documents initiaux :", len(docs))
print("Vocab total :", len(df))
print("Vocab filtré :", len(vocab))
print("Transactions finales :", len(transactions))

with open(OUTPUT_ARFF, "w", encoding="utf-8") as out:
    out.write("@RELATION yatea_lemmas\n\n")
    for t in vocab:
        safe = t.replace("'", "").replace('"', "").replace(" ", "_").replace(",", "_")
        out.write(f"@ATTRIBUTE T_{safe} {{0,1}}\n")
    out.write("\n@DATA\n")

    for trans in transactions:
        row = []
        s = set(trans)
        for t in vocab:
            row.append("1" if t in s else "0")
        out.write(",".join(row) + "\n")

print("✅ ARFF créé :", OUTPUT_ARFF)

