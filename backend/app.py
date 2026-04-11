from flask import Flask, request, jsonify

from analysis import analyze 

app = Flask(name)

@app.route("/health", methods=["GET"]) 
def health():
    return jsonify({"status": "ok"}), 200
    
@app.route("/analyze", methods=["POST"]) 
def analyze_route(): 
    data = request.get_json(force=True) 

    # Ces champs sont obligatoires 
    required_fields = ["price", "surface", "description", "address"] 
    for field in required_fields: 
        if field not in data: 
            return jsonify({"error": f"Missing field: {field}"}), 400 

    # Sécurisation des sous‑champs d’adresse 
    address = data.get("address", {}) 
    if not all(k in address for k in ["lat", "lng", "ville"]):
        return jsonify({"error": "Address must include lat, lng, ville"}), 400 
        
    try:
        # Le moteur principal 
        result = analyze( 
            data=data, 
            nlp=data.get("nlp", {}),
            vision=data.get("vision", {}) 
        )
        return jsonify(result), 200 
    
    except Exception as e:
        # En prod, on loguerait mieux 
        return jsonify({"error": str(e)}), 500 
        
        
if name == "main":
    app.run(host="0.0.0.0", port=10000)
