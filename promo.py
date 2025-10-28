
import random

TEMPLATES = [
    "🔥 {name} now at {price}! Grab it here 👉 {link} (Limited stock!)",
    "Deal Alert: {name} — only {price} today. Buy now: {link}",
    "🔖 Save big: {name} was {old_price}, now {price}. Link: {link}",
    "Top pick: {name} at {price}. Checkout 👉 {link} #BlackFriday"
]

def make_caption(deal):
    tpl = random.choice(TEMPLATES)
    return tpl.format(
        name=deal.get("name","Product"),
        price=deal.get("price",""),
        old_price=deal.get("old_price",""),
        link=deal.get("link","")
    )
