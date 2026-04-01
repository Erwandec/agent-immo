from flask import Flask, request, jsonify
from backend.analysis import analyze_text, analyze_photos
from backend.economics import compute_economics
from backend.scoring import compute_score
from backend.utils.distance import compute_drive_time

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    
    text = data.get('description','')
    photos = data.get('photos',[])
    price = data.get('price',0)
    surface = data.get('surface',0)
    address = data.get('address',{})
    nlp = analyze_text(text)
    try:
        vision = analyze_photos(photos)
        if not isinstance(vision,dict):
            raise Exception("Vision returned invalid format")
    except Exception as e:
        print(" Vision fallback:",e)
        vision={"travaux_total":0,
                "travaux_vision_score":0
        }
    try:
        distance = compute_drive_time(address)
    except:
        distance=999
    travaux=vision.get("travaux_total",0)
    
    economics = compute_economics(price=price, 
                                  surface=surface,
                                  travaux=travaux,
                                  ville=address.get('ville','Paris'))
    score = compute_score(
        prix_m2_annonce=price/surface if surface else 99999,
        prix_m2_marche=economics["prix_m2_marche"], 
        travaux_score=vision.get("travaux_vision_score",0),
        distance=distance,
        rendement=economics["rendement_net"])
    return jsonify({"nlp":nlp,"vision":vision,"distance":distance,"economics":economics,"score":score})

if __name__=='__main__': app.run(debug=True)
