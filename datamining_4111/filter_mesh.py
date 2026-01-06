from collections import Counter

# ===== PARAMÈTRE À AJUSTER SI BESOIN =====
MIN_FREQ = 5   # seuil minimal de fréquence d’un MeSH
# ========================================

freq = Counter()
rows = []

# Lecture des transactions MeSH brutes
with open("transactions_mesh.tsv", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        pmid, items = line.split("\t")
        meshes = set(items.split(","))   # set pour éviter doublons
        rows.append((pmid, meshes))
        freq.update(meshes)

# Sélection des MeSH fréquents
kept_meshes = {m for m, c in freq.items() if c >= MIN_FREQ}

print("Nombre total de MeSH différents :", len(freq))
print(f"MeSH conservés (fréquence >= {MIN_FREQ}) :", len(kept_meshes))

# Écriture des transactions filtrées
kept_pmids = 0
with open("transactions_mesh_filt.tsv", "w", encoding="utf-8") as out:
    for pmid, meshes in rows:
        filtered = sorted(meshes & kept_meshes)
        if filtered:
            out.write(pmid + "\t" + ",".join(filtered) + "\n")
            kept_pmids += 1

print("PMIDs conservés après filtrage :", kept_pmids)

