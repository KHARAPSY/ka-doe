import json
from fastapi import FastAPI
from api.routes import router as routers
from api.loggings import setup_logger

logger = setup_logger(__name__)

title = "Ka-Doe"
with open("settings.json") as f:
    settings = json.load(f)
version = settings.get("version", "0.0.0")

app = FastAPI(
    title=title,
    version=version
)

app.include_router(routers)

@app.on_event("startup")
async def startup_event():
    logger.info(f"{title} Version: {version} is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{title} Version: {version} is shutting down...")