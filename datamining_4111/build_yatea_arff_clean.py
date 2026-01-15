import csv

INPUT = "yatea_predicted_terms.tsv"
OUTPUT = "yatea_lemmas_clean.arff"

# Lire les transactions
transactions = {}
vocab = set()

with open(INPUT, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "\t" not in line:
            continue
        pmid, terms = line.split("\t", 1)
        items = [t.strip().replace(" ", "_") for t in terms.split(";") if t.strip()]
        if not items:
            continue
        transactions[pmid] = set(items)
        vocab.update(items)

vocab = sorted(vocab)

with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("@RELATION yatea_terms\n\n")
    for term in vocab:
        out.write(f"@ATTRIBUTE {term} {{0,1}}\n")
    out.write("\n@DATA\n")

    for pmid, items in transactions.items():
        row = ["1" if term in items else "0" for term in vocab]
        out.write(",".join(row) + "\n")

print("OK : ARFF propre généré ->", OUTPUT)

