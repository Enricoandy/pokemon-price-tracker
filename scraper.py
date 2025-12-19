import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PokemonPriceBot/1.0)"
}

PRODUCTS = {
    "Pokemon 151 SV2A": {},
    "Battle Partners SV9": {},
    "Black Bolt SV11B": {},
    "White Flare SV11": {},
    "Crimson Haze SV5A": {},
    "Future Flash SV4M": {},
    "Heat Wave Arena SV9A": {},
    "Mask of Change SV6": {},
    "Cyber Judge SV5M": {},
    "Mega Brave M1L": {},
    "Mega Dream EX M2A": {},
    "Mega Symphonia M1S": {},
    "Paradigm Trigger": {},
    "Paradise Dragona SV7A": {},
    "Ruler of the Black Flame SV3": {},
    "Stellar Miracle SV7": {},
    "Super Electric Breaker SV8": {},
    "Terastal Festival EX SV8A": {
        "tcgcompany": "https://tcgcompany.nl/terastal-festival-ex-booster-box/",
        "pokeplaza": "https://www.pokeplaza.nl/products/pokemon-sv8a-terastal-festival-ex-japanse-booster-box",
        "pokejapan": "https://tcgjapan.nl/booster-boxen/589-terastal-festival-booster-box.html",
        "cardgamelife": "",
        "tcgreus": ""
    },
    "VSTAR Universe 12A": {},
    "Shiny Treasure EX S4A": {}
}

SHOPS = ["tcgcompany", "pokeplaza", "pokejapan", "cardgamelife", "tcgreus"]

def get_price(shop, url):
    if not url:
        return "Niet gevonden"

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")

        if shop == "tcgcompany":
            price = soup.select_one("span.price")
            return price.text.strip() if price else "Niet gevonden"

        if shop == "pokeplaza":
            price = soup.select_one("span.money")
            return price.text.strip() if price else "Niet gevonden"

        if shop == "pokejapan":
            price = soup.select_one("span#our_price_display")
            return price.text.strip() if price else "Niet gevonden"

        if shop == "cardgamelife":
            price = soup.select_one(".price")
            return price.text.strip() if price else "Niet gevonden"

        if shop == "tcgreus":
            price = soup.select_one(".woocommerce-Price-amount")
            return price.text.strip() if price else "Niet gevonden"

        return "Niet gevonden"

    except Exception:
        return "Niet gevonden"

rows = []

for product, shops in PRODUCTS.items():
    for shop in SHOPS:
        url = shops.get(shop, "")
        price = get_price(shop, url)
        rows.append([
            product,
            shop,
            price,
            datetime.now().strftime("%Y-%m-%d")
        ])

with open("prijzen.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Shop", "Prijs", "Datum"])
    writer.writerows(rows)

print("✅ Klaar: prijzen.csv aangemaakt")
