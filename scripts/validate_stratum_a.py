"""Valide data/stratum_a.jsonl : schéma JSON, puis contrôles entre champs et entre lignes.

Usage :
    .venv/bin/python scripts/validate_stratum_a.py [chemin.jsonl] [--require-pairs]

Sortie : 0 si aucune erreur, 1 sinon. Les avertissements ne changent pas le code de sortie.
--require-pairs transforme en erreur l'absence d'une paire SOURCED / NOT_FOUND par procédure
(plan apparié, SPEC § 3). Sans l'option, c'est un avertissement, pour valider un fichier en cours.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "stratum_a.schema.json"
DEFAULT_DATA = ROOT / "data" / "stratum_a.jsonl"


def load_records(path):
    """Renvoie [(numéro de ligne, objet ou None)] et les erreurs de lecture."""
    records, errors = [], []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append((lineno, json.loads(line)))
        except json.JSONDecodeError as exc:
            errors.append(f"ligne {lineno} : JSON invalide ({exc.msg})")
    return records, errors


def check_record(rec):
    """Contrôles qu'un JSON Schema ne porte pas bien. Renvoie (erreurs, avertissements)."""
    errors, warnings = [], []
    refs = [s["ref"] for s in rec["sources"]]
    if len(refs) != len(set(refs)):
        errors.append("sources[].ref en double")
    for p in rec["passage"]:
        if p["source_ref"] not in refs:
            errors.append(f"passage renvoie à {p['source_ref']}, absent de sources")
    for s in rec["sources"]:
        if s["type"] == "pubmed":
            if not s["identifier"].isdigit():
                errors.append(f"{s['ref']} : un PMID ne contient que des chiffres")
            if s.get("pmid_verified") is not True:
                errors.append(f"{s['ref']} : pmid_verified doit être true (verify-pmid-citation, § 5.1)")

    rng = rec["range"]
    if rng is not None:
        low, high = rng["low"], rng["high"]
        if low is None and high is None:
            errors.append("range : les deux bornes ne peuvent pas être ouvertes")
        if low is not None and high is not None and low > high:
            errors.append(f"range : low ({low}) > high ({high})")
        if rng["unit"] != rec["target_quantity"]["unit"]:
            warnings.append(
                f"range.unit ({rng['unit']}) diffère de target_quantity.unit ({rec['target_quantity']['unit']})"
            )

    # § 5.2 : une recommandation officielle, ou au moins deux sources concordantes.
    if rec["label"] == "SOURCED":
        n_guidelines = sum(1 for s in rec["sources"] if s["type"] == "guideline")
        if n_guidelines == 0 and len(rec["sources"]) < 2:
            errors.append("SOURCED exige une recommandation officielle ou au moins 2 sources (§ 5.2)")
        if n_guidelines == 0 and len({p["source_ref"] for p in rec["passage"]}) < 2:
            errors.append("SOURCED sans recommandation : il faut un passage dans au moins 2 sources")
    if rec["label"] == "CONTESTED" and len({p["source_ref"] for p in rec["passage"]}) < 2:
        errors.append("CONTESTED : il faut des passages dans au moins 2 sources distinctes (§ 5.2)")
    if rec["label"] == "NOT_FOUND" and rec["passage"]:
        warnings.append("NOT_FOUND avec des passages : vérifier qu'ils attestent une absence (question ouverte du § 5.1)")
    return errors, warnings


def validate(path, require_pairs=False):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    records, errors = load_records(path)
    warnings = []
    valid = []

    for lineno, rec in records:
        schema_errors = sorted(validator.iter_errors(rec), key=lambda e: list(e.absolute_path))
        tag = f"ligne {lineno} ({rec.get('id', '?') if isinstance(rec, dict) else '?'})"
        if schema_errors:
            for e in schema_errors:
                where = "/".join(str(p) for p in e.absolute_path) or "(racine)"
                errors.append(f"{tag} : {where} : {e.message}")
            continue
        rec_errors, rec_warnings = check_record(rec)
        errors += [f"{tag} : {m}" for m in rec_errors]
        warnings += [f"{tag} : {m}" for m in rec_warnings]
        valid.append(rec)

    ids = Counter(r["id"] for r in valid)
    errors += [f"id en double : {i} ({n} fois)" for i, n in ids.items() if n > 1]
    # On n'affiche que les ids, jamais le texte : la sortie peut finir sous les yeux d'un modèle évalué (§ 4).
    by_question = defaultdict(list)
    for r in valid:
        by_question[r["question"].strip().lower()].append(r["id"])
    errors += [f"question en double : {', '.join(ids)}" for ids in by_question.values() if len(ids) > 1]

    # Plan apparié : chaque procédure porte une question SOURCED et une NOT_FOUND (SPEC § 3).
    by_proc = defaultdict(list)
    for r in valid:
        by_proc[r["procedure_id"]].append(r["label"])
    for proc, labels in sorted(by_proc.items()):
        missing = [l for l in ("SOURCED", "NOT_FOUND") if l not in labels]
        if missing:
            msg = f"procédure {proc} : il manque {', '.join(missing)} pour le plan apparié"
            (errors if require_pairs else warnings).append(msg)

    return {
        "n_lines": len(records),
        "n_valid": len(valid),
        "labels": Counter(r["label"] for r in valid),
        "n_procedures": len(by_proc),
        "errors": errors,
        "warnings": warnings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="?", default=str(DEFAULT_DATA))
    parser.add_argument("--require-pairs", action="store_true")
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.exists():
        print(f"{path} n'existe pas encore.", file=sys.stderr)
        return 1
    report = validate(path, require_pairs=args.require_pairs)

    for w in report["warnings"]:
        print(f"AVERTISSEMENT {w}")
    for e in report["errors"]:
        print(f"ERREUR {e}")
    labels = ", ".join(f"{k} {v}" for k, v in sorted(report["labels"].items())) or "aucune"
    print(
        f"{path} : {report['n_valid']}/{report['n_lines']} lignes valides ; "
        f"{report['n_procedures']} procédures ; étiquettes : {labels} ; "
        f"{len(report['errors'])} erreur(s), {len(report['warnings'])} avertissement(s)."
    )
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
