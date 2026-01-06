# Construction d’un fichier ARFF (format sparse) pour Weka

transactions = []
mesh_set = set()

with open("transactions_mesh_filt.tsv", "r", encoding="utf-8") as f:
    for line in f:
        pmid, items = line.strip().split("\t")
        meshes = items.split(",")
        transactions.append(meshes)
        mesh_set.update(meshes)

mesh_list = sorted(mesh_set)
mesh_index = {m: i for i, m in enumerate(mesh_list)}

with open("mesh.arff", "w", encoding="utf-8") as out:
    out.write("@RELATION mesh_pubtator\n\n")

    for m in mesh_list:
        # on remplace ":" par "_" pour compatibilité Weka
        out.write(f"@ATTRIBUTE {m.replace(':','_')} {{0,1}}\n")

    out.write("\n@DATA\n")

    for meshes in transactions:
        indices = sorted(mesh_index[m] for m in meshes)
        sparse_line = ",".join(f"{i} 1" for i in indices)
        out.write("{" + sparse_line + "}\n")

print("ARFF créé avec", len(mesh_list), "attributs et", len(transactions), "transactions")

