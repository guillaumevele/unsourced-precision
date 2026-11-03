"""Pilote : extraction des activations de Qwen2.5-1.5B-Instruct sur les 49 questions SOURCED et NOT_FOUND
(PREREG-AMENDEMENT-4.md). Hors CI : demande torch, transformers et le modèle (3,09 Go).

Règles fixées avant toute donnée :
- Gabarit de chat du modèle, un seul message utilisateur = la requête telle quelle ; le prompt système par
  défaut que le gabarit insère est gardé (usage normal du modèle) ; add_generation_prompt=True.
- Position : dernier token du prompt (après le marqueur de génération de l'assistant), toutes les couches
  (sortie des plongements + 28 couches). Témoin lexical : moyenne de la couche 0 sur les tokens de la requête.
- CPU, float32, sans échantillonnage (aucune génération). Sauvegarde en float16.

Usage (caches sur le SSD) :
  HF_HOME=... python pilot/extract.py --revision <sha>        ->  pilot/activations.npz, pilot/activations.json
  python pilot/extract.py --smoke --revision <sha>            ->  essai sur deux phrases synthétiques, rien d'écrit
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parent.parent
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"


def encode(tok, query):
    prompt = tok.apply_chat_template([{"role": "user", "content": query}], tokenize=False, add_generation_prompt=True)
    ids = tok(prompt, return_tensors="pt").input_ids
    q_ids = tok(query, add_special_tokens=False).input_ids
    # position de la requête dans le prompt : dernière occurrence de sa suite de tokens
    seq, n = ids[0].tolist(), len(q_ids)
    start = max(i for i in range(len(seq) - n + 1) if seq[i:i + n] == q_ids)
    return prompt, ids, start, start + n


@torch.no_grad()
def activations(model, tok, query):
    prompt, ids, s, e = encode(tok, query)
    hs = model(ids, output_hidden_states=True).hidden_states       # (couches + 1) × [1, T, d]
    last = torch.stack([h[0, -1] for h in hs]).numpy()               # [29, d]
    embmean = hs[0][0, s:e].mean(0).numpy()                          # [d]
    return prompt, last, embmean


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revision", required=True)
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True)
    tok = AutoTokenizer.from_pretrained(MODEL, revision=a.revision)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=a.revision, torch_dtype=torch.float32).eval()
    if a.smoke:
        for q in ["Combien de temps dure un trajet en train de Paris à Lyon ?", "Quelle est la couleur du ciel ?"]:
            prompt, last, emb = activations(model, tok, q)
            print(repr(prompt[-80:]), last.shape, emb.shape, float(np.abs(last).mean()))
        return
    split = None  # toutes les questions SOURCED et NOT_FOUND, dev et test confondus (amendement 4)
    rows = [json.loads(l) for l in (ROOT / "data" / "stratum_a.jsonl").open()]
    rows = [r for r in rows if r["label"] in ("SOURCED", "NOT_FOUND")]
    L, E, prompts = [], [], []
    for r in rows:
        prompt, last, emb = activations(model, tok, r["question"])
        L.append(last), E.append(emb), prompts.append(prompt)
    for A in (L, E):
        A = np.asarray(A, dtype=np.float32)
        assert np.isfinite(A).all() and np.abs(A).max() < 65000, "activation non finie ou hors de la plage float16"
    np.savez_compressed(ROOT / "pilot" / "activations.npz",
                        last=np.array(L, dtype=np.float16), embmean=np.array(E, dtype=np.float16),
                        y=np.array([r["label"] == "SOURCED" for r in rows], dtype=np.int8),
                        groups=np.array([r["procedure_id"] for r in rows]), ids=np.array([r["id"] for r in rows]),
                        questions=np.array([r["question"] for r in rows]))
    meta = {"model": MODEL, "revision": a.revision, "split": split, "n": len(rows),
            "couches": len(L[0]), "dimension": int(L[0].shape[1]),
            "torch": torch.__version__, "transformers": transformers.__version__,
            "gabarit_sha256": hashlib.sha256(prompts[0].replace(rows[0]["question"], "{q}").encode()).hexdigest()}
    (ROOT / "pilot" / "activations.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
