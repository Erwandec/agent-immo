import requests, os
def compute_drive_time(addr):
 api=os.getenv('ORS_API_KEY')
 r=requests.post('https://api.openrouteservice.org/v2/matrix/driving-car',json={'locations':[[addr['lng'],addr['lat']],[2.319,48.817]],'metrics':['duration']},headers={'Authorization':api})
 sec=r.json()['durations'][0][1]
 return sec/60
