from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Ye function Amazon ke asli page par jaakar price aur title nikalega
def scrape_amazon(query):
    # Query ko URL format me badalna (e.g. "iphone 15" -> "iphone+15")
    search_query = query.replace(' ', '+')
    url = f"https://www.amazon.in/s?k={search_query}"
    
    # Ye 'headers' Amazon ko bewakoof banayenge ki hum code nahi, asli Chrome browser hain
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Amazon ke code me price 'a-price-whole' class ke andar hota hai
        price_tag = soup.find("span", {"class": "a-price-whole"})
        title_tag = soup.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
        
        if price_tag and title_tag:
            return {
                "platform": "Amazon", 
                "title": title_tag.text.strip()[:30] + "...", # Sirf shuru ke 30 words
                "price": f"₹{price_tag.text}", 
                "link": url, 
                "badge": "Real Live Price"
            }
        else:
            return {"platform": "Amazon", "price": "Out of Stock / Blocked", "link": url, "badge": "Error"}
    except Exception as e:
        return {"platform": "Amazon", "price": "Error", "link": url, "badge": "Failed"}

@app.route('/search', methods=['GET'])
def search_product():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Product name needed"}), 400
    
    # Asli Amazon ka data fetch karna
    amazon_data = scrape_amazon(query)
    
    # Dummy data for Flipkart and Myntra (Isme hum aage asli scraper jodenge)
    results = [
        amazon_data,
        {"platform": "Flipkart", "price": "Coming Soon", "link": "#", "badge": "Building Scraper..."},
        {"platform": "Myntra", "price": "Coming Soon", "link": "#", "badge": "Building Scraper..."}
    ]
    
    return jsonify({"product": query, "prices": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
