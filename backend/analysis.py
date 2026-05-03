# analysis.py

def detect_exclusion(description: str):
    if not description:
        return None

    text = description.lower()
    exclusions = [
        "résidence étudiante",
        "résidence senior",
        "bail commercial",
        "gestion déléguée",
        "studéa",
        "nexity",
        "nemea",
        "espacil",
        "lmnp géré",
        "pas d'occupation personnelle"
    ]

    for keyword in exclusions:
        if keyword in text:
            return {
                "type": "Résidence gérée à bail commercial",
                "raison": "Produit de rendement sans levier, revente contrainte et usage interdit"
            }

    return None


def analyze(data, nlp, vision):
    description = data.get("description", "")

    exclusion = detect_exclusion(description)
    if exclusion:
        return {
            "scores": {
                "opportunite": 0,
                "achat_revente": 0
            },
            "exclusion": exclusion
        }

    from backend.economics import compute_economics
    from backend.scoring import score_opportunite, score_achat_revente

    eco = compute_economics(data, vision, nlp)

    score_opp = score_opportunite(data, eco, vision)
    score_ar = score_achat_revente(data, eco)

    return {
        "scores": {
            "opportunite": score_opp,
            "achat_revente": score_ar
        },
        "economics": eco
    }

from backend.dvf import get_dvf_multi_output

dvf_result = get_dvf_multi_output(
    data["address"]["lat"],
    data["address"]["lng"]
)

economics["dvf"] = dvf_result
