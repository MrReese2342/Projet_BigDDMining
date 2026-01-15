import re

inp = "pubmed_mh.tsv"
out = "pubmed_mh_clean.tsv"

with open(inp, "r", encoding="utf-8") as fin, \
     open(out, "w", encoding="utf-8") as fout:

    for line in fin:
        line = line.rstrip("\n")
        if "\t" not in line:
            continue

        pmid, mh_str = line.split("\t", 1)
        if not mh_str.strip():
            continue

        mh_clean = set()
        for mh in mh_str.split(";"):
            mh = mh.strip().lower()
            if not mh:
                continue
            mh = mh.split("/")[0]   # <-- règle demandée
            mh_clean.add(mh)

        if mh_clean:
            fout.write(pmid + "\t" + ";".join(sorted(mh_clean)) + "\n")

print("Fichier pubmed_mh_clean.tsv généré")

