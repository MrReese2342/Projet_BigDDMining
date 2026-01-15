def load(path):
    d = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue

            parts = line.split("\t", 1)  # <-- tolérant
            pmid = parts[0].strip()
            items = parts[1].strip() if len(parts) > 1 else ""

            if items:
                d[pmid] = set(x.strip().lower() for x in items.split(";") if x.strip())
            else:
                d[pmid] = set()
    return d

pred = load("pubtator_mesh_labels.tsv")
gold = load("pubmed_mh.tsv")

P = R = F = 0.0
n = 0

for pmid, gold_set in gold.items():
    if not gold_set:
        continue  # on évalue seulement quand PubMed a des MH

    pred_set = pred.get(pmid, set())
    inter = gold_set & pred_set

    precision = len(inter) / len(pred_set) if pred_set else 0.0
    recall    = len(inter) / len(gold_set) if gold_set else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    P += precision
    R += recall
    F += f1
    n += 1

print("PMIDs évalués (gold non vide) :", n)
print("Précision moyenne :", P / n if n else 0.0)
print("Rappel moyen :", R / n if n else 0.0)
print("F-score moyen :", F / n if n else 0.0)

