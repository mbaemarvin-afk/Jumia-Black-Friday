
import json
from telegram import Bot

cfg = json.load(open("config.json"))
TELE_TOKEN = cfg.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = cfg.get("TELEGRAM_CHAT_ID")

def post_telegram(text):
    bot = Bot(TELE_TOKEN)
    return bot.send_message(chat_id=CHAT_ID, text=text)
