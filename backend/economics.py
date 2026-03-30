def compute_economics(price,surface,travaux,ville):
    loyers={'Montrouge':32,'Paris':39,'Gentilly':28,'Arcueil':26}
    loyer_annuel=surface*loyers.get(ville,28)*12
    taxe=surface*20
    charges=40*12
    total=price+travaux
    rendement=(loyer_annuel-taxe-charges)/total
    prix_m2={'Paris':10500,'Montrouge':8500,'Gentilly':7000,'Arcueil':6000}.get(ville,7500)
    return {'loyer_potentiel':loyer_annuel,'taxe_fonciere':taxe,'charges_annuelles':charges,'rendement_net':rendement,'prix_m2_marche':prix_m2}
