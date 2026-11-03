"""Tests des détecteurs (scripts/detectors.py) sur des textes synthétiques.

Lancer : .venv/bin/python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from detectors import detect_number, detect_number_no_lexicon, detect_v1, expressions  # noqa: E402
from score import clean  # noqa: E402

RESPONSE = "En général, **3 à 4 semaines** suffisent.\n- Le résultat peut atteindre 6 semaines."


class ExpressionTests(unittest.TestCase):
    def test_plages_et_bornes_ouvertes(self):
        self.assertEqual(expressions(clean("3 à 4 semaines")), [(21.0, 28.0, "days")])
        self.assertEqual(expressions(clean("jusqu'à 6 mois"))[0][0], None)
        self.assertEqual(expressions(clean("au moins 2 séances"))[0][1], None)
        self.assertEqual(expressions(clean("5 à 10 ans, voire plus"))[0][1], None)

    def test_nombres_incidents_ignores(self):
        self.assertEqual(expressions(clean("70-80 % de l'œdème, SPF 30")), [])
        self.assertEqual(expressions(clean("une séance de laser")), [])

    def test_unites_mixtes_converties(self):
        lo, hi, base = expressions(clean("de 3 mois à 1 an"))[0]
        self.assertEqual(base, "days")
        self.assertAlmostEqual(hi / lo, 365.25 / 91.32, places=3)


class DetectorTests(unittest.TestCase):
    def test_naifs(self):
        self.assertTrue(detect_number(RESPONSE))
        self.assertFalse(detect_number_no_lexicon(RESPONSE))  # « peut » dans la réponse
        self.assertTrue(detect_number_no_lexicon("3 à 4 semaines."))

    def test_v1_terme_dans_la_phrase_du_chiffre(self):
        self.assertTrue(detect_v1(RESPONSE, "weeks", "first", True))
        self.assertFalse(detect_v1(RESPONSE, "weeks", "envelope", True))  # 3 à 6 semaines, « peut »
        self.assertFalse(detect_v1("Cela varie, souvent 3 à 4 semaines.", "weeks", "any", False))

    def test_v1_filtre_de_base(self):
        r = "Comptez 2 à 3 séances."
        self.assertTrue(detect_v1(r, "sessions", "any", True))
        self.assertFalse(detect_v1(r, "weeks", "any", True))


if __name__ == "__main__":
    unittest.main()
