ids = set()
with open("transactions_mesh_filt.tsv", "r", encoding="utf-8") as f:
    for line in f:
        pmid, items = line.strip().split("\t")
        for m in items.split(","):
            if m.startswith("MESH:"):
                ids.add(m.replace("MESH:", ""))  # ex: D012640
            elif m.startswith("MESH_"):
                # au cas où (mais normalement TSV garde :)
                ids.add(m.replace("MESH_", ""))

with open("mesh_ids.txt", "w", encoding="utf-8") as out:
    for x in sorted(ids):
        out.write(x + "\n")

print("IDs MeSH uniques :", len(ids))

