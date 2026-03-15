import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://shop.royalchallengers.com"

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
    page = response.text.lower()

    # Detect navigation tab
    ticket_tab = ">tickets<" in page

    # Detect buy button
    buy_button = "buy tickets" in page

    if ticket_tab or buy_button:

        send_telegram(
            "🚨 RCB MATCH TICKETS ARE LIVE!\n\n"
            "Go immediately:\n"
            "https://shop.royalchallengers.com"
        )

        print("Ticket tab or buy button detected!")

    else:
        print("Tickets not live yet.")


if __name__ == "__main__":
    check_tickets()
