# Tarifs relevés le 03/11/2026 : platform.claude.com/docs/en/about-claude/pricing
# et developers.openai.com/api/docs/pricing ($ par million de tokens, entrée / sortie)
P = {"claude-opus-5-5": (4, 20), "claude-sonnet-5-5": (2, 10),
     "gpt-6-astra": (10, 50), "claude-haiku-5-5": (0.10, 0.50)}

# Hypothèses volontairement pessimistes (sortie = réponse + raisonnement facturé)
Q, K = 60, 5
runs = {
  "Q1 test":              dict(calls=Q*K,       tin=400,  tout=2000),
  "Q1 dev (paraphrases)": dict(calls=12*3*K,    tin=400,  tout=2000),
  "Q2 sondes (3 témoins x ~3 chiffres)": dict(calls=Q*K*3*3, tin=1200, tout=1000),
}
def cost(m, r): pi, po = P[m]; return r["calls"]*(r["tin"]*pi + r["tout"]*po)/1e6

import sys
MODELS = sys.argv[1:] or ["claude-opus-5-5", "claude-sonnet-5-5", "gpt-6-astra"]
for m in MODELS:
    q1 = cost(m, runs["Q1 test"]) + cost(m, runs["Q1 dev (paraphrases)"])
    q2 = cost(m, runs["Q2 sondes (3 témoins x ~3 chiffres)"])
    print(f"{m:20s} Q1 {q1:7.2f} $   Q2 {q2:7.2f} $   total {q1+q2:7.2f} $")
tot = sum(cost(m, r) for m in MODELS for r in runs.values())
print(f"\n{len(MODELS)} modèles, Q1+Q2, une passe : {tot:.0f} $ ; avec marge x2 (relances, bugs) : {2*tot:.0f} $")
print(f"Mêmes appels via Batch API (-50 %) : {tot/2:.0f} $ ; avec marge x2 : {tot:.0f} $")
print("Appels par modèle :", {k: v['calls'] for k, v in runs.items()})
