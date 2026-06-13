from res import tmdb
import json
import os

CACHE_FILE = "data/tmdb_cache.json"


def open_cache():
    

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {"movies": {}, "credits": {}}

    return cache

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def get_cached_movie(cache, title, year):
    key = f"{title}::{year}"

    if key in cache["movies"]:
        return cache["movies"][key]
    

    result = tmdb.get_movie_by_title_and_year(title, year)
    cache["movies"][key] = result

    return result

def get_cached_credits(cache, tmdb_id):
    key = str(tmdb_id)

    if key in cache["credits"]:
        return cache["credits"][key]

    result = tmdb.get_credits(tmdb_id)
    cache["credits"][key] = result

    return result
