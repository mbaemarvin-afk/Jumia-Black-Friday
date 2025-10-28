import requests
import json
import random
from bs4 import BeautifulSoup

with open("config.json", "r") as f:
    config = json.load(f)

BASE_URL = config["BASE_URL"]
CATEGORIES = config["CATEGORIES"]
TELEGRAM_TOKEN = "8248716217:AAFlkDGIPGIIz1LHizS3OgSUdj94dp6C5-g"
TELEGRAM_CHAT_ID = "-1003285979057"
AFF_CODE = "5bed0bdf3d1ca"
BITLY_TOKEN = "77a3bc0d1d8e382c9dbd2b72efc8d748c0af814b"

PROMO_CODES = [
    "🔥 Use code BF2025 for extra 10% off!",
    "💸 Apply coupon: SALE50 for discounts on checkout!",
    "🎁 Save more: FREEDEL on selected items!",
    "💥 Black Friday: Up to 70% off electronics!"
]

BANNERS = [
    "https://affiliate.jumia.com/banners/blackfriday_banner1.jpg",
    "https://affiliate.jumia.com/banners/electronics_banner.jpg",
    "https://affiliate.jumia.com/banners/healthbeauty_banner.jpg",
    "https://affiliate.jumia.com/banners/fashion_banner.jpg"
]

category = random.choice(CATEGORIES)
print(f"🛍️ Fetching hot deals from category: {category}")

url = f"{BASE_URL}{category}/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("⚠️ Failed to fetch products.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
products = soup.select("article.prd._fb.col.c-prd")

deals = []
for product in products[:10]:
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
    print(f"✅ Found {len(deals)} products.\n")

def shorten_link(long_url):
    bitly_url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization": f"Bearer {BITLY_TOKEN}", "Content-Type": "application/json"}
    data = {"long_url": long_url}
    r = requests.post(bitly_url, headers=headers, json=data)
    return r.json().get("link", long_url) if r.status_code == 200 else long_url

for d in deals:
    affiliate_link = f"{d['link']}?aff_id={AFF_CODE}"
    short_link = shorten_link(affiliate_link)
    promo = random.choice(PROMO_CODES)
    banner = random.choice(BANNERS)
    message = (
        f"🛍️ {d['name']}\n"
        f"💰 {d['price']}\n"
        f"{promo}\n"
        f"🔗 {short_link}\n\n"
        f"🖼️ Banner: {banner}"
    )

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(telegram_url, data=data)

    if response.status_code == 200:
        print("✅ Posted to Telegram successfully!")
    else:
        print("❌ Failed to send:", response.text)
