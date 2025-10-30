import requests
import json
import random
import os
from bs4 import BeautifulSoup

with open("config.json", "r") as f:
    config = json.load(f)

BASE_URL = config["BASE_URL"]
CATEGORIES = config["CATEGORIES"]
TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
AFF_CODE = config["AFF_CODE"]
BITLY_TOKEN = config["BITLY_TOKEN"]
HEADERS = config["HEADERS"]

category = random.choice(CATEGORIES)
print(f"🛍️ Fetching hot deals from category: {category}")

url = f"{BASE_URL}{category}/"
response = requests.get(url, headers=HEADERS)
if response.status_code != 200:
    print("⚠️ Failed to fetch products.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
products = soup.select("article.prd._fb.col.c-prd")

deals = []
for product in products[:15]:
    name_tag = product.select_one("h3.name")
    price_tag = product.select_one(".prc")
    link_tag = product.select_one("a.core")
    if name_tag and price_tag and link_tag:
        name = name_tag.text.strip()
        price = price_tag.text.strip()
        link = BASE_URL + link_tag["href"]
        deals.append({"name": name, "price": price, "link": link})

if not deals:
    print("😢 No products found.")
    exit()
else:
    print(f"✅ Found {len(deals)} products.")

posted_links_file = "posted_links.txt"
if not os.path.exists(posted_links_file):
    open(posted_links_file, "w").close()

with open(posted_links_file, "r") as f:
    posted_links = set(line.strip() for line in f.readlines())

def shorten_link(long_url):
    bitly_url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization": f"Bearer {BITLY_TOKEN}", "Content-Type": "application/json"}
    data = {"long_url": long_url}
    r = requests.post(bitly_url, headers=headers, json=data)
    if r.status_code == 200:
        return r.json().get("link", long_url)
    return long_url

new_posts = 0
for d in deals:
    if d["link"] in posted_links:
        continue
    affiliate_link = f"{d['link']}?aff_id={AFF_CODE}"
    short_link = shorten_link(affiliate_link)
    message = f"🛒 {d['name']}\n💰 {d['price']}\n👉 {short_link}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(telegram_url, data=data)
    if response.status_code == 200:
        new_posts += 1
        print("✅ Posted new deal to Telegram!")
        with open(posted_links_file, "a") as f:
            f.write(d["link"] + "\n")
    else:
        print("❌ Failed to send:", response.text)

if new_posts == 0:
    print("ℹ️ No new deals to post right now.")
else:
    print(f"🎉 Posted {new_posts} new deals.")
