from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import alerts, auth, portfolios
from app.database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(alerts.router)
app.include_router(auth.router)
app.include_router(portfolios.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

