"""Draw summary statistics of a GPTZero flagged-citation CSV as an SVG chart.

Left: how many papers have 1, 2, 3, ... flagged citations.
Right: what the checker found when it compared each flagged citation's title
with the closest real source.

Usage: python3 plot_stats.py results.csv [-o hallucination_check_stats.svg]
Standard library only; the SVG follows the viewer's light/dark setting.
"""
import argparse
import csv
from collections import Counter
from html import escape
from pathlib import Path

W, H = 820, 330
TOP, BOTTOM = 92, 272          # plot area y-range shared by both panels
TITLE_OUTCOMES = [             # (title_match value, label), in display order
    ("no_match", "Title does not match"),
    ("", "No source found"),
    ("match", "Title matches"),
    ("partial_match", "Partial title match"),
]

# Explicit colours per mode (no CSS variables, so every SVG renderer shows them).
LIGHT = dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#8a8984", grid="#e7e6e2", axis="#bcbab4", s1="#2a78d6")
DARK = dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#8f8e86", grid="#2e2e2c", axis="#56554f", s1="#3987e5")
STYLE = """
  text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; fill: {ink2}; font-size: 12px; }}
  .bg {{ fill: {surface}; }}
  .h {{ fill: {ink}; font-size: 16px; font-weight: 650; }}
  .t1 {{ fill: {ink}; font-size: 13.5px; font-weight: 600; }}
  .t2, .muted, .tick {{ fill: {muted}; }}
  .tick {{ font-size: 11.5px; }}
  .lab {{ fill: {ink2}; font-size: 12.5px; }}
  .val {{ fill: {ink}; font-size: 12px; font-weight: 600; }}
  .muted {{ font-weight: 400; }}
  .grid {{ stroke: {grid}; stroke-width: 1; }}
  .axis {{ stroke: {axis}; stroke-width: 1; }}
  .bar {{ fill: {s1}; }}
"""


def nice_max(v, step):
    return max(step, -(-v // step) * step)


def left_panel(per_paper, x0, x1):
    ks = list(range(1, max(per_paper) + 1))
    ymax = nice_max(max(per_paper.values()), 10)
    y = lambda v: BOTTOM - (BOTTOM - TOP) * v / ymax
    slot = (x1 - x0) / len(ks)
    bw = min(34, slot - 6)
    out = [f'<text class="t1" x="{x0}" y="58">Papers by number of flagged citations</text>',
           f'<text class="t2" x="{x0}" y="78">{sum(per_paper.values())} papers</text>']
    for g in range(0, ymax + 1, 10):
        out.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{y(g):.1f}" y2="{y(g):.1f}"/>'
                   f'<text class="tick" x="{x0 - 8}" y="{y(g) + 4:.1f}" text-anchor="end">{g}</text>')
    for i, k in enumerate(ks):
        v = per_paper.get(k, 0)
        cx = x0 + slot * (i + 0.5)
        if v:
            h = BOTTOM - y(v)
            r = min(4, h)
            # Bar with rounded top corners, square at the baseline.
            out.append(f'<path class="bar" d="M{cx - bw / 2:.1f},{BOTTOM} v{-(h - r):.1f} '
                       f'q0,{-r} {r},{-r} h{bw - 2 * r:.1f} q{r},0 {r},{r} v{h - r:.1f} z">'
                       f'<title>{v} paper{"s" * (v != 1)} with {k} flagged citation{"s" * (k != 1)}</title></path>')
            out.append(f'<text class="val" x="{cx:.1f}" y="{y(v) - 6:.1f}" text-anchor="middle">{v}</text>')
        out.append(f'<text class="tick" x="{cx:.1f}" y="{BOTTOM + 18}" text-anchor="middle">{k}</text>')
    out.append(f'<line class="axis" x1="{x0}" x2="{x1}" y1="{BOTTOM}" y2="{BOTTOM}"/>')
    out.append(f'<text class="tick" x="{(x0 + x1) / 2:.1f}" y="{BOTTOM + 40}" text-anchor="middle">'
               f'Flagged citations per paper</text>')
    return out


def right_panel(title_counts, total, x0, x1):
    label_w = 150
    bx0, bx1 = x0 + label_w, x1 - 70
    vmax = max(title_counts.values())
    rows = len(TITLE_OUTCOMES)
    slot = (BOTTOM - TOP) / rows
    bh = min(24, slot - 10)
    out = [f'<text class="t1" x="{x0}" y="58">What the checker found for each citation</text>',
           f'<text class="t2" x="{x0}" y="78">{total} flagged citations, compared by title</text>']
    for i, (key, label) in enumerate(TITLE_OUTCOMES):
        v = title_counts.get(key, 0)
        cy = TOP + slot * (i + 0.5)
        w = (bx1 - bx0) * v / vmax
        r = min(4, w)
        out.append(f'<text class="lab" x="{bx0 - 10}" y="{cy + 4:.1f}" text-anchor="end">{escape(label)}</text>')
        if v:
            out.append(f'<path class="bar" d="M{bx0},{cy - bh / 2:.1f} h{w - r:.1f} q{r},0 {r},{r} '
                       f'v{bh - 2 * r:.1f} q0,{r} {-r},{r} h{-(w - r):.1f} z">'
                       f'<title>{escape(label)}: {v} citations</title></path>')
        out.append(f'<text class="val" x="{bx0 + w + 8:.1f}" y="{cy + 4:.1f}">{v} '
                   f'<tspan class="muted">({100 * v / total:.0f}%)</tspan></text>')
    out.append(f'<line class="axis" x1="{bx0}" x2="{bx0}" y1="{TOP}" y2="{BOTTOM}"/>')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=Path("hallucination_check_stats.svg"))
    args = ap.parse_args()

    with args.csv.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    per_paper = Counter(Counter(r["paper_id"] for r in rows).values())
    title_counts = Counter(r["title_match"] for r in rows)
    n_papers = len({r["paper_id"] for r in rows})

    body = [f'<text class="h" x="24" y="30">GPTZero hallucination check: {n_papers} papers, '
            f'{len(rows)} flagged citations</text>']
    body += left_panel(per_paper, 56, 380)
    body += right_panel(title_counts, len(rows), 440, W - 16)

    css = STYLE.format(**LIGHT) + "\n  @media (prefers-color-scheme: dark) {" + STYLE.format(**DARK) + "}\n"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
  aria-label="GPTZero hallucination check statistics: {n_papers} papers, {len(rows)} flagged citations">
<style>{css}</style>
<rect class="bg" width="{W}" height="{H}" rx="8"/>
{chr(10).join(body)}
</svg>
'''
    args.out.write_text(svg, encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
