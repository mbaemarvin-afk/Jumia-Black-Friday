import requests
from bs4 import BeautifulSoup
import json
import random

with open("config.json", "r") as f:
    config = json.load(f)

BASE_URL = config["BASE_URL"]
CATEGORIES = config["CATEGORIES"]

category = random.choice(CATEGORIES)
print(f"🛍️ Fetching deals from category: {category}")

url = f"{BASE_URL}{category}/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("⚠️ Failed to fetch the page. Status code:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")
products = soup.select(".core, .sku, .prd")

if not products:
    print("😢 No products found. Try another category slug or update selector.")
else:
    print(f"✅ Found {len(products)} products.\n")

deals = []
for p in products[:10]:
    name = p.select_one(".name")
    price = p.select_one(".prc")
    link_tag = p.find("a", href=True)

    if name and price and link_tag:
        deals.append({
            "name": name.text.strip(),
            "price": price.text.strip(),
            "link": f"https://www.jumia.co.ke{link_tag['href']}"
        })

if not deals:
    print("⚠️ Missing product data — possibly layout changed or class names are different.")
else:
    for d in deals:
        print(d)
