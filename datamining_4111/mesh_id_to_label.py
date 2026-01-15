import requests
import time

def extract_label_value(v):
    # label peut être string, dict avec @value, ou liste
    if isinstance(v, str):
        return v
    if isinstance(v, dict) and "@value" in v:
        return v["@value"]
    if isinstance(v, list):
        for it in v:
            lab = extract_label_value(it)
            if lab:
                return lab
    return None

def get_label(mesh_id: str):
    url = f"https://id.nlm.nih.gov/mesh/{mesh_id}.json"
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        return None
    data = r.json()

    # Ici data est un dict et contient "label"
    if isinstance(data, dict) and "label" in data:
        return extract_label_value(data["label"])

    # fallback (au cas où)
    return None

if __name__ == "__main__":
    with open("mesh_ids.txt", "r", encoding="utf-8") as f:
        ids = [line.strip() for line in f if line.strip()]

    mapping = {}
    for i, mid in enumerate(ids, 1):
        lab = get_label(mid)
        if lab:
            mapping[mid] = lab.strip().lower()

        if i % 25 == 0:
            print(f"{i}/{len(ids)} traités, mapping={len(mapping)}")

        time.sleep(0.03)

    with open("mesh_id_label.tsv", "w", encoding="utf-8") as out:
        for mid in sorted(mapping):
            out.write(mid + "\t" + mapping[mid] + "\n")

    print("Mapping obtenu :", len(mapping))

