# analysis.py

from backend.economics import compute_economics 
from backend.scoring import score_opportunite, score_achat_revente 

def analyze(data, nlp, vision):

    # ✅ Normalisation VISION si absente
    if not isinstance(vision, dict) or not vision:
        vision = {
            "travaux_total": 0,
            "travaux_vision_score": 0.0,
            "detail": []
        }

    # ✅ Normalisation NLP si absent
    if not isinstance(nlp, dict):
        nlp = {}

    eco = compute_economics(data, vision, nlp)

    score_opp = score_opportunite(data, eco, vision)
    score_ar = score_achat_revente(data, eco)

    return {
        "scores": {
            "opportunite": round(score_opp, 1),
            "achat_revente": round(score_ar, 1)
        },
        "economics": eco
    }
