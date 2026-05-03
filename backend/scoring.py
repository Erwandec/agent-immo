# scoring.py 

def score_opportunite(data, eco, vision):
    pm2_announce = data["price"] / data["surface"]
    ratio = eco["prix_m2_dvf"] / pm2_announce

    score_prix = min(40, max(0, 40 * ratio))

    # 🔒 Sécurisation Vision
    vision_score = vision.get("travaux_vision_score", 0)
    score_travaux = 20 * (1 - vision_score)

    score_dist = 15
    score_credit = 20 if eco["credit"]["mensualite"] < 1000 else 0

    penalty_neuf = -50 if data.get("is_new") else 0

    total = score_prix + score_travaux + score_dist + score_credit + penalty_neuf
    return max(0, round(total, 1))
    
def score_achat_revente(eco, dvf_price):
    value = dvf_price * eco["surface"] 
    margin = value - eco["cout_total"] 
    
    if margin <= 0:
        return 0
        
        return min(100, (margin / eco["cout_total"]) * 200)
