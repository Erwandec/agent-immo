# backend/analysis.py
"""
Analyse principale du moteur d'investissement immobilier.

Inclut :
- Étape A : exclusions structurelles (résidences gérées, bail commercial)
- Appel DVF multi-sorties (sans inférence de typologie)
"""

from backend.scoring import score_opportunite, score_achat_revente
from backend.economics import compute_economics
from backend.dvf import get_dvf_multi_output


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
        "pas d'occupation personnelle",
    ]

    for keyword in exclusions:
        if keyword in text:
            return {
                "type": "Résidence gérée à bail commercial",
                "raison": "Produit de rendement sans levier, revente contrainte et usage interdit",
            }

    return None


def analyze(data: dict, nlp: dict, vision: dict):
    description = data.get("description", "")

    # === ÉTAPE A : EXCLUSION IMMÉDIATE ===
    exclusion = detect_exclusion(description)
    if exclusion:
        return {
            "scores": {
                "opportunite": 0,
                "achat_revente": 0,
            },
            "exclusion": exclusion,
        }

    # === ANALYSE ÉCONOMIQUE ===
    economics = compute_economics(data, vision, nlp)

    # === DVF MULTI-SORTIES ===
    lat = data["address"]["lat"]
    lon = data["address"]["lng"]

    economics["dvf"] = get_dvf_multi_output(lat, lon)

    # === SCORING ===
    score_oppo = score_opportunite(data, economics, vision)
    score_ar = score_achat_revente(data, economics)

    return {
        "scores": {
            "opportunite": score_oppo,
            "achat_revente": score_ar,
        },
        "economics": economics,
    }
