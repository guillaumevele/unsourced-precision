"""Annotation des réponses de la strate A par deux modèles d'autres familles (PREREG § 6, ANNOTATION.md).

Lit les journaux Inspect de logs/<split>/, extrait le texte visible de chaque tirage, mélange
les réponses de tous les modèles avec la graine 20261105, puis les envoie par lots de 20 à
chaque annotateur, avec la consigne figée data/annotation/prompt.md. L'annotateur ne voit
ni le modèle ni l'étiquette. Température 0, sans outils.

Sorties :
    data/annotation/<split>/items.jsonl            correspondance élément -> journal (modèle, id, tirage)
    data/annotation/<split>/<annotateur>/lot_NN.json   réponse brute de l'API
    data/annotation/<split>/<annotateur>.jsonl     champs extraits, un objet par élément

Clés : variables MISTRAL_API_KEY et ZHIPU_API_KEY, sinon lues dans --env-file (jamais écrites).
Usage : .venv/bin/python scripts/annotate.py dev [--only mistral|glm] [--max-batches N]
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED, BATCH = 20261105, 20
ANNOTATORS = {
    "mistral": {"url": "https://api.mistral.ai/v1/chat/completions", "key": "MISTRAL_API_KEY",
                "model": "mistral-large-4", "extra": {"reasoning_effort": "low"}},
    "glm": {"url": "https://open.bigmodel.cn/api/paas/v4/chat/completions", "key": "ZHIPU_API_KEY",
            "model": "glm-5.3", "extra": {"reasoning_effort": "low"}},
}

def read_key(name, env_file):
    if os.environ.get(name):
        return os.environ[name]
    for line in Path(env_file).expanduser().read_text(errors="ignore").splitlines():
        m = re.match(rf"\s*(?:export\s+)?{name}\s*=\s*(.*)", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit(f"clé {name} introuvable")


def load_items(split):
    from inspect_ai.log import read_eval_log

    questions = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data" / "stratum_a.jsonl").open()}
    items = []
    for log_path in sorted((ROOT / "logs" / split).glob("*.eval")):
        log = read_eval_log(str(log_path))
        model = log.eval.model
        for s in log.samples:
            choice = s.output.choices[0]
            q = questions[s.id]
            key = f"{model}|{s.id}|{s.epoch}"
            items.append({
                "item": hashlib.sha256(key.encode()).hexdigest()[:12],
                "model": model, "question_id": s.id, "epoch": s.epoch, "log": log_path.name,
                "stop_reason": choice.stop_reason,
                "query": q["question"], "target": q["target_quantity"]["description"],
                "unit": q["target_quantity"]["unit"], "response": choice.message.text,
            })
    items.sort(key=lambda x: x["item"])
    random.Random(SEED).shuffle(items)
    return items


def call(annotator, key, prompt, batch):
    payload = [{"id": it["item"], "requete": it["query"], "quantite_visee": it["target"],
                "unite": it["unit"], "reponse": it["response"]} for it in batch]
    body = {"model": annotator["model"], "temperature": 0, "top_p": 1, "max_tokens": 16000,
            "messages": [{"role": "user", "content": prompt + "\n\nLot :\n" + json.dumps(payload, ensure_ascii=False)}],
            **annotator["extra"]}
    for attempt in range(6):
        req = urllib.request.Request(annotator["url"], data=json.dumps(body).encode(),
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
                                              "User-Agent": "unsourced-precision"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = float(e.headers.get("retry-after") or 20 * (attempt + 1))
                print(f"  HTTP {e.code}, nouvel essai dans {wait:.0f} s", flush=True)
                time.sleep(wait)
                continue
            sys.exit(f"HTTP {e.code} : {e.read().decode()[:300]}")
    sys.exit("échec après 6 essais")


def parse(raw):
    content = raw["choices"][0]["message"]["content"]
    text = content if isinstance(content, str) else "".join(
        p.get("text", "") for p in content if p.get("type") == "text")
    return json.loads(text[text.index("["): text.rindex("]") + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("split", choices=["dev", "test"])
    ap.add_argument("--only", choices=list(ANNOTATORS))
    ap.add_argument("--max-batches", type=int)
    ap.add_argument("--env-file", default="~/.hermes/.env")
    a = ap.parse_args()
    out = ROOT / "data" / "annotation" / a.split
    out.mkdir(parents=True, exist_ok=True)
    items = load_items(a.split)
    (out / "items.jsonl").write_text("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in items))
    prompt = (ROOT / "data" / "annotation" / "prompt.md").read_text()
    batches = [items[i:i + BATCH] for i in range(0, len(items), BATCH)][: a.max_batches]
    for name, ann in ANNOTATORS.items():
        if a.only and name != a.only:
            continue
        key = read_key(ann["key"], a.env_file)
        (out / name).mkdir(exist_ok=True)
        rows = []
        for n, batch in enumerate(batches, 1):
            raw_path = out / name / f"lot_{n:02d}.json"
            ids = [it["item"] for it in batch]
            for attempt in range(3):
                raw = json.loads(raw_path.read_text()) if raw_path.exists() else call(ann, key, prompt, batch)
                raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=1))
                try:
                    got = parse(raw)
                    ok = [g.get("id") for g in got] == ids
                except (ValueError, KeyError):
                    got, ok = [], False
                if ok:
                    break
                # Lot incomplet ou illisible : conservé comme rejeté, puis redemandé tel quel.
                rej = out / "essais_rejetes"
                rej.mkdir(exist_ok=True)
                raw_path.rename(rej / f"{name}_lot_{n:02d}_essai_{attempt + 1}.json")
                print(f"  {name} lot {n} rejeté ({len(got)} éléments lisibles pour {len(ids)}), nouvel essai", flush=True)
            else:
                sys.exit(f"{name} lot {n} : toujours incomplet après 3 essais")
            rows += got
            print(f"{name} lot {n}/{len(batches)} : {len(got)} éléments ({raw.get('model')})", flush=True)
        (out / f"{name}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


if __name__ == "__main__":
    main()
