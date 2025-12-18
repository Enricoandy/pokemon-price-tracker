import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

PRODUCTS = {
    "Terastal Festival EX": {
        "tcgcompany": "https://www.tcgcompany.nl/...",
        "pokeplaza": "https://www.pokeplaza.nl/...",
        "pokejapan": "https://www.pokejapan.nl/...",
        "cardgamelife": "https://www.cardgamelife.nl/...",
        "tcgreus": "https://www.tcgreus.nl/..."
    }
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_price(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.select_one(".price")
        return price.text.strip() if price else "Niet gevonden"
    except:
        return "Fout"

rows = []
for product, shops in PRODUCTS.items():
    for shop, url in shops.items():
        rows.append([
            product,
            shop,
            get_price(url),
            datetime.now().strftime("%Y-%m-%d")
        ])

with open("prijzen.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Shop", "Prijs", "Datum"])
    writer.writerows(rows)
