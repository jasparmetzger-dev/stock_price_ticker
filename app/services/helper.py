import yfinance as yf
import pandas as pd

from twilio.rest import Client
import os
from dotenv import load_dotenv
 

def send_message(phone_number: str, name: str, alert_price: float) -> None:
    load_dotenv()

    EXPORT_PHONE_NUMBER = os.getenv("EXPORT_PHONE_NUMBER")
    ACCOUNNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(ACCOUNNT_SID, AUTH_TOKEN)

    body = f"Alert 🐢: Your portfolio '{name}' has now reached the target price of {alert_price:.2f}!"

    client.messages.create(
        to=phone_number,
        from_=EXPORT_PHONE_NUMBER,
        body=body
    )


#return (last, current) price
def get_ticker_price(ticker: str) -> tuple[float, float]:
    history: pd.DataFrame = yf.Ticker(ticker=ticker).history(period="1d", interval="5m")
    #print(history.head)
    return history["Close"].iloc[-2], history["Close"].iloc[-1]


if __name__ == "__main__":
    send_message(phone_number=os.getenv("MY_PHONE_NUMBER"),
                name="test_portfolio",
                alert_price=100.12
                 )