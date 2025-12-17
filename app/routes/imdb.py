from fastapi import APIRouter

from app.services.scraper_service import IMDBScraper

router = APIRouter(prefix="/imdb", tags=["IMDB"])

@router.get("/top250")
async def get_top_250():
    scraper = IMDBScraper()
    data = await scraper.fetch_top_250()
    return {
        'count': len(data),
        'results': data
    }