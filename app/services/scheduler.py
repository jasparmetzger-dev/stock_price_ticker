from apscheduler.schedulers.background import BackgroundScheduler
import app.services.sms as t

from app.models import Alert, Holding, Portfolio
from sqlalchemy.orm import Session
from app.database import SessionLocal


scheduler = BackgroundScheduler()
FREQUENCY = 1 #in minutes


def check_for_alerts() -> None:
    db: Session = SessionLocal()

    try:
        all_active_alerts: list[Alert] = db.query(Alert).filter(Alert.is_active).all()

        for alert in all_active_alerts:
            portfolio: Portfolio = alert.portfolio
            holdings:list[Holding] = portfolio.holdings


            cur_price: float = 0
            last_price: float = 0
            for holding in holdings:
                (cur, last) = t.get_ticker_price(holding.ticker)
                cur_price += cur * holding.weight
                last_price += last * holding.weight
            
            #if price passed alert
            if (last_price < alert.target and alert.target < cur_price) or (last_price > alert.target and alert.target > cur_price):
                t.send_message(phone_number=portfolio.user.phone_number, name=portfolio.name, alert_price=alert.target)
                alert.is_active = False
                db.commit()

    finally: db.close() 


scheduler.add_job(check_for_alerts, "interval", minutes=FREQUENCY)