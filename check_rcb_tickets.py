import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://rcbmpapi.ticketgenie.in/ticket/eventlist/o"
RCB_TICKETS_PAGE = "https://shop.royalchallengers.com/ticket"


def send_telegram(message):

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)


def check_api():

    try:

        response = requests.get(API_URL, timeout=10)
        data = response.json()

        events = data.get("result", [])

        if len(events) > 0:

            print("API detected ticket events!")

            send_telegram(
                "🚨 RCB TICKETS MAY BE LIVE!\n\n"
                "Check immediately:\n"
                "https://shop.royalchallengers.com"
            )

            return True

        print("API shows no events")

        return False

    except Exception as e:
        print("API check failed:", e)
        return False


def check_website():

    try:

        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(RCB_TICKETS_PAGE, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        ticket_elements = soup.find_all("p", {"class": "css-1nm99ps"})

        if len(ticket_elements) > 0:

            print("Website detected tickets!")

            send_telegram(
                "🚨 RCB TICKETS MAY BE LIVE!\n\n"
                "Check immediately:\n"
                "https://shop.royalchallengers.com/ticket"
            )

            return True

        print("Website shows no tickets")

        return False

    except Exception as e:
        print("Website check failed:", e)
        return False


def check_tickets():

    print("Checking at:", datetime.now())

    api_result = check_api()

    if not api_result:
        check_website()


if __name__ == "__main__":
    check_tickets()
