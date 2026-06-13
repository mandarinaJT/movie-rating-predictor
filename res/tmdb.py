import requests
from dotenv import load_dotenv
from pandas import DataFrame
import os
from tqdm import tqdm
from res import cache
import time

load_dotenv()

access_token = os.getenv("TMDB_READ_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}",
}

def get_movie_by_title_and_year(title: str, year: int):
    
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "query": title,
        "year": year,
    }
    
    response = requests.get(url, headers=headers, params=params)

    return response.json()


def get_all_movies_from_ratings(my_cache, df: DataFrame):

    results = []

    for row in tqdm(df.itertuples(index=False), total=len(df), desc="Processing movies"):
        title = row.Name
        year = row.Year
        my_rating = row.Rating
        date_rated = row.Date

        result = cache.get_cached_movie(my_cache, title, year)

        if not result.get("results"):
            continue

        m = result["results"][0]

        results.append({
            "title": title,
            "year": year,
            "my_rating": my_rating,
            "date_rated": date_rated,
            "tmdb_id": m["id"],
            "genre_ids": m["genre_ids"],
            "vote_average": m["vote_average"],
            "vote_count": m["vote_count"],
            "popularity": m["popularity"],
            "release_date": m["release_date"],
            "original_language": m["original_language"],
        })

    return results


def get_popular_movies_page(page: int):

    url = "https://api.themoviedb.org/3/movie/popular"

    params = {"page": page}

    response = requests.get(url, headers=headers, params=params)


    return response.json()

def get_popular_movies():

    results = []

    for page in tqdm(range(1, 501), desc="Processing movies"):
        result = get_popular_movies_page(page)

        movies = result.get("results", [])

        for m in movies:

            results.append({
                "title": m["title"],
                "year": m["release_date"][:4] if m.get("release_date") else None,
                "tmdb_id": m["id"],
                "genre_ids": m["genre_ids"],
                "vote_average": m["vote_average"],
                "vote_count": m["vote_count"],
                "popularity": m["popularity"],
                "release_date": m["release_date"],
                "original_language": m["original_language"],
            })

    return results


def get_genres():
    response = requests.get(
        "https://api.themoviedb.org/3/genre/movie/list",
        headers=headers,
    )

    print(response.json())


def get_credits(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed for {tmdb_id}: {e}")
        return {"cast": [], "crew": []}
    


def extract_directors(credits):
    return [
        person["name"]
        for person in credits.get("crew", [])
        if person.get("job") == "Director"
    ]

def extract_actors(credits, top_n=5):
    cast = credits.get("cast", [])

    return [actor["name"] for actor in cast[:top_n]]

def add_cast_and_crew(my_cache, df):
    directors = []
    actors = []

    # for row in tqdm(df.itertuples(index=False), total=len(df), desc="Processing movies"):
    for tmdb_id in tqdm(df["tmdb_id"], total=len(df), desc="Processing credits"):
        credits = cache.get_cached_credits(my_cache, tmdb_id)

        directors.append(extract_directors(credits))
        actors.append(extract_actors(credits, top_n=5))
    
    df["directors"] = directors
    df["actors"] = actors

    return df



        

    

