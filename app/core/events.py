import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

LOG_DIR = Path("app/logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def startup_event():
    logging.info("Application has started successfully.")

def shutdown_event():
    logging.info("Application is shutting down.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_event()
    yield
    shutdown_event()