import re

INPUT = "yatea_predicted_terms.tsv"
OUTPUT = "yatea_lemmas_weka.arff"

def clean_name(s: str) -> str:
    s = s.strip().lower()
    s = s.replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]", "_", s)      # vire % , - etc
    s = re.sub(r"_+", "_", s).strip("_")  # évite ____ et trim
    if not s or not re.match(r"^[a-z_]", s):
        s = "x_" + s
    return "T_" + s

transactions = {}
vocab_raw = []

with open(INPUT, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "\t" not in line:
            continue
        pmid, terms = line.split("\t", 1)
        items = [t.strip() for t in terms.split(";") if t.strip()]
        if not items:
            continue
        transactions[pmid] = set(items)
        vocab_raw.extend(items)

# Vocab unique brut
vocab_raw = sorted(set(vocab_raw))

# Mapping brut -> nom ARFF clean + unique
used = {}
mapping = {}
vocab_clean = []
for term in vocab_raw:
    base = clean_name(term)
    name = base
    k = 2
    while name in used:
        name = f"{base}_{k}"
        k += 1
    used[name] = True
    mapping[term] = name
    vocab_clean.append(name)

# Écriture ARFF
with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("@RELATION yatea_terms_weka\n\n")
    for attr in vocab_clean:
        out.write(f"@ATTRIBUTE {attr} {{0,1}}\n")
    out.write("\n@DATA\n")

    for pmid, items in transactions.items():
        row = []
        for raw_term in vocab_raw:
            row.append("1" if raw_term in items else "0")
        out.write(",".join(row) + "\n")

print("OK ->", OUTPUT)
print("Transactions:", len(transactions), "Attributs:", len(vocab_clean))

