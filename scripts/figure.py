"""Figure de Q1 : surprécision contre utilité, par modèle, avec les politiques de référence (PREREG § 8).

Lit results/q1.json (analyse principale) et écrit results/q1_frontier.svg, sans dépendance externe.
Usage : .venv/bin/python scripts/figure.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H, L, R, T, B = 640, 460, 70, 30, 40, 60
COLORS = {"claude-haiku-5-5": "#2a78b4", "claude-opus-5-5": "#c2410c", "claude-sonnet-5-5": "#4d7c0f"}
NAMES = {"claude-haiku-5-5": "Haiku 5.5", "claude-opus-5-5": "Opus 5.5", "claude-sonnet-5-5": "Sonnet 5.5"}
LABEL = {"claude-haiku-5-5": (9, 16, "start"), "claude-opus-5-5": (9, -9, "start"),
         "claude-sonnet-5-5": (-9, -9, "end")}  # décalage x, y et ancrage, pour éviter les chevauchements


def x(v):
    return L + v * (W - L - R)


def y(v):
    return H - B - v * (H - T - B)


def svg(q1):
    p = q1["principal"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           'font-family="Helvetica, Arial, sans-serif" font-size="12">',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    for t in (0, 0.25, 0.5, 0.75, 1):
        out += [f'<line x1="{x(t)}" y1="{y(0)}" x2="{x(t)}" y2="{y(1)}" stroke="#e5e7eb"/>',
                f'<line x1="{x(0)}" y1="{y(t)}" x2="{x(1)}" y2="{y(t)}" stroke="#e5e7eb"/>',
                f'<text x="{x(t)}" y="{y(0) + 18}" text-anchor="middle" fill="#374151">{t:g}</text>',
                f'<text x="{x(0) - 8}" y="{y(t) + 4}" text-anchor="end" fill="#374151">{t:g}</text>']
    out += [f'<text x="{(x(0) + x(1)) / 2}" y="{H - 18}" text-anchor="middle" fill="#111827">'
            'Overprecision on NOT_FOUND questions (lower is better)</text>',
            f'<text transform="translate(20 {(y(0) + y(1)) / 2}) rotate(-90)" text-anchor="middle" fill="#111827">'
            'Utility on SOURCED questions (higher is better)</text>',
            f'<text x="{L}" y="24" fill="#111827" font-size="14" font-weight="bold">'
            'Q1, test set: rate and 95% cluster-bootstrap CI per model</text>']
    out += [f'<circle cx="{x(0)}" cy="{y(0)}" r="5" fill="none" stroke="#6b7280" stroke-width="1.5"/>',
            f'<text x="{x(0) + 8}" y="{y(0) - 8}" fill="#6b7280">always refuse or refer</text>',
            f'<line x1="{x(1)}" y1="{y(0)}" x2="{x(1)}" y2="{y(1)}" stroke="#6b7280" stroke-dasharray="4 4"/>',
            f'<text x="{x(1) - 6}" y="{y(1) + 14}" text-anchor="end" fill="#6b7280">always a precise number</text>']
    for m, c in COLORS.items():
        key = f"anthropic/{m}"
        o, u = p["surprecision"]["modeles"][key], p["utilite"]["modeles"][key]
        cx, cy = x(o["taux"]), y(u["taux"])
        out += [f'<line x1="{x(o["ic95"][0])}" y1="{cy}" x2="{x(o["ic95"][1])}" y2="{cy}" stroke="{c}" stroke-width="2" opacity="0.55"/>',
                f'<line x1="{cx}" y1="{y(u["ic95"][0])}" x2="{cx}" y2="{y(u["ic95"][1])}" stroke="{c}" stroke-width="2" opacity="0.55"/>',
                f'<circle cx="{cx}" cy="{cy}" r="6" fill="{c}"/>',
                f'<text x="{cx + LABEL[m][0]}" y="{cy + LABEL[m][1]}" text-anchor="{LABEL[m][2]}" fill="{c}" '
                f'font-weight="bold">{NAMES[m]}</text>']
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main():
    q1 = json.loads((ROOT / "results" / "q1.json").read_text())
    (ROOT / "results" / "q1_frontier.svg").write_text(svg(q1))
    print("results/q1_frontier.svg")


if __name__ == "__main__":
    main()
