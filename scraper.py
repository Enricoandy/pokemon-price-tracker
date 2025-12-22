import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

PRODUCTS = {
    "pokemon 151 SV2A": {
        "tcgcompany": "https://tcgcompany.nl/151-booster-box-geen-seal-no-shrink/",
        "pokeplaza": "https://pokeplaza.com/en/products/pokemon-sv2a-151-japanse-booster-box?_pos=8&_sid=86000c676&_ss=r",
        "pokejapan": "URL_POKEJAPAN_151",
        "cardgamelife": "URL_CARDGAMELIFE_151",
        "tcgreus": "URL_TCGREUS_151"
    },
    "battle partners SV9": {
        "tcgcompany": "URL_TCGCOMPANY_BP",
        "pokeplaza": "URL_POKEPLAZA_BP",
        "pokejapan": "URL_POKEJAPAN_BP",
        "cardgamelife": "URL_CARDGAMELIFE_BP",
        "tcgreus": "URL_TCGREUS_BP"
    },
    "black bolt sv11b": {
        "tcgcompany": "URL_TCGCOMPANY_BB",
        "pokeplaza": "URL_POKEPLAZA_BB",
        "pokejapan": "URL_POKEJAPAN_BB",
        "cardgamelife": "URL_CARDGAMELIFE_BB",
        "tcgreus": "URL_TCGREUS_BB"
    },
    "White flare sv11": {
        "tcgcompany": "URL_TCGCOMPANY_WF",
        "pokeplaza": "URL_POKEPLAZA_WF",
        "pokejapan": "URL_POKEJAPAN_WF",
        "cardgamelife": "URL_CARDGAMELIFE_WF",
        "tcgreus": "URL_TCGREUS_WF"
    },
    "Crimson haze sv5a": {
        "tcgcompany": "URL_TCGCOMPANY_CH",
        "pokeplaza": "URL_POKEPLAZA_CH",
        "pokejapan": "URL_POKEJAPAN_CH",
        "cardgamelife": "URL_CARDGAMELIFE_CH",
        "tcgreus": "URL_TCGREUS_CH"
    },
    "future flash sv4m": {
        "tcgcompany": "URL_TCGCOMPANY_FF",
        "pokeplaza": "URL_POKEPLAZA_FF",
        "pokejapan": "URL_POKEJAPAN_FF",
        "cardgamelife": "URL_CARDGAMELIFE_FF",
        "tcgreus": "URL_TCGREUS_FF"
    },
    "Heat wave arena SV9a": {
        "tcgcompany": "URL_TCGCOMPANY_HWA",
        "pokeplaza": "URL_POKEPLAZA_HWA",
        "pokejapan": "URL_POKEJAPAN_HWA",
        "cardgamelife": "URL_CARDGAMELIFE_HWA",
        "tcgreus": "URL_TCGREUS_HWA"
    },
    "Mask of change SV6": {
        "tcgcompany": "URL_TCGCOMPANY_MOC",
        "pokeplaza": "URL_POKEPLAZA_MOC",
        "pokejapan": "URL_POKEJAPAN_MOC",
        "cardgamelife": "URL_CARDGAMELIFE_MOC",
        "tcgreus": "URL_TCGREUS_MOC"
    },
    "cyber judge sv5m": {
        "tcgcompany": "URL_TCGCOMPANY_CJ",
        "pokeplaza": "URL_POKEPLAZA_CJ",
        "pokejapan": "URL_POKEJAPAN_CJ",
        "cardgamelife": "URL_CARDGAMELIFE_CJ",
        "tcgreus": "URL_TCGREUS_CJ"
    },
    "mega brave m1L": {
        "tcgcompany": "URL_TCGCOMPANY_MB",
        "pokeplaza": "URL_POKEPLAZA_MB",
        "pokejapan": "URL_POKEJAPAN_MB",
        "cardgamelife": "URL_CARDGAMELIFE_MB",
        "tcgreus": "URL_TCGREUS_MB"
    },
    "mega dream ex M2A": {
        "tcgcompany": "URL_TCGCOMPANY_MD",
        "pokeplaza": "URL_POKEPLAZA_MD",
        "pokejapan": "URL_POKEJAPAN_MD",
        "cardgamelife": "URL_CARDGAMELIFE_MD",
        "tcgreus": "URL_TCGREUS_MD"
    },
    "Mega symphonia m1s": {
        "tcgcompany": "URL_TCGCOMPANY_MS",
        "pokeplaza": "URL_POKEPLAZA_MS",
        "pokejapan": "URL_POKEJAPAN_MS",
        "cardgamelife": "URL_CARDGAMELIFE_MS",
        "tcgreus": "URL_TCGREUS_MS"
    },
    "Paradigm trigger": {
        "tcgcompany": "URL_TCGCOMPANY_PT",
        "pokeplaza": "URL_POKEPLAZA_PT",
        "pokejapan": "URL_POKEJAPAN_PT",
        "cardgamelife": "URL_CARDGAMELIFE_PT",
        "tcgreus": "URL_TCGREUS_PT"
    },
    "Paradise dragona sv7a": {
        "tcgcompany": "URL_TCGCOMPANY_PD",
        "pokeplaza": "URL_POKEPLAZA_PD",
        "pokejapan": "URL_POKEJAPAN_PD",
        "cardgamelife": "URL_CARDGAMELIFE_PD",
        "tcgreus": "URL_TCGREUS_PD"
    },
    "ruler of the black flame sv3": {
        "tcgcompany": "URL_TCGCOMPANY_RBF",
        "pokeplaza": "URL_POKEPLAZA_RBF",
        "pokejapan": "URL_POKEJAPAN_RBF",
        "cardgamelife": "URL_CARDGAMELIFE_RBF",
        "tcgreus": "URL_TCGREUS_RBF"
    },
    "stellar miracle sv7": {
        "tcgcompany": "URL_TCGCOMPANY_SM",
        "pokeplaza": "URL_POKEPLAZA_SM",
        "pokejapan": "URL_POKEJAPAN_SM",
        "cardgamelife": "URL_CARDGAMELIFE_SM",
        "tcgreus": "URL_TCGREUS_SM"
    },
    "super electric breaker sv8": {
        "tcgcompany": "URL_TCGCOMPANY_SEB",
        "pokeplaza": "URL_POKEPLAZA_SEB",
        "pokejapan": "URL_POKEJAPAN_SEB",
        "cardgamelife": "URL_CARDGAMELIFE_SEB",
        "tcgreus": "URL_TCGREUS_SEB"
    },
    "terastal festival sv8a": {
PRODUCTS = {
    "Terastal Festival EX SV8a": {
        "tcgcompany": "https://tcgcompany.nl/terastal-festival-ex-booster-box/",
        "pokeplaza": "https://www.pokeplaza.nl/products/pokemon-sv8a-terastal-festival-ex-japanse-booster-box",
        "pokejapan": "https://tcgjapan.nl/booster-boxen/589-terastal-festival-booster-box.html",
        "cardgamelife": "",
        "tcgreus": ""
    }
}

    },
    "vstar universe 12a": {
        "tcgcompany": "URL_TCGCOMPANY_VU",
        "pokeplaza": "URL_POKEPLAZA_VU",
        "pokejapan": "URL_POKEJAPAN_VU",
        "cardgamelife": "URL_CARDGAMELIFE_VU",
        "tcgreus": "URL_TCGREUS_VU"
    },
    "shiny treasure ex s4a": {
        "tcgcompany": "URL_TCGCOMPANY_STE",
        "pokeplaza": "URL_POKEPLAZA_STE",
        "pokejapan": "URL_POKEJAPAN_STE",
        "cardgamelife": "URL_CARDGAMELIFE_STE",
        "tcgreus": "URL_TCGREUS_STE"
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
