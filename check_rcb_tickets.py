import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://shop.royalchallengers.com/tickets"


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)


def check_tickets():
    r = requests.get(URL)

    if "sold out" not in r.text.lower():
        send_telegram("🚨 RCB Tickets Might Be Live! Check Now!\nhttps://shop.royalchallengers.com/tickets")
        print("Notification sent!")
    else:
        print("Tickets not available yet")


if __name__ == "__main__":
    check_tickets()
