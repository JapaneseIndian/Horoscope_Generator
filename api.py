from flask import Flask, request, jsonify
from datetime import datetime
import random as r
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
DATA_FILE = "horoscope_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"savedscope": [], "next_id": 1}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Zodiac data
zodiac = ["Aries","Taurus","Gemini","Cancer","Scorpio","Leo","Pisces","Libra","Virgo","Aquarius","Sagittarius","Capricorn"]

predictions = {
    "love": ["Venus aligns with your heart today", "An old flame may reappear","An unexpected compliment will make your day special","Your charm is at peak levels - someone's noticing your magnetic energy"],
    "career": ["Mercury brings good opportunities", "Avoid important decisions today","A bold move at work will pay off unexpectedly","Your creative ideas will impress superiors this week"],
    "health": ["Listen to your body's needs", "A walk in nature will help","Listen to your body's subtle signals - they're trying to tell you something","Hydration will be your secret weapon this week"],
    "social life":["An old friend will reappear with exciting news","Your natural charisma will shine at gatherings","Your social circle is about to expand in delightful ways","Group activities will bring unexpected joy this weekend"],
    "mind":["Meditation will reveal solutions to lingering problems","A book or podcast will spark an important epiphany","Journaling will help process complex emotions"]
}
@app.route('/horoscope', methods=['GET']) 
def horoscope():
    sign = request.args.get('sign')
    category = request.args.get('category', 'career')
    prediction = r.choice(predictions[category])

    if not sign or sign not in zodiac:
        return jsonify({"error": "Invalid zodiac sign"}), 400
    
    return jsonify({
        "sign": sign,
        "category": category,
        "prediction": prediction,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "lucky_number": r.randint(1, 100)
    })
@app.route('/horoscope/save', methods=['POST'])
def save_horoscope():
    data = request.get_json()
    if not data or 'prediction' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    db = load_data()
    new_entry = {
        "id": db["next_id"],
        "sign": data["sign"],
        "prediction": data["prediction"],
        "category": data.get("category", "general"),
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    db["savedscope"].append(new_entry)
    db["next_id"] += 1
    save_data(db)
    
    return jsonify(new_entry), 201
@app.route('/horoscope/delete/<int:pred_id>', methods=['DELETE'])
def delete_horoscope(pred_id):
    db = load_data()
    for i, pred in enumerate(db["savedscope"]):
        if pred["id"] == pred_id:
            db["savedscope"].pop(i)
            save_data(db)
            return jsonify({"message": "Prediction deleted"}), 200
    
    return jsonify({"error": "Prediction not found"}), 404
@app.route('/horoscope/saved', methods=['GET'])
def list_saved():
    db = load_data()
    return jsonify({
        "count": len(db["savedscope"]),
        "horoscopes": db["savedscope"]
    })


if __name__ == '__main__':
    app.run(debug=True)