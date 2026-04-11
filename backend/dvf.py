# dvf.py 

import math
import requests 
from datetime import datetime 

def haversine(lat1, lon1, lat2, lon2):
  R = 6371000 
  phi1, phi2 = math.radians(lat1), math.radians(lat2) 
  dphi = math.radians(lat2 - lat1) 
  dlambda = math.radians(lon2 - lon1) 
  a = math.sin(dphi/2)**2 + math.cos(phi1)math.cos(phi2)math.sin(dlambda/2)**2 
  return 2Rmath.atan2(math.sqrt(a), math.sqrt(1-a)) 
  
def date_weight(date_str): 
  delta = (datetime.now() - datetime.strptime(date_str, "%Y-%m-%d")).days 
  if delta < 180: return 1 
  if delta < 365: return 0.7 
  if delta < 730: return 0.5
  return 0.3

def inflation_adjust(price, years, inflation_rate=0.02): 
  return price * ((1 + inflation_rate) ** years) 
  
def get_weighted_price(lat, lon, radius=200):
    url = f"https://api.cquest.org/dvf?lat={lat}&lon={lon}&dist={radius}" 
    data = requests.get(url).json().get("resultats", []) 
    
    weighted = [] 
    for v in data:
      if not v.get("surface_reelle_bati") or not v.get("valeur_fonciere"): 
        continue 
      
      pm2 = v["valeur_fonciere"] / v["surface_reelle_bati"] 
      dist = haversine(lat, lon, v["lat"], v["lon"]) 
      w_dist = max(0.1, 1 - dist / radius) 
      w_date = date_weight(v["date_mutation"]) 
      year = int(v["date_mutation"][:4]) 
      pm2_adj = inflation_adjust(pm2, datetime.now().year - year) 
      
weighted.append((pm2_adj, w_dist * w_date)) 

  if not weighted: 
    return None 
    
    return sum(p*w for p,w in weighted) / sum(w for _,w in weighted)
