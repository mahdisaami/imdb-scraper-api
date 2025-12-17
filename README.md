# IMDb Scraper API 🎬

A **FastAPI-based backend service** that scrapes IMDb’s **Top 250 Movies** using async HTTP requests, extracts structured data from Next.js JSON (`__NEXT_DATA__`), persists data in a relational database, and exposes it via a secure REST API.

Built with **scalability, clean architecture, and real-world backend patterns** in mind.

---

## 🚀 Features

### Scraping & Data
- ✅ Async scraping with `httpx`
- ✅ Parses IMDb Next.js data (`__NEXT_DATA__`)
- ✅ Clean data extraction & normalization layer
- ✅ Rate limiting support
- ✅ Ready for proxy rotation & caching

### API & Backend
- ✅ FastAPI RESTful endpoints
- ✅ SQLite database for persistence
- ✅ SQLAlchemy ORM
- ✅ Alembic migrations
- ✅ JWT-based authentication
- ✅ Full User CRUD (Create, Read, Update, Delete)
- ✅ PUT & PATCH support for partial updates
- ✅ Production-friendly project structure

---

## 📦 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **httpx (async)**
- **BeautifulSoup4**
- **lxml**
- **SQLAlchemy**
- **Alembic**
- **SQLite**
- **JWT (Authentication & Authorization)**
- **Uvicorn**

---

## 🔑 API Endpoints

### 🎬 IMDb

#### Get IMDb Top 250 Movies
- **Endpoint:** `GET /imdb/top250`
- **Description:** Fetches the IMDb Top 250 movies with structured data.
- **Auth:** Optional / Protected (depending on configuration)

##### ✅ Example Response
```json
{
  "count": 250,
  "results": [
    {
      "rank": 1,
      "id": "tt0111161",
      "title": "The Shawshank Redemption",
      "year": 1994,
      "rating": 9.3,
      "ratingCount": 3130605,
      "plot": "A banker convicted of uxoricide...",
      "genres": "Drama"
    }
  ]
}

```
## 🚀 Future Improvements
- Docker support: Containerize the project for easy deployment
- Additional endpoints: Fetch details, search movies, stats
- Improved scraping: Rotating proxies, caching, scheduled updates