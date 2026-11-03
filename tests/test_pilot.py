"""Tests de l'analyse du pilote (pilot/probe.py) sur des données synthétiques à valeurs connues.

Lancer : .venv/bin/python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pilot"))

from probe import auroc, fit_dual, oof_scores, sigmoid, text_features  # noqa: E402


class ProbeTests(unittest.TestCase):
    def test_auroc(self):
        self.assertEqual(auroc(np.array([0.9, 0.8, 0.1, 0.85]), np.array([1, 1, 0, 0])), 0.75)

    def test_signal_plante_retrouve_hors_pli(self):
        rng = np.random.default_rng(0)
        n, d = 40, 300
        y = np.array([0, 1] * 20)
        X = rng.normal(size=(n, d))
        X[:, :30] += 3.0 * (2 * y - 1)[:, None] / np.sqrt(30)   # signal réparti sur 30 axes, comme une activation
        groups = [f"g{i // 2}" for i in range(n)]          # 20 groupes de deux
        s = oof_scores(lambda tr, te: (X[tr], X[te]), y, groups)
        self.assertGreater(auroc(s, y), 0.85)

    def test_bruit_pur_proche_du_hasard(self):
        rng = np.random.default_rng(1)
        y = np.array([0, 1] * 20)
        X = rng.normal(size=(40, 300))
        s = oof_scores(lambda tr, te: (X[tr], X[te]), y, [f"g{i}" for i in range(40)])
        self.assertLess(abs(auroc(s, y) - 0.5), 0.25)

    def test_sans_signal_auroc_exactement_neutre(self):
        # caractéristiques constantes : scores tous nuls, AUROC 0,5 (l'intercept par pli ne doit pas l'abaisser)
        y = np.array([1] * 24 + [0] * 25)
        groups = [f"g{i % 38}" for i in range(49)]
        s = oof_scores(lambda tr, te: (np.ones((len(tr), 5)), np.ones((len(te), 5))), y, groups)
        self.assertEqual(auroc(s, y), 0.5)

    def test_bruit_moyen_proche_du_hasard(self):
        y = np.array([1] * 24 + [0] * 25)
        groups = [f"g{i % 38}" for i in range(49)]
        vals = []
        for seed in range(10):
            X = np.random.default_rng(seed).normal(size=(49, 200))
            vals.append(auroc(oof_scores(lambda tr, te: (X[tr], X[te]), y, groups), y))
        self.assertLess(abs(np.mean(vals) - 0.5), 0.1)

    def test_duale_separe_les_classes(self):
        X = np.array([[2.0, 0], [1.5, 0.2], [-2.0, 0], [-1.5, -0.2]])
        y = np.array([1, 1, 0, 0])
        a, b = fit_dual(X, y, c=1.0)
        p = sigmoid(X @ (X.T @ a) + b)
        self.assertTrue((p[:2] > 0.5).all() and (p[2:] < 0.5).all())

    def test_vocabulaire_appris_sur_le_pli_seulement(self):
        feats = text_features(["botox durée", "laser cicatrice", "mot unique"])
        Xtr, Xte = feats(np.array([0, 1]), np.array([2]))
        self.assertEqual(Xte.sum(), 0.0)                   # aucun mot du test absent de l'entraînement


if __name__ == "__main__":
    unittest.main()
