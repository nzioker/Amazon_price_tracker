import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


def get_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    url = "https://www.amazon.com/Apple-Magic-Keyboard-Computers-Silicon/dp/B09BRG3GRR?ref_=ast_sto_dp&th=1&psc=1"
    response = requests.get(url=url, headers=headers)

    # response.raise_for_status()
    results = response.text

    soup = BeautifulSoup(results, "lxml")
    item = soup.find(name="span", class_="a-offscreen").getText()
    macbook_price = item.split("$")[1]
    macbook_price_float = float(macbook_price)
    return macbook_price_float


def send_mail_alert():
    current_price = get_price()
    if current_price <= 100:
        text = f"The current price of the macbook is {current_price}. Hurry up before the price shoots up."

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs="nzioker@yahoo.com", msg=text)
            print("Done")


send_mail_alert()
