import requests
import xml.etree.ElementTree as ET
import time

EMAIL = "elhathout75@gmail.com"
BATCH_SIZE = 200

# Charger les PMIDs
with open("pmids.txt", "r", encoding="utf-8") as f:
    pmids = [line.strip() for line in f if line.strip().isdigit()]

def fetch_batch(batch):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(batch),
        "retmode": "xml",
        "email": EMAIL
    }
    r = requests.get(url, params=params, timeout=90)
    r.raise_for_status()
    return r.text

mh_by_pmid = {}

for i in range(0, len(pmids), BATCH_SIZE):
    batch = pmids[i:i+BATCH_SIZE]
    print(f"Batch {i} → {i+len(batch)}")

    xml_data = fetch_batch(batch)
    root = ET.fromstring(xml_data)

    for article in root.findall(".//PubmedArticle"):
        pmid_elem = article.find(".//MedlineCitation/PMID")
        if pmid_elem is None or not pmid_elem.text:
            continue
        pmid = pmid_elem.text.strip()

        mh = set()
        for desc in article.findall(".//MeshHeading/DescriptorName"):
            if desc.text:
                mh.add(desc.text.strip().lower())
        mh_by_pmid[pmid] = mh

    time.sleep(0.34)  # respect NCBI rate limit (≈ 3 req/sec)

with open("pubmed_mh.tsv", "w", encoding="utf-8") as out:
    for pmid in pmids:
        terms = sorted(mh_by_pmid.get(pmid, set()))
        out.write(pmid + "\t" + ";".join(terms) + "\n")

print("PMIDs avec MH récupérés :", sum(1 for v in mh_by_pmid.values() if v))

