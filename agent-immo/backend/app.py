from flask import Flask, request, jsonify
from analysis import analyze_text, analyze_photos
from economics import compute_economics
from scoring import compute_score
from utils.distance import compute_drive_time

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data['description']
    photos = data['photos']
    price = data['price']
    surface = data['surface']
    address = data['address']
    nlp = analyze_text(text)
    vision = analyze_photos(photos)
    distance = compute_drive_time(address)
    economics = compute_economics(price=price, surface=surface, travaux=vision['travaux_total'], ville=address.get('ville','Paris'))
    score = compute_score(price/surface, economics['prix_m2_marche'], vision['travaux_vision_score'], distance, economics['rendement_net'])
    return jsonify({'nlp':nlp,'vision':vision,'distance':distance,'economics':economics,'score':score})

if __name__=='__main__': app.run(debug=True)
