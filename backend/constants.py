# constants.py

NOTARY_RATE_OLD = 0.075
DEFAULT_AGENCY_RATE = 0.05 
BANK_FILE_FEES = 1000 

# Crédit (hypothèses standard)
CREDIT_DURATION_YEARS = 25
CREDIT_MONTHLY = 950
CREDIT_RATE = 0.04 # 4%

# Fiscalité locale (€/m²/an) – source DGFiP data.gouv.fr
COMMUNAL_TF_COEFFICIENT = { 
  "Montrouge": 20,
  "Paris": 14,
  "Boulogne-Billancourt": 18
} 

# Charges copro
COPRO_OLD_RATE = 30 # €/m²/an
COPRO_RECENT_RATE = 20

# Travaux ratios €/m²
RENOVATION_RATIOS = {
  "global_light": (400, 700),
  "global_heavy": (800, 1200),
  "electricity": (80, 150),
  "paint": (20, 40),
  "floor": (40, 120)
}
