# economics.py
import re
from backend.constants import COPRO_OLD_RATE, COMMUNAL_TF_COEFFICIENT, NOTARY_RATE_OLD, DEFAULT_AGENCY_RATE, BANK_FILE_FEES


def extract_charges_from_description(description: str):
    if not description:
        return None
    match = re.search(r"charges.*?(\d{2,5})\s*€", description.lower())
    return int(match.group(1)) if match else None


def extract_taxe_fonciere_from_description(description: str):
    if not description:
        return None
    match = re.search(r"taxe fonci[eè]re.*?(\d{2,5})\s*€", description.lower())
    return int(match.group(1)) if match else None


def compute_economics(data, vision, nlp):
    price = data["price"]
    surface = data["surface"]
    city = data["address"]["ville"]
    description = data.get("description", "")

    notary = price * NOTARY_RATE_OLD
    agency = price * DEFAULT_AGENCY_RATE
    dossier = BANK_FILE_FEES

    charges_annonce = extract_charges_from_description(description)
    if charges_annonce is not None:
        charges_copro = charges_annonce
        charges_source = "Annonce"
    else:
        charges_copro = surface * COPRO_OLD_RATE
        charges_source = "Estimation immeuble ancien"

    tf_annonce = extract_taxe_fonciere_from_description(description)
    if tf_annonce is not None:
        taxe_fonciere = tf_annonce
        tf_source = "Annonce"
    else:
        taxe_fonciere = surface * COMMUNAL_TF_COEFFICIENT.get(city, 20)
        tf_source = "DGFiP (data.gouv.fr)"

    return {
        "frais": {
            "notaire": notary,
            "agence": agency,
            "dossier": dossier
        },
        "charges_copro": {
            "montant": charges_copro,
            "source": charges_source
        },
        "taxe_fonciere": {
            "montant": taxe_fonciere,
            "source": tf_source
        }
    }
