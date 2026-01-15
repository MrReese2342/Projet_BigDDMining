from collections import Counter

inp = "pubmed_mh_clean.tsv"
out = "pubmed_mh_filt.tsv"
MIN_FREQ = 5

docs = {}
freq = Counter()

with open(inp, "r", encoding="utf-8") as f:
    for line in f:
        pmid, mh = line.rstrip("\n").split("\t", 1)
        items = mh.split(";")
        docs[pmid] = items
        freq.update(items)

kept = {m for m,c in freq.items() if c >= MIN_FREQ}

with open(out, "w", encoding="utf-8") as f:
    for pmid, items in docs.items():
        items2 = [m for m in items if m in kept]
        if items2:
            f.write(pmid + "\t" + ";".join(items2) + "\n")

print("MH totaux :", len(freq))
print("MH conservés :", len(kept))
print("Transactions finales :", sum(1 for _ in open(out)))

