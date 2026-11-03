"""Ajoute une entrée search_log à une question déjà retenue : add_search.py A-004 < entree.json"""
import json, sys
from pathlib import Path
p = Path(__file__).resolve().parent.parent / "data" / "stratum_a.jsonl"
rid, entry = sys.argv[1], json.load(sys.stdin)
rows = [json.loads(l) for l in p.open()]
next(r for r in rows if r["id"] == rid)["search_log"].append(entry)
p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
print(rid, "+1 recherche")
