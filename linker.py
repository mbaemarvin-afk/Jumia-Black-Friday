
import json, requests
from urllib.parse import urlencode

cfg = json.load(open("config.json"))
BITLY_TOKEN = cfg.get("BITLY_TOKEN")
AFF = cfg.get("AFF_CODE")

def append_affiliate(url):
    if not AFF:
        return url
    sep = "&" if "?" in url else "?"
    return url + f"{sep}aff_id={AFF}"

def shorten_bitly(long_url):
    if not BITLY_TOKEN:
        return long_url
    headers = {"Authorization": f"Bearer {BITLY_TOKEN}", "Content-Type": "application/json"}
    data = {"long_url": long_url}
    r = requests.post("https://api-ssl.bitly.com/v4/shorten", json=data, headers=headers, timeout=10)
    if r.ok:
        return r.json().get("link", long_url)
    return long_url
