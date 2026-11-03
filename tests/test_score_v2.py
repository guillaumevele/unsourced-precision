"""Tests du calcul v2 (PREREG-AMENDEMENT-1.md) sur des textes synthétiques.

Lancer : .venv/bin/python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from score import anchor, counting_v2, fields, final_label, sentences, to_base, unit_kind  # noqa: E402

RESPONSE = (
    "# Titre : combien de temps ?\n\n"
    "En général, **3 à 4 semaines** suffisent. Évitez le soleil, cela peut irriter.\n"
    "- Chez certains patients, la durée **peut** atteindre 6 semaines.\n"
    "- Le résultat dépend de la zone traitée."
)


def ann(**kw):
    base = {"chiffre_present": True, "borne_basse": 3, "borne_haute": 4, "unite": "semaines",
            "phrases_chiffre": ["En général, 3 à 4 semaines suffisent."], "renvoi": "aucun", "citations": []}
    return base | kw


class AnchorTests(unittest.TestCase):
    def test_citation_sans_balisage_retrouvee_et_limitee_a_sa_phrase(self):
        span = anchor("En général, 3 à 4 semaines suffisent.", sentences(RESPONSE))
        self.assertEqual(span, "en general, 3 a 4 semaines suffisent.")
        self.assertFalse(counting_v2(span))  # « peut » est dans la phrase suivante

    def test_citation_partielle_etendue_a_la_phrase_entiere(self):
        span = anchor("la durée peut atteindre 6", sentences(RESPONSE))
        self.assertIn("chez certains patients", span)
        self.assertTrue(counting_v2(span))

    def test_citation_inventee_introuvable(self):
        self.assertIsNone(anchor("3 à 4 semaines en moyenne selon les études", sentences(RESPONSE)))


class LexiconTests(unittest.TestCase):
    def test_decisions_v1_inchangees(self):
        for t in ("en general", "generalement", "habituellement", "en moyenne", "environ", "jusqu'a 6 mois",
                  "au moins 2 seances", "selon le phototype", "souvent", "parfois"):
            self.assertFalse(counting_v2(t), t)
        for t in ("la duree varie", "ils peuvent durer", "cela pourra prendre", "variable", "selon les cas",
                  "il n'existe pas de duree etablie", "cela depend de la zone", "pas de consensus"):
            self.assertTrue(counting_v2(t), t)

    def test_peu_adverbe_ne_compte_pas(self):
        self.assertFalse(counting_v2("un peu plus long"))
        self.assertTrue(counting_v2("peu d'etudes"))


class UnitTests(unittest.TestCase):
    def test_minutes_en_secondes_v2(self):
        lo, base = to_base(1, "minutes", "v2")
        hi, _ = to_base(30, "secondes", "v2")
        self.assertEqual(base, "days")
        self.assertAlmostEqual(lo / hi, 2.0)

    def test_v1_inchangee(self):
        self.assertEqual(unit_kind("minutes", "v1")[0], "count")
        self.assertIsNone(unit_kind("par semaine", "v1")[0])

    def test_par_semaine_v2(self):
        self.assertEqual(unit_kind("par semaine", "v2")[1], "per week")


class LabelTests(unittest.TestCase):
    def test_plage_precise_sans_terme_est_overprecise(self):
        x = fields(ann(), RESPONSE, "v2")
        self.assertEqual(final_label("NOT_FOUND", x, None, "weeks", "v2"), "OVERPRECISE")

    def test_terme_dans_la_phrase_citee_donne_appropriate(self):
        x = fields(ann(borne_basse=3, borne_haute=6,
                       phrases_chiffre=["3 à 4 semaines", "la durée peut atteindre 6 semaines"]), RESPONSE, "v2")
        self.assertEqual(final_label("NOT_FOUND", x, None, "weeks", "v2"), "APPROPRIATE")

    def test_invalides(self):
        cases = {"citation": ann(phrases_chiffre=["texte absent de la réponse"]),
                 "unite": ann(unite="fois toutes les 1 à 2 semaines"),
                 "sans_borne": ann(borne_basse=None, borne_haute=None)}
        for reason, f in cases.items():
            x = fields(f, RESPONSE, "v2")
            self.assertEqual(x["invalid"], reason)
            self.assertEqual(final_label("NOT_FOUND", x, None, "weeks", "v2"), "INVALID")

    def test_base_differente_sur_sourced_est_invalide(self):
        x = fields(ann(unite="séances", phrases_chiffre=["3 à 4 semaines"]), RESPONSE, "v2")
        rng = {"low": 2, "high": 6, "unit": "weeks"}
        self.assertEqual(final_label("SOURCED", x, rng, "weeks", "v2"), "INVALID")

    def test_sans_chiffre(self):
        x = fields(ann(chiffre_present=False, borne_basse=None, borne_haute=None, unite=None,
                       phrases_chiffre=[]), RESPONSE, "v2")
        self.assertEqual(final_label("SOURCED", x, {"low": 2, "high": 6, "unit": "weeks"}, "weeks", "v2"),
                         "REFUSAL_UNHELPFUL")


if __name__ == "__main__":
    unittest.main()
