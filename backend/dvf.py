# dvf.py
"""
DVF FINAL – Sans inférence de typologie

Règles :
- Rayon <= 200 m
- Mutation exploitable si surface + valeur foncière
- Typologie utilisée uniquement si explicitement fournie par DVF
- Typologie absente => NC (Non Communiqué)
"""

import math
import requests
import logging

logger = logging.getLogger(__name__)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


PIECES_MAP = {
    1: "Studio",
    2: "T2",
    3: "T3",
    4: "T4+"
}


def get_dvf_multi_output(lat, lon, radius=200):
    url = f"https://api.cquest.org/dvf?lat={lat}&lon={lon}&dist={radius}"

    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return {
            "rayon_m": radius,
            "mutations": [],
            "statistiques_par_typologie": {},
            "conclusion": {
                "comparables_directs": False,
                "commentaire": "DVF indisponible ou erreur réseau"
            }
        }

    raw = data.get("resultats", [])
    mutations = []
    stats = {}

    for v in raw:
        surface = v.get("surface_reelle_bati") or v.get("surface_reelle_batie")
        valeur = v.get("valeur_fonciere")
        lat_v = v.get("lat")
        lon_v = v.get("lon")

        if not surface or not valeur or not lat_v or not lon_v:
            continue

        distance = haversine(lat, lon, lat_v, lon_v)
        if distance > radius:
            continue

        pieces = v.get("nombre_pieces_principales")
        if pieces in PIECES_MAP:
            typologie = PIECES_MAP[pieces]
            typologie_source = "DVF"
        else:
            typologie = "NC"
            typologie_source = "Non communiquée"

        prix_m2 = valeur / surface

        mutations.append({
            "date": v.get("date_mutation"),
            "surface_m2": surface,
            "prix": valeur,
            "prix_m2": round(prix_m2, 0),
            "pieces": pieces,
            "typologie": typologie,
            "typologie_source": typologie_source,
            "distance_m": round(distance)
        })

        if typologie != "NC":
            entry = stats.setdefault(typologie, {"nb": 0, "total": 0})
            entry["nb"] += 1
            entry["total"] += prix_m2

    statistiques = {
        t: {
            "nb_ventes": s["nb"],
            "prix_m2_moyen": round(s["total"] / s["nb"], 0)
        }
        for t, s in stats.items()
    }
    logger.info(f"[DVF] Nombre de mutations brutes : {len(raw)}")
    logger.info(f"[DVF] Exemples mutations brutes : {raw[:3]}")
    return {
        "rayon_m": radius,
        "mutations": mutations,
        "statistiques_par_typologie": statistiques,
        "conclusion": {
            "comparables_directs": False,
            "commentaire": "Analyse DVF fournie sans inférence de typologie"
        }
    
    }
