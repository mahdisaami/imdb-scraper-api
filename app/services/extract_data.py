def extract_250_movies(datas):
    results = []

    for item in datas:
        node = item.get("node", {})

        results.append({
            "rank": item.get("currentRank"),
            "imdb_id": node.get("id"),
            "title": node.get("titleText", {}).get("text"),
            "year": node.get("releaseYear", {}).get("year"),
            "rating": node.get("ratingsSummary", {}).get("aggregateRating"),
            "rating_count": node.get("ratingsSummary", {}).get("voteCount"),
            "plot": node.get("plot", {}).get("plotText", {}).get("plainText"),
            "genres": [
                g["genre"]["text"]
                for g in node.get("titleGenres", {}).get("genres", [])
            ]
        })

    return results
