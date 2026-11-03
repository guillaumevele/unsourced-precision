"""Tests de Q2 (scripts/q2_build.py, scripts/q2_analyze.py) sur des données synthétiques.

Lancer : .venv/bin/python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from q2_analyze import analyze, auroc_boot, parse, summary, verdict  # noqa: E402
from q2_build import displaced, figure  # noqa: E402

OPUS, SONNET = "anthropic/claude-opus-5-5", "anthropic/claude-sonnet-5-5"


class ParseTests(unittest.TestCase):
    def test_verdicts_et_confiance(self):
        self.assertEqual(parse("**Établi**. Confiance : 80/100."), 80.0)
        self.assertEqual(parse("Non établi — confiance 70 %"), 30.0)
        self.assertEqual(parse("Ce chiffre n'est pas établi. Confiance : 90."), 10.0)
        self.assertEqual(parse("Not established, confidence 60"), 40.0)

    def test_illisible(self):
        self.assertIsNone(parse("Cela dépend du patient."))
        self.assertIsNone(parse("Établi."))  # pas de confiance
        self.assertIsNone(parse("Non établi, confiance 250"))


class BuildTests(unittest.TestCase):
    def test_figure(self):
        self.assertEqual(figure(3, 4, "semaines"), "3 à 4 semaines")
        self.assertEqual(figure(2, 2, "séances"), "2 séances")
        self.assertEqual(figure(None, 6, "mois"), "jusqu'à 6 mois")
        self.assertEqual(figure(1.5, None, "jours"), "au moins 1,5 jours")
        self.assertIsNone(figure(1, 2, "semaines à mois"))

    def test_chiffre_deplace(self):
        self.assertEqual(displaced({"low": 2, "high": 4, "unit": "weeks"}), "12 semaines")
        self.assertEqual(displaced({"low": 3, "high": None, "unit": "months"}), "1 mois")
        self.assertEqual(displaced({"low": 1, "high": None, "unit": "days"}), "0,3 jours")
        self.assertIsNone(displaced({"low": 0, "high": 0, "unit": "days"}))


class AurocTests(unittest.TestCase):
    def test_valeurs_connues(self):
        pos = [("q1", 90.0), ("q2", 80.0)]
        neg = [("q3", 10.0), ("q4", 85.0)]
        self.assertEqual(auroc_boot(pos, neg)["auroc"], 0.75)  # 3 paires gagnées sur 4
        tie = auroc_boot([("q1", 50.0)], [("q2", 50.0)])
        self.assertEqual(tie["auroc"], 0.5)

    def test_reproductible_et_verdicts(self):
        pos = [(f"p{i}", 80.0 + i) for i in range(10)]
        neg = [(f"n{i}", 20.0 + i) for i in range(10)]
        s1, s2 = summary(auroc_boot(pos, neg)), summary(auroc_boot(pos, neg))
        self.assertEqual(s1, s2)
        self.assertEqual(verdict(s1), "discrimine")
        self.assertEqual(verdict({"auroc": 0.4, "ic95": [0.3, 0.55]}), "réfuté")
        self.assertEqual(verdict({"auroc": 0.6, "ic95": [0.45, 0.75]}), "non concluant")


class AnalyzeTests(unittest.TestCase):
    def test_temoins_et_croise(self):
        elements, scores = [], {}
        for i in range(6):
            for cls, val in (("a", 20.0), ("b", 80.0)):
                q = f"{cls}{i}"
                e = {"element": f"{q}-o", "class": cls, "author": OPUS, "question_id": q, "overprecise": cls == "a",
                     "bornes_identiques": True,
                     "sondes": {"auto": {OPUS: f"auto-{q}"}, "croisee": {SONNET: f"cro-{q}"},
                                "question": {OPUS: f"q-{q}"}}}
                elements.append(e)
                scores[f"auto-{q}"] = [val]
                scores[f"cro-{q}"] = [50.0]  # l'autre modèle ne distingue rien
                scores[f"q-{q}"] = [50.0]
        out = analyze(elements, scores, {})[OPUS]
        self.assertEqual(out["auto"]["auroc"], 1.0)
        self.assertEqual(out["question_seule"]["auroc"]["auroc"], 0.5)
        self.assertEqual(out["question_seule"]["auto_moins_temoin"]["difference"], 0.5)
        self.assertTrue(out["au_dela_de_la_question"])
        self.assertEqual(out["croise"]["auto_moins_croise"]["difference"], 0.5)
        self.assertIsNone(out["dispersion_q1"]["auroc"])  # aucune dispersion fournie


if __name__ == "__main__":
    unittest.main()
