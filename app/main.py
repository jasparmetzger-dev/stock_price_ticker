from fastapi import FastAPI

from app import models
from app.routers import alerts, auth, portfolios
from app.database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(alerts.router)
app.include_router(auth.router)
app.include_router(portfolios.router)


@app.get("/")
def root():
    return {"status" : "running"}

