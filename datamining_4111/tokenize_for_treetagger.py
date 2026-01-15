import re

inp = "texts_for_treetagger.txt"
out = "texts_for_treetagger.tok"

# Tokenizer simple mais robuste pour texte biomédical
# - garde les mots avec tirets/apostrophes (critical-illness, patient's)
# - garde les motifs type C->U
# - sépare ponctuation
token_re = re.compile(
    r"""
    [A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*      # mots / mots composés
    |[A-Za-z]\-\>[A-Za-z]                  # motifs type C->U
    |\d+(?:\.\d+)?%?                       # nombres, décimaux, %
    |[^\w\s]                               # ponctuation / symboles
    """,
    re.VERBOSE
)

with open(inp, "r", encoding="utf-8") as f_in, open(out, "w", encoding="utf-8") as f_out:
    for line in f_in:
        line = line.strip()
        if not line:
            continue
        toks = token_re.findall(line)
        for t in toks:
            f_out.write(t + "\n")
        f_out.write("\n")  # ligne vide = séparation doc/phrase

print("OK:", out, "généré")

