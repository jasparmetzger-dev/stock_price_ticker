from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import database
from sqlalchemy.orm import Session
from fastapi import Depends

from app.models import Portfolio, Holding, User

router = APIRouter()


class Stock(BaseModel):
    ticker: str
    weight: float

class PortfolioRequest(BaseModel):
    user_id: int
    name: str
    stocks: list[Stock]

def validate_req(stocks: list[Stock]) -> bool:

    cnt: float = sum([x.weight for x in stocks])
    if abs(cnt - 1.0) > 0.01: return False

    #for x in stocks:
    #    if not market_data.is_valid_ticker(x.ticker): return False
    
    return True


@router.post("/portfolio")
def make_portfolio(data: PortfolioRequest, db: Session = Depends(database.get_db)):
    portfolio: PortfolioRequest = data.copy()

    valid_portfolio: bool = validate_req(portfolio.stocks)

    if not valid_portfolio:
        error_msg: str = "Not a valid portfolio. Tickers must be valid and weights must add up to one."
        raise HTTPException(status_code=400, detail=error_msg)
    
    new_portfolio = Portfolio(
        user_id=portfolio.user_id,
        name=portfolio.name
    )
    db.add(new_portfolio)
    db.flush() #writes, but doesnt commit

    for s in portfolio.stocks:
        h = Holding(
            portfolio_id=new_portfolio.id,
            ticker=s.ticker,
            weight=s.weight
        )
        db.add(h)
    db.commit()

    return {"meassage" : "portfolio created."}