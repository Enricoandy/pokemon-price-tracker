import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import logging
import re

# PRODUCTS (ik heb alleen de key 'pokejapan' vervangen door 'TCGJapan' zoals je vroeg)
PRODUCTS = {
    "pokemon 151 SV2A": {
        "tcgcompany": "https://tcgcompany.nl/151-booster-box-geen-seal-no-shrink/",
        "pokeplaza": "https://pokeplaza.com/en/products/pokemon-sv2a-151-japanse-booster-box?_pos=8&_sid=86000c676&_ss=r",
        "TCGJapan": "URL_POKEJAPAN_151",
        "cardgamelife": "URL_CARDGAMELIFE_151",
        "tcgreus": "URL_TCGREUS_151"
    },
    "battle partners SV9": {
        "tcgcompany": "URL_TCGCOMPANY_BP",
        "pokeplaza": "URL_POKEPLAZA_BP",
        "TCGJapan": "URL_POKEJAPAN_BP",
        "cardgamelife": "URL_CARDGAMELIFE_BP",
        "tcgreus": "URL_TCGREUS_BP"
    },
    "black bolt sv11b": {
        "tcgcompany": "URL_TCGCOMPANY_BB",
        "pokeplaza": "URL_POKEPLAZA_BB",
        "TCGJapan": "URL_POKEJAPAN_BB",
        "cardgamelife": "URL_CARDGAMELIFE_BB",
        "tcgreus": "URL_TCGREUS_BB"
    },
    "White flare sv11": {
        "tcgcompany": "URL_TCGCOMPANY_WF",
        "pokeplaza": "URL_POKEPLAZA_WF",
        "TCGJapan": "URL_POKEJAPAN_WF",
        "cardgamelife": "URL_CARDGAMELIFE_WF",
        "tcgreus": "URL_TCGREUS_WF"
    },
    "Crimson haze sv5a": {
        "tcgcompany": "URL_TCGCOMPANY_CH",
        "pokeplaza": "URL_POKEPLAZA_CH",
        "TCGJapan": "URL_POKEJAPAN_CH",
        "cardgamelife": "URL_CARDGAMELIFE_CH",
        "tcgreus": "URL_TCGREUS_CH"
    },
    "future flash sv4m": {
        "tcgcompany": "URL_TCGCOMPANY_FF",
        "pokeplaza": "URL_POKEPLAZA_FF",
        "TCGJapan": "URL_POKEJAPAN_FF",
        "cardgamelife": "URL_CARDGAMELIFE_FF",
        "tcgreus": "URL_TCGREUS_FF"
    },
    "Heat wave arena SV9a": {
        "tcgcompany": "URL_TCGCOMPANY_HWA",
        "pokeplaza": "URL_POKEPLAZA_HWA",
        "TCGJapan": "URL_POKEJAPAN_HWA",
        "cardgamelife": "URL_CARDGAMELIFE_HWA",
        "tcgreus": "URL_TCGREUS_HWA"
    },
    "Mask of change SV6": {
        "tcgcompany": "URL_TCGCOMPANY_MOC",
        "pokeplaza": "URL_POKEPLAZA_MOC",
        "TCGJapan": "URL_POKEJAPAN_MOC",
        "cardgamelife": "URL_CARDGAMELIFE_MOC",
        "tcgreus": "URL_TCGREUS_MOC"
    },
    "cyber judge sv5m": {
        "tcgcompany": "URL_TCGCOMPANY_CJ",
        "pokeplaza": "URL_POKEPLAZA_CJ",
        "TCGJapan": "URL_POKEJAPAN_CJ",
        "cardgamelife": "URL_CARDGAMELIFE_CJ",
        "tcgreus": "URL_TCGREUS_CJ"
    },
    "mega brave m1L": {
        "tcgcompany": "URL_TCGCOMPANY_MB",
        "pokeplaza": "URL_POKEPLAZA_MB",
        "TCGJapan": "URL_POKEJAPAN_MB",
        "cardgamelife": "URL_CARDGAMELIFE_MB",
        "tcgreus": "URL_TCGREUS_MB"
    },
    "mega dream ex M2A": {
        "tcgcompany": "URL_TCGCOMPANY_MD",
        "pokeplaza": "URL_POKEPLAZA_MD",
        "TCGJapan": "URL_POKEJAPAN_MD",
        "cardgamelife": "URL_CARDGAMELIFE_MD",
        "tcgreus": "URL_TCGREUS_MD"
    },
    "Mega symphonia m1s": {
        "tcgcompany": "URL_TCGCOMPANY_MS",
        "pokeplaza": "URL_POKEPLAZA_MS",
        "TCGJapan": "URL_POKEJAPAN_MS",
        "cardgamelife": "URL_CARDGAMELIFE_MS",
        "tcgreus": "URL_TCGREUS_MS"
    },
    "Paradigm trigger": {
        "tcgcompany": "URL_TCGCOMPANY_PT",
        "pokeplaza": "URL_POKEPLAZA_PT",
        "TCGJapan": "URL_POKEJAPAN_PT",
        "cardgamelife": "URL_CARDGAMELIFE_PT",
        "tcgreus": "URL_TCGREUS_PT"
    },
    "Paradise dragona sv7a": {
        "tcgcompany": "URL_TCGCOMPANY_PD",
        "pokeplaza": "URL_POKEPLAZA_PD",
        "TCGJapan": "URL_POKEJAPAN_PD",
        "cardgamelife": "URL_CARDGAMELIFE_PD",
        "tcgreus": "URL_TCGREUS_PD"
    },
    "ruler of the black flame sv3": {
        "tcgcompany": "URL_TCGCOMPANY_RBF",
        "pokeplaza": "URL_POKEPLAZA_RBF",
        "TCGJapan": "URL_POKEJAPAN_RBF",
        "cardgamelife": "URL_CARDGAMELIFE_RBF",
        "tcgreus": "URL_TCGREUS_RBF"
    },
    "stellar miracle sv7": {
        "tcgcompany": "URL_TCGCOMPANY_SM",
        "pokeplaza": "URL_POKEPLAZA_SM",
        "TCGJapan": "URL_POKEJAPAN_SM",
        "cardgamelife": "URL_CARDGAMELIFE_SM",
        "tcgreus": "URL_TCGREUS_SM"
    },
    "super electric breaker sv8": {
        "tcgcompany": "URL_TCGCOMPANY_SEB",
        "pokeplaza": "URL_POKEPLAZA_SEB",
        "TCGJapan": "URL_POKEJAPAN_SEB",
        "cardgamelife": "URL_CARDGAMELIFE_SEB",
        "tcgreus": "URL_TCGREUS_SEB"
    },
    "Terastal Festival EX SV8a": {
        "tcgcompany": "https://tcgcompany.nl/terastal-festival-ex-booster-box/",
        "pokeplaza": "https://www.pokeplaza.nl/products/pokemon-sv8a-terastal-festival-ex-japanse-booster-box",
        "TCGJapan": "https://tcgjapan.nl/booster-boxen/589-terastal-festival-booster-box.html",
        "cardgamelife": "",
        "tcgreus": ""
    },
    "vstar universe 12a": {
        "tcgcompany": "URL_TCGCOMPANY_VU",
        "pokeplaza": "URL_POKEPLAZA_VU",
        "TCGJapan": "URL_POKEJAPAN_VU",
        "cardgamelife": "URL_CARDGAMELIFE_VU",
        "tcgreus": "URL_TCGREUS_VU"
    },
    "shiny treasure ex s4a": {
        "tcgcompany": "URL_TCGCOMPANY_STE",
        "pokeplaza": "URL_POKEPLAZA_STE",
        "TCGJapan": "URL_POKEJAPAN_STE",
        "cardgamelife": "URL_CARDGAMELIFE_STE",
        "tcgreus": "URL_TCGREUS_STE"
    }
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# A few common selectors to try; je kunt per shop specifieker maken
FALLBACK_SELECTORS = [
    '.price',
    '.product-price',
    '.price-amount',
    '.pricebox',
    '.product__price',
    '.price-tag',
    '.amount',
    'meta[property="product:price:amount"]',
    'meta[itemprop="price"]'
]

# eenvoudige euro/valuta regex
PRICE_RE = re.compile(r'€\s*\d{1,3}(?:[.,]\d{2})?|\d{1,3}(?:[.,]\d{2})?\s*€|\$\s*\d+(?:[.,]\d+)?')

def is_valid_url(url: str) -> bool:
    return isinstance(url, str) and url.strip() and url.strip().lower().startswith(("http://", "https://"))

def extract_price_from_text(text: str) -> str:
    if not text:
        return ""
    m = PRICE_RE.search(text)
    if m:
        return m.group(0).strip()
    # fallback: if text contains digits, return cleaned text (may include currency)
    if re.search(r'\d', text):
        return ' '.join(text.split())
    return ""

def get_price(url: str, shop: str = None) -> str:
    if not is_valid_url(url):
        logging.debug("Ongeldige of lege URL voor shop=%s: %r", shop, url)
        return "Ongeldige URL"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        logging.warning("Netwerkfout bij ophalen %s (%s): %s", shop, url, e)
        return "Fout (netwerk)"

    if r.status_code != 200:
        logging.warning("HTTP %s voor %s: %s", r.status_code, shop, url)
        return f"HTTP {r.status_code}"

    soup = BeautifulSoup(r.text, "html.parser")

    # probeer fallback-selectors
    for sel in FALLBACK_SELECTORS:
        el = soup.select_one(sel)
        if el:
            if el.name == "meta":
                text = el.get("content", "")
            else:
                text = el.get_text(" ", strip=True)
            price = extract_price_from_text(text)
            if price:
                logging.info("Prijs gevonden (%s) met selector %s: %s", shop, sel, price)
                return price

    # probeer hele tekst te doorzoeken
    full_text = soup.get_text(" ", strip=True)
    price = extract_price_from_text(full_text)
    if price:
        logging.info("Prijs gevonden in page text voor %s: %s", shop, price)
        return price

    # niets gevonden — meestal JS-rendered of selector mismatch
    logging.info("Geen prijs gevonden voor %s (mogelijk JS-rendered of andere selector)", shop)
    return "Niet gevonden (mogelijk JS-rendered)"

def main():
    rows = []
    for product, shops in PRODUCTS.items():
        for shop, url in shops.items():
            prijs = get_price(url, shop)
            rows.append([product, shop, prijs, datetime.now().strftime("%Y-%m-%d")])

    # schrijf CSV
    with open("prijzen.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Product", "Shop", "Prijs", "Datum"])
        writer.writerows(rows)

    logging.info("Klaar — prijzen.csv geschreven met %d rijen", len(rows))

if __name__ == "__main__":
    main()
