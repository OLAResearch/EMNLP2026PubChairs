"""Split a GPTZero flagged-citation CSV into one file per annotator, by paper.

All citations of a paper go to the same annotator. Papers are balanced so each
annotator gets about the same number of papers and of citations.

Usage: python3 split_papers.py results.csv [--annotators 2]
Writes results_annotator1.csv, results_annotator2.csv, ... next to the input.
"""
import argparse
import csv
from collections import OrderedDict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", type=Path, help="GPTZero flagged-citation CSV")
    ap.add_argument("--annotators", "-n", type=int, default=2, help="number of annotators (default 2)")
    args = ap.parse_args()

    with args.csv.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        papers = OrderedDict()
        for row in reader:
            papers.setdefault(row["paper_id"], []).append(row)

    n = args.annotators
    max_papers = -(-len(papers) // n)  # ceil: paper counts differ by at most one
    buckets = [[] for _ in range(n)]
    load = [0] * n
    # Largest papers first, each to the least-loaded annotator with room left.
    for pid in sorted(papers, key=lambda p: (-len(papers[p]), p)):
        i = min((i for i in range(n) if len(buckets[i]) < max_papers), key=lambda i: load[i])
        buckets[i].append(pid)
        load[i] += len(papers[pid])

    for i, pids in enumerate(buckets, 1):
        out = args.csv.with_name(f"{args.csv.stem}_annotator{i}.csv")
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for pid in papers:  # keep the original paper order
                if pid in pids:
                    w.writerows(papers[pid])
        print(f"{out.name}: {len(pids)} papers, {load[i - 1]} citations")


if __name__ == "__main__":
    main()
