import json

input_path = "litcovid_clean.json"
output_path = "corpus_clean.tsv"

count = 0

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(output_path, "w", encoding="utf-8") as out:
    for item in data:
        pmid = str(item.get("pmid", "")).strip()
        title = item.get("title", "").strip()
        abstract = item.get("abstract", "").strip()

        if not pmid:
            continue

        text = title
        if abstract:
            text += " " + abstract

        if len(text) < 30:
            continue

        out.write(f"{pmid}\t{text}\n")
        count += 1

print("OK :", count, "articles écrits dans", output_path)

