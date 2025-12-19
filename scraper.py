from playwright.sync_api import sync_playwright
from datetime import datetime
import csv
import time

PRODUCTS = {
    "Terastal Festival EX SV8A": {
        "tcgcompany": "https://tcgcompany.nl/terastal-festival-ex-booster-box/",
        "pokeplaza": "https://www.pokeplaza.nl/products/pokemon-sv8a-terastal-festival-ex-japanse-booster-box",
        "pokejapan": "https://tcgjapan.nl/booster-boxen/589-terastal-festival-booster-box.html",
        "cardgamelife": "",
        "tcgreus": ""
    }
}

SHOP_SELECTORS = {
    "tcgcompany": ".woocommerce-Price-amount",
    "pokeplaza": ".price .money",
    "pokejapan": "#our_price_display",
    "cardgamelife": ".woocommerce-Price-amount",
    "tcgreus": ".woocommerce-Price-amount"
}

rows = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for product, shops in PRODUCTS.items():
        for shop, url in shops.items():

            if not url:
                price = "Niet gevonden"
            else:
                try:
                    page.goto(url, timeout=60000)
                    page.wait_for_timeout(4000)

                    selector = SHOP_SELECTORS.get(shop)
                    element = page.query_selector(selector)

                    price = element.inner_text().strip() if element else "Niet gevonden"

                except Exception:
                    price = "Niet gevonden"

            rows.append([
                product,
                shop,
                price,
                datetime.now().strftime("%Y-%m-%d")
            ])

    browser.close()

with open("prijzen.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product", "Shop", "Prijs", "Datum"])
    writer.writerows(rows)

print("✅ prijzen.csv succesvol aangemaakt")
