import re
import csv

RULE_RE = re.compile(
    r"^\s*\d+\.\s+\[(?P<lhs>.+?)\]:\s*(?P<lhs_count>\d+)\s*==>\s*\[(?P<rhs>.+?)\]:\s*(?P<rhs_count>\d+).*?"
    r"<conf:\((?P<conf>[\d\.]+)\)>\s*lift:\((?P<lift>[\d\.]+)\)\s*lev:\((?P<lev>[-\d\.]+)\)\s*conv:\((?P<conv>[-\d\.]+)\)"
)

def parse_side(side: str):
    # ex: "T_a=1, T_b=1" -> ["T_a", "T_b"]
    items = []
    for part in side.split(","):
        part = part.strip()
        # retire "=1" si présent
        part = part.replace("=1", "").strip()
        if part:
            items.append(part)
    return items

def main():
    in_file = "yatea_rules.txt"
    edges_out = "neo4j_edges.csv"
    nodes_out = "neo4j_nodes.csv"

    nodes = set()
    edges = []

    with open(in_file, encoding="utf-8") as f:
        for line in f:
            m = RULE_RE.match(line.strip())
            if not m:
                continue

            lhs_items = parse_side(m.group("lhs"))
            rhs_items = parse_side(m.group("rhs"))

            conf = float(m.group("conf"))
            lift = float(m.group("lift"))
            lev = float(m.group("lev"))
            conv = float(m.group("conv"))

            # On crée une arête pour chaque paire (lhs_item -> rhs_item)
            for a in lhs_items:
                nodes.add(a)
                for b in rhs_items:
                    nodes.add(b)
                    edges.append({
                        "source": a,
                        "target": b,
                        "confidence": conf,
                        "lift": lift,
                        "leverage": lev,
                        "conviction": conv
                    })

    with open(nodes_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id"])
        for n in sorted(nodes):
            w.writerow([n])

    with open(edges_out, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["source", "target", "confidence", "lift", "leverage", "conviction"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for e in edges:
            w.writerow(e)

    print(f"OK nodes: {len(nodes)} -> {nodes_out}")
    print(f"OK edges: {len(edges)} -> {edges_out}")

if __name__ == "__main__":
    main()

