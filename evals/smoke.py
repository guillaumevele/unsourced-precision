"""Test de fumée du banc : deux échantillons factices, fournisseur mockllm.

Aucun contenu clinique ici. Les échantillons sont des marqueurs (§ 4 de la SPEC :
aucun LLM ne rédige les questions). Ce fichier vérifie seulement que la chaîne
Inspect tourne sans appeler de vrai modèle.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.scorer import includes
from inspect_ai.solver import generate


@task
def smoke() -> Task:
    return Task(
        dataset=MemoryDataset(
            [
                Sample(id="placeholder-1", input="PLACEHOLDER 1", target="mockllm"),
                Sample(id="placeholder-2", input="PLACEHOLDER 2", target="mockllm"),
            ],
            name="smoke-placeholders",
        ),
        solver=generate(),
        scorer=includes(),
    )
