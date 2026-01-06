pmids = set()

with open("corpus_clean.tsv", "r", encoding="utf-8") as f:
    for line in f:
        pmid = line.split("\t")[0].strip()
        if pmid.isdigit():
            pmids.add(pmid)

with open("pmids.txt", "w", encoding="utf-8") as out:
    for p in sorted(pmids):
        out.write(p + "\n")

print("PMIDs extraits :", len(pmids))

