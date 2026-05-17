from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app) 

@app.route('/search', methods=['GET'])
def search_product():
    query = request.args.get('q')
    base_price = random.randint(500, 2000)
    
    results = [
        {"platform": "Amazon", "price": f"{base_price - 40}", "link": "#", "badge": "Fastest Delivery"},
        {"platform": "Flipkart", "price": f"{base_price + 20}", "link": "#", "badge": "Bank Offers"},
        {"platform": "Myntra", "price": f"{base_price - 60}", "link": "#", "badge": "Best Price"}
    ]
    return jsonify({"product": query, "prices": results})

@app.route('/compare', methods=['GET'])
def compare_products():
    p1 = request.args.get('p1')
    p2 = request.args.get('p2')
    cat = request.args.get('cat') 
    
    if cat == 'beauty':
        comp = {
            "aspect_1": {"title": "Texture & Quality", "desc": f"{p1} feels very lightweight. {p2} has a thicker texture but provides better coverage."},
            "verdict": f"For daily use, **{p1}** is better. For occasional heavy use, go with **{p2}**."
        }
    else:
        comp = {
            "aspect_1": {"title": "Build & Battery", "desc": f"{p1} has premium metal finish (18h battery). {p2} is plastic but gives solid 24h backup."},
            "verdict": f"If battery matters most, **{p2}** is the clear winner."
        }
    return jsonify({"comparison": comp})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
