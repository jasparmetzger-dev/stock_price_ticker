from fastapi import FastAPI

from app import models
from app.routers import auth
from app.database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth.router)


@app.get("/")
def root():
    return {"status" : "running"}

