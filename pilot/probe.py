"""Pilote : la représentation interne d'une question encode-t-elle « un chiffre est publié » ?
(PREREG-AMENDEMENT-4.md). Analyse seule, numpy seul, sans le modèle : lit pilot/activations.npz.

Règles fixées avant toute donnée :
- 49 questions SOURCED (positif) et NOT_FOUND ; CONTESTED exclu.
- Sonde : régression logistique L2 (C = 0.1, pas de réglage), écrite sous forme duale (n petit, d grand),
  standardisation apprise sur les seules questions d'entraînement de chaque pli.
- Validation croisée : un pli par procedure_id (leave-one-procedure-out), AUROC sur les scores hors pli.
- Couche principale : 14 (milieu des 28 couches de Qwen2.5-1.5B) ; les autres couches sont descriptives.
- Témoins, mêmes plis et même sonde :
  (1) texte : unigrammes et bigrammes de mots de la question, vocabulaire appris sur chaque pli ;
  (2) plongements lexicaux : moyenne de la couche 0 sur les tokens de la question ;
  (3) permutation des étiquettes entre questions (1 000 permutations, couche principale).
- IC à 95 % par bootstrap sur les questions (10 000, graine 20261108), différences appariées.
- Score hors pli : X·w, sans l'intercept (qui dépend du taux de positifs de chaque pli).
- Verdict : « décodable linéairement » si borne basse de l'AUROC > 0,5 et p de permutation < 0,05 ;
  « au-delà d'une ligne de base textuelle » seulement si, en plus, les bornes basses de (couche 14 − texte) et (couche 14 − plongements)
  sont > 0 ; sinon « non concluant ». Jamais « le modèle sait ».

Usage : .venv/bin/python pilot/probe.py   ->  results/pilot.json, results/pilot.md
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
C, LAYER, SEED, B, PERMS = 0.1, 14, 20261108, 10000, 1000


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def fit_dual(X, y, c=C, iters=50):
    """Logistique L2 en duale : w = Xᵀa, objectif Σ log(1+exp(-y f)) + (1/2c)·aᵀKa, f = Ka + b, y ∈ {0,1}."""
    s = 2.0 * y - 1.0
    K = X @ X.T
    n = len(y)
    a, b, lam = np.zeros(n), 0.0, 1.0 / c
    for _ in range(iters):
        f = K @ a + b
        p = sigmoid(s * f)
        g = -s * (1 - p)                       # dérivée de la perte par rapport à f
        w = p * (1 - p)                        # courbure
        grad = np.concatenate([K @ g + lam * (K @ a), [g.sum()]])
        H = np.zeros((n + 1, n + 1))
        H[:n, :n] = K @ (w[:, None] * K) + lam * K + 1e-8 * np.eye(n)
        H[:n, n] = H[n, :n] = K @ w
        H[n, n] = w.sum() + 1e-8
        step = np.linalg.solve(H, grad)
        a, b = a - step[:n], b - step[n]
        if np.abs(step).max() < 1e-8:
            break
    return a, b


def oof_scores(feats, y, groups, c=C):
    """Scores hors pli, un pli par groupe ; feats(train_idx, test_idx) -> (X_train, X_test)."""
    out = np.zeros(len(y))
    for g in sorted(set(groups)):
        te = np.array([x == g for x in groups])
        tr = ~te
        if len(set(y[tr])) < 2:
            out[te] = 0.0
            continue
        Xtr, Xte = feats(np.where(tr)[0], np.where(te)[0])
        mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
        Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
        a, b = fit_dual(Xtr, y[tr], c)
        out[te] = Xte @ (Xtr.T @ a)   # sans b : l'intercept dépend du taux de positifs du pli et fausserait l'AUROC poolée
    return out


def auroc(score, y):
    pos, neg = score[y == 1], score[y == 0]
    if not len(pos) or not len(neg):
        return float("nan")
    return float(((pos[:, None] > neg[None, :]) + 0.5 * (pos[:, None] == neg[None, :])).mean())


def boot(scores, y, rng_seed=SEED):
    """IC par bootstrap sur les questions, mêmes tirages pour tous les scores (différences appariées)."""
    idx = np.random.default_rng(rng_seed).integers(0, len(y), size=(B, len(y)))
    res = {k: np.array([auroc(v[i], y[i]) for i in idx]) for k, v in scores.items()}
    return res


def ci(x):
    lo, hi = np.nanpercentile(x, [2.5, 97.5])
    return [round(float(lo), 4), round(float(hi), 4)]


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return re.findall(r"[a-z0-9]+", t)


def text_features(questions):
    toks = [norm(q) for q in questions]
    grams = [set(t) | {a + " " + b for a, b in zip(t, t[1:])} for t in toks]

    def feats(tr, te):
        vocab = sorted(set().union(*(grams[i] for i in tr)))
        col = {v: j for j, v in enumerate(vocab)}
        X = np.zeros((len(questions), len(vocab)))
        for i, gs in enumerate(grams):
            for v in gs:
                if v in col:
                    X[i, col[v]] = 1.0
        return X[tr], X[te]
    return feats


def analyze(last, embmean, y, groups, questions):
    layer = lambda L: (lambda tr, te: (last[tr, L], last[te, L]))  # noqa: E731
    per_layer = {}
    for L in range(last.shape[1]):
        per_layer[L] = auroc(oof_scores(layer(L), y, groups), y)
    s_main = oof_scores(layer(LAYER), y, groups)
    s_text = oof_scores(text_features(questions), y, groups)
    s_emb = oof_scores(lambda tr, te: (embmean[tr], embmean[te]), y, groups)
    bs = boot({"main": s_main, "text": s_text, "emb": s_emb}, y)
    rng = np.random.default_rng(SEED + 1)
    perm = np.array([auroc(oof_scores(layer(LAYER), yp, groups), yp)
                     for yp in (rng.permutation(y) for _ in range(PERMS))])
    a_main = auroc(s_main, y)
    p_perm = float((1 + (perm >= a_main).sum()) / (1 + PERMS))
    d_text, d_emb = bs["main"] - bs["text"], bs["main"] - bs["emb"]
    decodable = ci(bs["main"])[0] > 0.5 and p_perm < 0.05
    beyond = decodable and ci(d_text)[0] > 0 and ci(d_emb)[0] > 0
    return {
        "n": int(len(y)), "positifs_SOURCED": int(y.sum()), "plis": len(set(groups)), "C": C, "couche_principale": LAYER,
        "auroc_couche_principale": round(a_main, 4), "ic95": ci(bs["main"]), "p_permutation": round(p_perm, 4),
        "temoin_texte": {"auroc": round(auroc(s_text, y), 4), "ic95": ci(bs["text"]),
                         "difference": round(a_main - auroc(s_text, y), 4), "difference_ic95": ci(d_text)},
        "temoin_plongements": {"auroc": round(auroc(s_emb, y), 4), "ic95": ci(bs["emb"]),
                               "difference": round(a_main - auroc(s_emb, y), 4), "difference_ic95": ci(d_emb)},
        "par_couche_descriptif": {str(k): round(v, 4) for k, v in per_layer.items()},
        "verdict": "au-delà d'une ligne de base textuelle" if beyond else ("décodable linéairement" if decodable else "non concluant"),
    }


def fmt(x):
    return f"{x:.3f}".replace(".", ",")


def markdown(r, meta):
    L = [f"# Pilote : représentation interne de « chiffre publié » (généré par `pilot/probe.py`, ne pas éditer)", "",
         f"Modèle `{meta['model']}` (révision `{meta['revision'][:12]}`), {r['n']} questions ({r['positifs_SOURCED']} SOURCED), "
         f"{r['plis']} plis par procédure, régression logistique L2 (C = {r['C']}).", "",
         "| Mesure | AUROC [IC 95 %] |", "|---|---|",
         f"| Couche {r['couche_principale']} (principale) | {fmt(r['auroc_couche_principale'])} [{fmt(r['ic95'][0])} ; {fmt(r['ic95'][1])}], p permutation {fmt(r['p_permutation'])} |",
         f"| Témoin texte (n-grammes) | {fmt(r['temoin_texte']['auroc'])} [{fmt(r['temoin_texte']['ic95'][0])} ; {fmt(r['temoin_texte']['ic95'][1])}] |",
         f"| Témoin plongements lexicaux | {fmt(r['temoin_plongements']['auroc'])} [{fmt(r['temoin_plongements']['ic95'][0])} ; {fmt(r['temoin_plongements']['ic95'][1])}] |",
         f"| Couche principale − texte | {fmt(r['temoin_texte']['difference'])} [{fmt(r['temoin_texte']['difference_ic95'][0])} ; {fmt(r['temoin_texte']['difference_ic95'][1])}] |",
         f"| Couche principale − plongements | {fmt(r['temoin_plongements']['difference'])} [{fmt(r['temoin_plongements']['difference_ic95'][0])} ; {fmt(r['temoin_plongements']['difference_ic95'][1])}] |",
         "", f"**Verdict pré-inscrit : {r['verdict']}.**", "", "## Par couche (descriptif)", "",
         "| Couche | AUROC |", "|---|---|"] + [f"| {k} | {fmt(v)} |" for k, v in r["par_couche_descriptif"].items()]
    return "\n".join(L) + "\n"


def main():
    path = ROOT / "pilot" / "activations.npz"
    if not path.exists():
        sys.exit("pilot/activations.npz absent : lancer d'abord pilot/extract.py")
    d = np.load(path, allow_pickle=False)
    for k in ("last", "embmean"):
        if not np.isfinite(d[k].astype(np.float64)).all():
            sys.exit(f"activations non finies dans {k} : analyse refusée")
    meta = json.loads((ROOT / "pilot" / "activations.json").read_text())
    r = analyze(d["last"].astype(np.float64), d["embmean"].astype(np.float64), d["y"].astype(int),
                list(d["groups"]), list(d["questions"]))
    (ROOT / "results" / "pilot.json").write_text(json.dumps({"meta": meta, **r}, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "results" / "pilot.md").write_text(markdown(r, meta))
    print((ROOT / "results" / "pilot.md").read_text())


if __name__ == "__main__":
    main()
