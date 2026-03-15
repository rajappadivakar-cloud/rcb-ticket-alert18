import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

rcb_tickets_page_url = "https://shop.royalchallengers.com/ticket"

# Dates you want to monitor
tickets_dates = ["2026-03-28", "2026-04-05"]


def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)


def get_dates_of_available_tickets(bs):

    dates = []

    for p in bs.find_all("p", {"class": "css-1nm99ps"}):
        dates.append(p.text)

    return dates


def check_tickets():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(rcb_tickets_page_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    available_tickets_dates = get_dates_of_available_tickets(soup)

    print("Checked at:", datetime.now())

    for available_ticket_date in available_tickets_dates:

        date_obj = datetime.strptime(
            available_ticket_date,
            "%A, %b %d, %Y %I:%M %p"
        )

        formatted_date = date_obj.strftime("%Y-%m-%d")

        if formatted_date in tickets_dates:

            send_telegram(
                f"🚨 RCB TICKETS AVAILABLE!\n\n"
                f"Match Date: {formatted_date}\n"
                f"Book now:\n"
                f"{rcb_tickets_page_url}"
            )

            print("Tickets detected!")

            return

    print("Tickets not available yet")


if __name__ == "__main__":
    check_tickets()
