# analysis.py

from economics import compute_economics 
from scoring import score_opportunite, score_achat_revente 

def analyze(data, nlp, vision): 
    eco = compute_economics(data, vision, nlp) 

    score_opp = score_opportunite(data, eco, vision) 
    score_ar = score_achat_revente(eco, eco["prix_m2_dvf"]) 
    
    return {
        "scores": {
            "opportunite": round(score_opp, 1),
            "achat_revente": round(score_ar, 1) 
        },
        "economics": eco
    }
