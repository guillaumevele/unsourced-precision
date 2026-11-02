"""Strate A : ordre de parcours des requêtes réelles (SPEC § 3, PREREG § 2).

Aucune question n'est rédigée. Les questions sont des requêtes Search Console
réelles, posées telles quelles. Ce script est commité AVANT toute recherche de
sources ; il ne fait que filtrer, dédoublonner et ordonner avec une graine fixe.

Entrées (privées, ignorées par git, sha256 dans NOTES.md) :
    data/private/site_a.json, data/private/site_b.json
    site_c est hors domaine : non lu.
Sortie (privée) :
    data/private/candidates_ordered.jsonl

Usage : .venv/bin/python scripts/select_queries.py
"""

import json
import random
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "data" / "private"
SITES = {"A": "site_a.json", "B": "site_b.json"}
SEED = 20261103

# La requête demande une durée, un délai ou un nombre (séances, jours…).
QUANTITY = re.compile(
    r"\b(combien de (temps|séances?|seances?|jours|semaines|mois|fois|injections?)"
    r"|durée|duree|dure\b|délai|delai|au bout de|après combien|apres combien"
    r"|tous les combien|en combien de temps"
    r"|temps de (récupération|recuperation|cicatrisation|guérison|guerison)"
    r"|convalescence)",
    re.I,
)
# Prix et remboursement : hors sujet.
PRICE = re.compile(r"co[uû]t|prix|tarif|rembours|€|euros?\b", re.I)
# Mots qui ne disent rien du sujet : une requête faite seulement de ces mots est écartée.
EMPTY_WORDS = set(
    "combien de du des le la les l un une en temps durée duree dure délai delai "
    "jours jour semaines semaine mois fois séances seances séance seance au bout "
    "après apres quand faut il ça ca ? est ce que pour".split()
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", text).strip()


def dedupe_key(text: str) -> str:
    return " ".join(sorted(set(normalize(text).split())))


def main() -> None:
    kept: dict[str, dict] = {}
    counts = {"lues": 0, "quantite": 0, "prix": 0, "vides": 0}
    for site, filename in SITES.items():
        for row in json.loads((PRIVATE / filename).read_text()):
            counts["lues"] += 1
            query = row["query"].strip()
            if not QUANTITY.search(query):
                continue
            counts["quantite"] += 1
            if PRICE.search(query):
                counts["prix"] += 1
                continue
            if set(normalize(query).split()) <= {normalize(w) for w in EMPTY_WORDS}:
                counts["vides"] += 1
                continue
            key = dedupe_key(query)
            candidate = {"query": query, "site": site, "impressions": row["impressions"]}
            best = kept.get(key)
            if best is None or (candidate["impressions"], candidate["query"]) > (best["impressions"], best["query"]):
                kept[key] = candidate

    ordered = sorted(kept.values(), key=lambda c: normalize(c["query"]))
    random.Random(SEED).shuffle(ordered)

    out = PRIVATE / "candidates_ordered.jsonl"
    with out.open("w") as f:
        for rank, c in enumerate(ordered, 1):
            f.write(json.dumps({"rank": rank, **c}, ensure_ascii=False) + "\n")
    print(counts, "| après dédoublonnage :", len(ordered), "|", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
