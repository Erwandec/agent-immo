def compute_score(pm2a,pm2m,tv,dist,rend):
    score_prix=max(0,min(40,40*(pm2m/pm2a)))
    score_travaux=20*(1-tv)
    score_distance=15 if dist<=30 else max(0,15*(1-(dist-30)/30))
    score_rend=min(20,20*rend*10)
    return score_prix+score_travaux+score_distance+score_rend+5
