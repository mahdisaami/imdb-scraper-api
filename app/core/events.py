import logging
from pathlib import Path

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
