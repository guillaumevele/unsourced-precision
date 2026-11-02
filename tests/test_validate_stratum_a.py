"""Tests du validateur sur des fixtures synthétiques (aucun contenu clinique).

Lancer : .venv/bin/python -m unittest discover -s tests -v
"""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_stratum_a import validate  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "stratum_a_valid.jsonl"


def load_fixture():
    return [json.loads(l) for l in FIXTURE.read_text(encoding="utf-8").splitlines() if l.strip()]


def run(records, **kwargs):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    return validate(Path(f.name), **kwargs)


class ValidFixture(unittest.TestCase):
    def test_fixture_passes(self):
        report = run(load_fixture())
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["n_valid"], 3)

    def test_unpaired_procedure_is_warning_then_error(self):
        self.assertTrue(any("plan apparié" in w for w in run(load_fixture())["warnings"]))
        strict = run(load_fixture(), require_pairs=True)
        self.assertTrue(any("plan apparié" in e for e in strict["errors"]))


class Rejections(unittest.TestCase):
    """Chaque cas casse une seule règle et doit produire au moins une erreur."""

    def assertRejected(self, mutate, needle):
        recs = load_fixture()
        mutate(recs)
        errors = run(recs)["errors"]
        self.assertTrue(any(needle in e for e in errors), f"attendu « {needle} » dans {errors}")

    def test_llm_drafted_true(self):
        self.assertRejected(lambda r: r[0].update(llm_drafted=True), "llm_drafted")

    def test_provenance_missing(self):
        self.assertRejected(lambda r: r[0].pop("provenance"), "provenance")

    def test_lang_english_rejected(self):
        self.assertRejected(lambda r: r[0].update(lang="en"), "lang")

    def test_not_found_with_range(self):
        self.assertRejected(lambda r: r[1].update(range={"low": 1, "high": 2, "unit": "u"}), "range")

    def test_sourced_without_range(self):
        self.assertRejected(lambda r: r[0].update(range=None), "range")

    def test_sourced_without_passage(self):
        self.assertRejected(lambda r: r[0].update(passage=[]), "passage")

    def test_contested_needs_two_sources(self):
        def m(r):
            r[2]["sources"] = r[2]["sources"][:1]
            r[2]["passage"] = r[2]["passage"][:1]
        self.assertRejected(m, "sources")

    def test_contested_passages_from_one_source(self):
        self.assertRejected(lambda r: r[2]["passage"][1].update(source_ref="S1"), "CONTESTED")

    def test_empty_search_log(self):
        self.assertRejected(lambda r: r[1].update(search_log=[]), "search_log")

    def test_passage_points_to_unknown_source(self):
        self.assertRejected(lambda r: r[0]["passage"][0].update(source_ref="S9"), "absent de sources")

    def test_unverified_pmid(self):
        self.assertRejected(lambda r: r[2]["sources"][0].update(pmid_verified=False), "pmid_verified")

    def test_non_numeric_pmid(self):
        self.assertRejected(lambda r: r[2]["sources"][0].update(identifier="PMC123"), "PMID")

    def test_inverted_range(self):
        self.assertRejected(lambda r: r[0]["range"].update(low=5, high=1), "low")

    def test_both_bounds_open(self):
        self.assertRejected(lambda r: r[0]["range"].update(low=None, high=None), "ouvertes")

    def test_sourced_single_non_guideline_source(self):
        def m(r):
            r[0]["sources"][0].update(type="pubmed", identifier="00000003", pmid_verified=True)
        self.assertRejected(m, "§ 5.2")

    def test_duplicate_id(self):
        self.assertRejected(lambda r: r[1].update(id="A-001"), "id en double")

    def test_duplicate_question(self):
        self.assertRejected(lambda r: r[1].update(question=r[0]["question"]), "question en double")

    def test_bad_date(self):
        self.assertRejected(lambda r: r[0]["search_log"][0].update(date="02/11/2026"), "date")

    def test_unknown_field(self):
        self.assertRejected(lambda r: r[0].update(extra=1), "extra")


if __name__ == "__main__":
    unittest.main()
