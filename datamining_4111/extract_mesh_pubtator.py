import gzip
import re

# Charger les PMIDs du corpus
with open("pmids.txt", "r", encoding="utf-8") as f:
    pmids = set(line.strip() for line in f if line.strip().isdigit())

print("PMIDs chargés :", len(pmids))

mesh_pattern = re.compile(r"MESH:[A-Z0-9]+")
mesh_by_pmid = {p: set() for p in pmids}

with gzip.open("bioconcepts2pubtatorcentral.gz", "rt", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if not line or not line[0].isdigit():
            continue

        pmid = line.split("\t", 1)[0]
        if pmid not in mesh_by_pmid:
            continue

        for mesh in mesh_pattern.findall(line):
            mesh_by_pmid[pmid].add(mesh)

with open("transactions_mesh.tsv", "w", encoding="utf-8") as out:
    count = 0
    for pmid, meshes in mesh_by_pmid.items():
        if meshes:
            out.write(pmid + "\t" + ",".join(sorted(meshes)) + "\n")
            count += 1

print("PMIDs avec au moins un MeSH :", count)

