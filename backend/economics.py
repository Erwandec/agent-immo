# economics.py 

from backend.constants import *
from backend.dvf import get_weighted_price 

def compute_economics(data, vision, nlp):
    price = data["price"] 
    surface = data["surface"] 
    city = data["address"]["ville"] 
    lat = data["address"]["lat"] 
    lon = data["address"]["lng"] 

    # Frais 
    notary = price * NOTARY_RATE_OLD 
    agency = nlp.get("agency_fee", price * DEFAULT_AGENCY_RATE) 
    dossier = BANK_FILE_FEES 

    # Taxe foncière 
    tf_coeff = COMMUNAL_TF_COEFFICIENT.get(city, 20) 
    taxe_fonciere = nlp.get("taxe_fonciere", surface * tf_coeff) 
    tf_source = "Annonce" if "taxe_fonciere" in nlp else "DGFiP (data.gouv.fr)" 

    # Charges copro
    charges = nlp.get(
        "charges",
        surface * COPRO_OLD_RATE
    )
    charges_source = "Annonce" if "charges" in nlp else "Estimation immeuble ancien" 

    # Travaux 
    travaux = vision["travaux_total"] 
    travaux_detail = vision["detail"] 

    # DVF
    dvf_pm2 = get_weighted_price(lat, lon) or 8500 

    # Crédit
    credit_cost = CREDIT_MONTHLY * 12 * CREDIT_DURATION_YEARS 
    
    total_cost = price + notary + agency + dossier + travaux + credit_cost 
    
    return {
        "prix_m2_dvf": dvf_pm2, 
        "frais": {
            "notaire": notary,
            "agence": agency,
            "dossier": dossier 
        },
        "taxe_fonciere": { 
            "montant": taxe_fonciere,
            "source": tf_source 
        },
        "charges_copro": {
            "montant": charges,
            "source": charges_source
        },
        "travaux": {
            "total": travaux,
            "detail": travaux_detail,
            "ratios": RENOVATION_RATIOS 
        }, 
        "credit": {
            "mensualite": CREDIT_MONTHLY,
            "taux": CREDIT_RATE, 
            "duree": CREDIT_DURATION_YEARS,
            "cout_total": credit_cost,
            "source": "Moyenne marché bancaire France"
        },
        "cout_total": total_cost 
    }
