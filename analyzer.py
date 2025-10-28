# analyzer.py
import json
from scraper import get_deals_for_category

cfg = json.load(open("config.json"))
CATS = cfg.get("CATEGORIES", [])

def parse_price(s):
    # naive: remove currency symbols and commas
    if not s: return None
    s = s.replace("KSh", "").replace("KES", "").replace(",", "").strip()
    try:
        return float("".join(ch for ch in s if (ch.isdigit() or ch=='.')))
    except:
        return None

def compute_stats_for_category(slug):
    deals = get_deals_for_category(slug, limit=50)
    rows = []
    for d in deals:
        p = parse_price(d.get("price"))
        old = parse_price(d.get("old_price"))
        if p and old and old>0:
            disc = (old - p)/old
        else:
            disc = 0
        rows.append((d["name"], p, old, disc, d["link"]))
    if not rows:
        return {"slug": slug, "avg_discount": 0, "count":0}
    avg_disc = sum(r[3] for r in rows)/len(rows)
    return {"slug": slug, "avg_discount": avg_disc, "count": len(rows)}

def rank_categories():
    stats = [compute_stats_for_category(c) for c in CATS]
    return sorted(stats, key=lambda x: (x["avg_discount"], x["count"]), reverse=True)

if __name__ == "__main__":
    print(rank_categories())
