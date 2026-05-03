# dvf.py 

import math
import requests
from datetime import datetime


def haversine(lat1, lon1, lat2, lon2):
    """Distance entre deux points GPS en mÃ¨tres (formule de Haversine)"""
    R = 6_371_000

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def date_weight(date_str):
    """PondÃ©ration selon la rÃ©cence de la vente"""
    delta_days = (datetime.now() - datetime.strptime(date_str, "%Y-%m-%d")).days

    if delta_days < 180:
        return 1.0
    if delta_days < 365:
        return 0.7
    if delta_days < 730:
        return 0.5
    return 0.3


def inflation_adjust(price_m2, years, inflation_rate=0.02):
    """Ajustement du prix par inflation annuelle moyenne"""
    return price_m2 * (1 + inflation_rate) ** years


def get_weighted_price(lat, lon, radius=200):
    """Prix au mÂ² DVF pondÃ©rÃ© par distance, date et inflation"""
    url = f"https://api.cquest.org/dvf?lat={lat}&lon={lon}&dist={radius}"
    response = requests.get(url, timeout=10)
    ventes = response.json().get("resultats", [])

    valeurs = []

    for v in ventes:
        surface = v.get("surface_reelle_bati") or v.get("surface_reelle_batie")
        valeur = v.get("valeur_fonciere")

        if not surface or not valeur:
            continue

        prix_m2 = valeur / surface

        dist = haversine(lat, lon, v["lat"], v["lon"])
        w_dist = max(0.1, 1 - dist / radius)
        w_date = date_weight(v["date_mutation"])

        year = int(v["date_mutation"][:4])
        prix_m2_adj = inflation_adjust(prix_m2, datetime.now().year - year)

        poids = w_dist * w_date
        valeurs.append((prix_m2_adj, poids))

    if not valeurs:
        return None

    return sum(v * w for v, w in valeurs) / sum(w for _, w in valeurs)
