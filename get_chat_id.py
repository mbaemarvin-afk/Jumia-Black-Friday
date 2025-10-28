import requests
import json

with open("config.json", "r") as f:
    config = json.load(f)

token = config["TELEGRAM_TOKEN"]

url = f"https://api.telegram.org/bot{token}/getUpdates"
response = requests.get(url)
print(response.text)
