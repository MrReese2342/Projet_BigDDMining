inp = "pubmed_mh_filt.tsv"
out = "pubmed_mh.arff"

docs = []
items = set()

with open(inp, "r", encoding="utf-8") as f:
    for line in f:
        pmid, mh = line.rstrip("\n").split("\t", 1)
        s = set(mh.split(";"))
        docs.append(s)
        items.update(s)

items = sorted(items)

with open(out, "w", encoding="utf-8") as f:
    f.write("@RELATION pubmed_mh\n\n")
    for it in items:
        f.write(f"@ATTRIBUTE '{it}' {{0,1}}\n")
    f.write("\n@DATA\n")
    for d in docs:
        row = ["1" if it in d else "0" for it in items]
        f.write(",".join(row) + "\n")

print(f"ARFF créé : {len(docs)} transactions, {len(items)} attributs")

