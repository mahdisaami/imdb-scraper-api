import json

import httpx
from bs4 import BeautifulSoup

from app.services.extract_data import extract_250_movies
from app.services.proxy_service import ProxyRouter
from app.utils.helpers import rate_limit

IMDB_TOP_URL = "https://www.imdb.com/chart/top"

proxies_list = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
]

proxy_router = ProxyRouter(proxies_list)

class IMDBScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9"
        }

    async def fetch_top_250(self):
        proxy = await proxy_router.get_proxy()

        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=10,
            follow_redirects=True,

        ) as client:

            response = await client.get(IMDB_TOP_URL)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        script_tag = soup.find("script", id="__NEXT_DATA__")
        if not script_tag or not script_tag.string:
            raise RuntimeError("IMDB NEXT_DATA not found")

        data = json.loads(script_tag.string)
        edges = data["props"]["pageProps"]["pageData"]["chartTitles"]["edges"]

        results = extract_250_movies(edges)

        await rate_limit()

        return results