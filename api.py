from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
CORS(app)

def scrape_and_save():
    url = "https://afx.kwayisi.org/nse/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "lxml")
        tables = soup.find_all("table")
        stocks = []
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 5:
                    stock = {
                        "symbol": cols[0].text.strip(),
                        "name": cols[1].text.strip(),
                        "volume": cols[2].text.strip(),
                        "price": cols[3].text.strip(),
                        "change": cols[4].text.strip(),
                        "timestamp": datetime.now().isoformat()
                    }
                    stocks.append(stock)
        if stocks:
            with open("stocks_data.json", "w") as f:
                json.dump(stocks, f, indent=2)
        return stocks
    except Exception as e:
        print(f"Scraper error: {e}")
        return []

def get_stocks_data():
    if os.path.exists("stocks_data.json"):
        with open("stocks_data.json", "r") as f:
            return json.load(f)
    return scrape_and_save()

@app.route("/")
def home():
    return jsonify({"message": "FaidaAI API is running", "version": "1.0"})

@app.route("/stocks")
def get_stocks():
    stocks = get_stocks_data()
    return jsonify({
        "status": "success",
        "count": len(stocks),
        "data": stocks,
        "last_updated": datetime.now().isoformat()
    })

@app.route("/stocks/<symbol>")
def get_stock(symbol):
    stocks = get_stocks_data()
    stock = next((s for s in stocks if s["symbol"].upper() == symbol.upper()), None)
    if stock:
        return jsonify({"status": "success", "data": stock})
    return jsonify({"status": "error", "message": "Stock not found"}), 404

@app.route("/refresh")
def refresh():
    stocks = scrape_and_save()
    return jsonify({
        "status": "success",
        "message": f"Refreshed {len(stocks)} stocks",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)