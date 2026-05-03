# backend/scoring.py
"""
Scoring refondu – compatible Étape A (exclusion) et Étape B (DVF diagnostic)

Le scoring ne dépend plus d'un prix DVF unique.
"""


def score_opportunite(data, eco, vision):
    score = 0

    # --- 1. Décote apparente (micro-surface prise en compte) ---
    pm2_annonce = data["price"] / data["surface"]

    if data["surface"] < 12:
        # micro-surface très contrainte
        score -= 10
    elif pm2_annonce < 8000:
        score += 20
    elif pm2_annonce < 9500:
        score += 10

    # --- 2. Potentiel travaux ---
    travaux_score = vision.get("travaux_vision_score", 0)

    if travaux_score > 0.5:
        score += 25
    elif travaux_score > 0.2:
        score += 15

    # --- 3. Faisabilité financière (contrainte, pas coût réel) ---
    mensualite = eco.get("credit", {}).get("mensualite", None)

    if mensualite is not None:
        if mensualite < 600:
            score += 20
        elif mensualite < 800:
            score += 10
        else:
            score -= 5

    # --- 4. Malus structurels ---
    if data["surface"] < 10:
        score -= 10

    dpe = vision.get("dpe", None)
    if dpe in ["F", "G"]:
        score -= 10

    # bornage final
    return max(0, min(100, round(score, 1)))


def score_achat_revente(data, eco, vision=None):
    """
    Score achat-revente :
    - n'existe que si travaux créateurs de valeur
    - sinon retourne 0 par design
    """

    travaux_score = vision.get("travaux_vision_score", 0) if vision else 0

    if travaux_score < 0.3:
        return 0

    surface = data["surface"]
    if surface < 12:
        return 0  # micro-surface non liquides en revente active

    # Placeholder : sera affiné à l'Étape C
    return 50
