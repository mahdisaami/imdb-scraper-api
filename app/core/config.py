from fastapi import FastAPI

from app.core.events import shutdown_event, startup_event, lifespan
from app.middleware.time_middleware import ProcessTimeMiddleware
from app.routes import imdb, users

app = FastAPI(
    title = 'IMDB Scraper API',
    description = 'An API to scrape IMDB data including movies, TV shows, and actors.',
    version = '1.0.0',
    lifespan=lifespan,
)




app.add_middleware(ProcessTimeMiddleware)

# app.add_event_handler("startup", startup_event)
# app.add_event_handler("shutdown", shutdown_event)

app.include_router(imdb.router)
app.include_router(users.router)