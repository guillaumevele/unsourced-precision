"""Annotation Gemini par Vertex AI au lieu de l'API Gemini (même modèle, même consigne, mêmes réglages).

annotate.py reste inchangé (empreinte dans timestamps/amendement-1.manifest.txt) : ce lanceur ne
remplace que l'adresse de l'appel Gemini et ajoute role: "user" exigé par Vertex, puis exécute annotate.main(). Raison : le 03/11/2026, la
clé gratuite a été remplacée par une clé de projet dont l'API Gemini répond HTTP 402 (crédits
prépayés épuisés) ; Vertex AI, même clé, répond (NOTES.md). Les lots déjà reçus sont relus du disque.

Usage : .venv/bin/python scripts/annotate_vertex.py test --version v2 --only gemini [--max-batches N]
"""

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import annotate  # noqa: E402

PROJECT, LOCATION = "726967596529", "global"
annotate.ANNOTATORS["gemini"]["url"] = (
    f"https://aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}"
    "/publishers/google/models/gemini-3.6-flash:generateContent")


class VertexRequest(urllib.request.Request):
    """Vertex AI exige role: "user" dans chaque contenu ; seul ajout au corps de la requête."""

    def __init__(self, url, data=None, *args, **kwargs):
        if data and "aiplatform.googleapis.com" in url:
            body = json.loads(data)
            for c in body.get("contents", []):
                c.setdefault("role", "user")
            data = json.dumps(body).encode()
        super().__init__(url, data, *args, **kwargs)


annotate.urllib.request.Request = VertexRequest

if __name__ == "__main__":
    annotate.main()
