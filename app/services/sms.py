import yfinance as yf
import pandas as pd

from vonage import Vonage, Auth
from vonage_sms import SmsMessage
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

 

def send_message(phone_number: str, name: str, alert_price: float) -> None:
    load_dotenv()

    VONAGE_SECRET = os.getenv("VONAGE_SECRET")
    VONAGE_KEY = os.getenv("VONAGE_KEY")
    print(VONAGE_SECRET)
    print(VONAGE_KEY)

    client = Vonage(Auth(api_key=VONAGE_KEY, api_secret=VONAGE_SECRET))

    body = f"Alert 🐢: Your portfolio '{name}' has now reached the target price of {alert_price:.2f}!"

    client.sms.send(SmsMessage(
        from_="Vonage_StockAlert",
        to=phone_number,
        text=body
    ))



#return (last, current) price
def get_ticker_price(ticker: str) -> tuple[float, float]:
    history: pd.DataFrame = yf.Ticker(ticker=ticker).history(period="1d", interval="5m")
    #print(history.head)
    return history["Close"].iloc[-2], history["Close"].iloc[-1]


if __name__ == "__main__":
    print(find_dotenv())
    num = os.getenv("MY_PHONE_NUMBER")
    print(num)
    send_message(phone_number=num,
                name="test_portfolio",
                alert_price=100.12
                 )