import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_nse_stocks():
    url = "https://afx.kwayisi.org/nse/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
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

        with open("stocks_data.json", "w") as f:
            json.dump(stocks, f, indent=2)

        print(f"✅ {len(stocks)} stocks saved to stocks_data.json")
        return stocks

    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    scrape_nse_stocks()