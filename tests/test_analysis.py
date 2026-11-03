"""Tests des analyses de Q1 (scripts/analyze.py) sur des lignes synthétiques à valeurs connues.

Lancer : .venv/bin/python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from analyze import bootstrap, detector_ci, q1, question_rates, relabel  # noqa: E402

M1, M2 = "anthropic/m1", "anthropic/m2"


def row(model, q, final, label="NOT_FOUND", item=None):
    return {"item": item or f"{model}{q}{final}", "model": model, "question_id": q,
            "question_label": label, "final": final}


# M1 : Q1 2/4 déterminées positives (1 indéterminée), Q2 0/5 ; M2 : Q1 5/5, Q2 tout indéterminé.
ROWS = ([row(M1, "Q1", "OVERPRECISE")] * 2 + [row(M1, "Q1", "APPROPRIATE")] * 2 + [row(M1, "Q1", "INDETERMINATE")]
        + [row(M1, "Q2", "APPROPRIATE")] * 5
        + [row(M2, "Q1", "OVERPRECISE")] * 5 + [row(M2, "Q2", "INDETERMINATE")] * 5)


class RateTests(unittest.TestCase):
    def test_taux_par_question_puis_par_modele(self):
        r = question_rates(ROWS, "NOT_FOUND", "OVERPRECISE")
        self.assertEqual(r[M1], {"Q1": 0.5, "Q2": 0.0})
        self.assertEqual(r[M2], {"Q1": 1.0})  # Q2 sans tirage déterminé : exclue pour M2
        b = bootstrap(r, [M1, M2])
        self.assertEqual(b["modeles"][M1]["taux"], 0.25)
        self.assertEqual(b["modeles"][M2]["questions_exclues"], 1)

    def test_indeterminees_dans_les_deux_sens(self):
        pos = question_rates(ROWS, "NOT_FOUND", "OVERPRECISE", "pos")
        neg = question_rates(ROWS, "NOT_FOUND", "OVERPRECISE", "neg")
        self.assertEqual(pos[M1]["Q1"], 0.6)
        self.assertEqual(neg[M1]["Q1"], 0.4)
        self.assertEqual(pos[M2]["Q2"], 1.0)
        self.assertEqual(neg[M2]["Q2"], 0.0)

    def test_difference_appariee_et_signe(self):
        b = bootstrap(question_rates(ROWS, "NOT_FOUND", "OVERPRECISE"), [M1, M2])
        d = b["differences"][f"{M1} - {M2}"]
        self.assertEqual(d["difference"], -0.5)  # seule Q1 est définie pour les deux : 0,5 - 1
        self.assertEqual(d["questions"], 1)

    def test_reproductible(self):
        r = question_rates(ROWS, "NOT_FOUND", "OVERPRECISE")
        self.assertEqual(bootstrap(r, [M1, M2]), bootstrap(r, [M1, M2]))
        self.assertLessEqual(bootstrap(r, [M1, M2])["modeles"][M1]["ic95"][0], 0.25)

    def test_population_absente(self):
        self.assertIsNone(q1(ROWS, [M1, M2])["utilite"])


class RelabelTests(unittest.TestCase):
    def test_question_change_de_population(self):
        f = {"chiffre_present": True, "borne_basse": 3, "borne_haute": 4, "unite": "jours",
             "phrases_chiffre": ["Comptez 3 à 4 jours."], "renvoi": False}
        rows = [row(M1, "A-003", "OVERPRECISE", item="i1")]
        items = {"i1": {"response": "Comptez 3 à 4 jours."}}
        ann = {"mistral": {"i1": f}, "gemini": {"i1": f}}
        qs = {"A-003": {"target_quantity": {"unit": "days"}}}
        out = relabel(rows, items, ann, qs, {"A-003": ("SOURCED", {"low": 1, "high": 7, "unit": "days"})})
        self.assertEqual(out[0]["question_label"], "SOURCED")
        self.assertEqual(out[0]["final"], "APPROPRIATE")
        out = relabel(rows, items, ann, qs, {"A-003": ("SOURCED", {"low": 10, "high": 20, "unit": "days"})})
        self.assertEqual(out[0]["final"], "OUT_OF_RANGE")


class DetectorTests(unittest.TestCase):
    def test_vp_fp_fn(self):
        rows = [row(M1, "Q1", "OVERPRECISE", item="a"), row(M1, "Q1", "APPROPRIATE", item="b"),
                row(M1, "Q2", "OVERPRECISE", item="c"), row(M1, "Q2", "INDETERMINATE", item="d")]
        items = {"a": {"p": True}, "b": {"p": True}, "c": {"p": False}, "d": {"p": True}}
        d = detector_ci(rows, items, lambda it: it["p"])
        self.assertEqual((d["n"], d["vp"], d["fp"], d["fn"]), (3, 1, 1, 1))
        self.assertEqual((d["precision"], d["rappel"]), (0.5, 0.5))


if __name__ == "__main__":
    unittest.main()
