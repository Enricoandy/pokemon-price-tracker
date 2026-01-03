import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

PRODUCTS = {
    "Terastal Festival EX SV8a": {
        "tcgcompany": "https://tcgcompany.nl/terastal-festival-ex-booster-box/",
        "pokeplaza": "https://pokeplaza.com/en/collections/japans/products/pokemon-sv8a-terastal-festival-ex-japanse-booster-box",
        "tcgjapan": "https://tcgjapan.nl/booster-boxen/589-terastal-festival-booster-box.html",
        "cardgamelife": "https://cardgamelife.com/products/terastal-festival-booster-box/",
        "tcgreus": "https://www.tcgreus.nl/products/pokemon-tcg-terastal-festival-ex-sv8a-japanse-booster-box"
    }
}

# -------------------- SCRAPERS PER WEBSHOP --------------------

def get_price_tcgcompany(url):
    soup = fetch_soup(url)
    if not soup:
        return "Niet gevonden"
    price = soup.select_one(".price")
    return clean_price(price)

def get_price_pokeplaza(url):
    soup = fetch_soup(url)
    if not soup:
        return "Niet gevonden"
    price = soup.select_one(".price-item--regular")
    return clean_price(price)

def get_price_tcgjapan(url):
    soup = fetch_soup(url)
    if not soup:
        return "Niet gevonden"
    price = soup.select_one(".our_price_display")
    return clean_price(price)

def get_price_cardgamelife(url):
    soup = fetch_soup(url)
    if not soup:
        return "Niet gevonden"
    price = soup.select_one(".price-item--regular")
    return clean_price(price)

def get_price_tcgreus(url):
    soup = fetch_soup(url)
    if not soup:
        return "Niet gevonden"
    price = soup.select_one(".price-item--regular")
    return clean_price(price)


# -------------------- HULPFUNCTIES --------------------

def fetch_soup(url):
    if not url:
        return None

    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return None

    return BeautifulSoup(r.text, "html.parser")

def clean_price(price_element):
    if not price_element:
        return "Niet gevonden"

    return (
        price_element.text
        .replace("€", "")
        .replace(",", ".")
        .strip()
    )

SCRAPERS = {
    "tcgcompany": get_price_tcgcompany,
    "pokeplaza": get_price_pokeplaza,
    "tcgjapan": get_price_tcgjapan,
    "cardgamelife": get_price_cardgamelife,
    "tcgreus": get_price_tcgreus
}

# -------------------- MAIN --------------------

rows = []

for product, shops in PRODUCTS.items():
    for shop, url in shops.items():
        scraper = SCRAPERS.get(shop)
        price = scraper(url) if scraper else "Geen scraper"

        rows.append([
            product,
            shop,
            price,
            datetime.now().strftime("%Y-%m-%d")
        ])

        time.sleep(1)  # tegen blokkades

with open("prijzen.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Shop", "Prijs", "Datum"])
    writer.writerows(rows)

print("✅ Klaar! prijzen.csv is aangemaakt.")
