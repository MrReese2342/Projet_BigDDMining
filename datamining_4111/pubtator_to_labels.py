# Charge mapping
mesh_map = {}
with open("mesh_id_label.tsv", "r", encoding="utf-8") as f:
    for line in f:
        mid, label = line.strip().split("\t", 1)
        mesh_map[mid] = label.strip().lower()

out_count = 0

with open("transactions_mesh_filt.tsv", "r", encoding="utf-8") as f, \
     open("pubtator_mesh_labels.tsv", "w", encoding="utf-8") as out:
    for line in f:
        pmid, items = line.strip().split("\t")
        labels = []
        for m in items.split(","):
            if m.startswith("MESH:"):
                mid = m.replace("MESH:", "")
                if mid in mesh_map:
                    labels.append(mesh_map[mid])
        labels = sorted(set(labels))
        if labels:
            out.write(pmid + "\t" + ";".join(labels) + "\n")
            out_count += 1

print("PMIDs convertis avec au moins un label :", out_count)

