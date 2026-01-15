import os, re, csv, subprocess
from pathlib import Path

CORPUS_TSV = "corpus_clean.tsv"
GOLD_MH = "pubmed_mh_clean.tsv"   # ton gold (PMID -> mh1;mh2;...)
RCFILE = "yatea_per_doc/yatea.rc"

TREETAGGER_BIN = os.path.expanduser("~/treetagger/bin/tree-tagger")
TREETAGGER_PAR = os.path.expanduser("~/treetagger/lib/english.par")

WORKDIR = Path("yatea_per_doc")
TMPDIR = WORKDIR / "tmp"
OUTDIR = WORKDIR / "out"

def load_gold(path):
    gold = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            pmid, items = line.split("\t", 1)
            terms = set(x.strip().lower() for x in items.split(";") if x.strip())
            if terms:
                gold[pmid] = terms
    return gold

def tokenize(text):
    # simple, stable tokenization (ok pour TreeTagger)
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*|[^\sA-Za-z0-9]", text)

def run_cmd(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return r.returncode, r.stdout, r.stderr

def extract_yatea_terms(term_list_path):
    """
    termList.txt colonnes typiques:
      ID <tab> inflected_form <tab> lemmatized_form <tab> freq ...
    On prend la forme lemmatisée (col 3).
    """
    terms = set()
    with open(term_list_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                lem = parts[2].strip().lower()
                if lem:
                    terms.add(lem)
    return terms

def main():
    gold = load_gold(GOLD_MH)
    print("PMIDs gold (avec MH):", len(gold))

    # lire corpus_clean.tsv (pmid \t text)
    docs = []
    with open(CORPUS_TSV, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 2: 
                continue
            pmid, text = row[0].strip(), row[1].strip()
            if pmid in gold:
                docs.append((pmid, text))

    print("Docs à traiter (intersection corpus ∩ gold):", len(docs))

    results = []
    for i, (pmid, text) in enumerate(docs, 1):
        # 1) token file
        tok_path = TMPDIR / f"{pmid}.tok"
        with open(tok_path, "w", encoding="utf-8") as g:
            for t in tokenize(text):
                g.write(t + "\n")
            g.write(".\n")

        # 2) treetagger -> ttg
        ttg_path = TMPDIR / f"{pmid}.ttg"
        cmd_tt = [TREETAGGER_BIN, "-token", "-lemma", TREETAGGER_PAR, str(tok_path)]
        rc, out, err = run_cmd(cmd_tt)
        if rc != 0:
            print("TreeTagger error for", pmid, err[:200])
            continue
        ttg_path.write_text(out, encoding="utf-8")

        # 3) yatea output dir unique
        out_run_dir = OUTDIR / pmid
        if out_run_dir.exists():
            # si relance
            subprocess.run(["rm", "-rf", str(out_run_dir)])

        # YaTeA va créer un repo dans le cwd; on lance dans le dossier out/pmid
        out_run_dir.mkdir(parents=True, exist_ok=True)

        cmd_y = ["yatea", f"--rcfile={os.path.abspath(RCFILE)}", str(ttg_path)]
        rc, out2, err2 = run_cmd(cmd_y, cwd=str(out_run_dir))
        if rc != 0:
            print("YaTeA error for", pmid, err2[:200])
            continue

        # 4) récupérer termList.txt
        # Le chemin exact dépend du suffix; avec config par défaut: corpus/default/raw/termList.txt
        term_list = out_run_dir / "corpus" / "default" / "raw" / "termList.txt"
        if not term_list.exists():
            # parfois YaTeA nomme le repo selon le fichier
            # on cherche termList.txt
            found = list(out_run_dir.rglob("termList.txt"))
            if not found:
                print("termList not found for", pmid)
                continue
            term_list = found[0]

        pred = extract_yatea_terms(term_list)
        g = gold[pmid]

        if not pred:
            p = r = f1 = 0.0
        else:
            inter = len(pred & g)
            p = inter / len(pred) if pred else 0.0
            r = inter / len(g) if g else 0.0
            f1 = (2*p*r/(p+r)) if (p+r) else 0.0

        results.append((pmid, p, r, f1, len(pred), len(g)))
        if i % 50 == 0:
            print(f"{i}/{len(docs)} traités")

    # save + mean
    out_tsv = WORKDIR / "yatea_vs_pubmed_eval.tsv"
    with open(out_tsv, "w", encoding="utf-8") as w:
        w.write("pmid\tprecision\trecall\tf1\tpred_n\tgold_n\n")
        for row in results:
            w.write("\t".join(map(str, row)) + "\n")

    if results:
        mp = sum(x[1] for x in results) / len(results)
        mr = sum(x[2] for x in results) / len(results)
        mf = sum(x[3] for x in results) / len(results)
        print("\nPMIDs évalués:", len(results))
        print("Précision moyenne:", mp)
        print("Rappel moyen:", mr)
        print("F-score moyen:", mf)
        print("Fichier:", out_tsv)

if __name__ == "__main__":
    main()

