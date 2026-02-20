from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import database
from app.models import Alert
from sqlalchemy.orm import Session
from fastapi import Depends


router = APIRouter()

class AlertRequest(BaseModel):
    price: float

#nothing to validate atm
def validate_req() -> bool:
    return True

@router.post("/portfolio/{portfolio_id}/alerts")
def make_alert(data: AlertRequest, portfolio_id:int, db: Session = Depends(database.get_db)):
    alert = data.copy()
    valid_alert: bool = validate_req()
    if not valid_alert: raise HTTPException(status_code=400, detail="invalid alert.")

    new_alert = Alert(
        portfolio_id=portfolio_id,
        target=alert.price,
        is_active=True
    )
    db.add(new_alert)
    db.commit()

    return {"message" : "alert created"}