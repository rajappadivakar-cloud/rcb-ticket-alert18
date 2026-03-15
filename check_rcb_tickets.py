import os
import requests

# Read secrets from GitHub
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# RCB shop URL
URL = "https://shop.royalchallengers.com"

# Words that may appear when tickets go live
KEYWORDS = [
    "ticket",
    "match ticket",
    "buy ticket",
    "book ticket",
    "stadium ticket"
]


def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)


def check_tickets():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    page_text = response.text.lower()

    for keyword in KEYWORDS:
        if keyword in page_text:
            send_telegram(
                "🚨 RCB MATCH TICKETS MAY BE LIVE!\n\n"
                "Check immediately:\n"
                "https://shop.royalchallengers.com"
            )
            print("Ticket keyword detected!")
            return

    print("No ticket keywords found.")


if __name__ == "__main__":
    check_tickets()
