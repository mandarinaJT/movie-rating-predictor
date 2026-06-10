from res import tmdb
import json
import os

CACHE_FILE = "data/tmdb_cache.json"


def open_cache():
    

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    return cache

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def get_cached_movie(cache, title, year):
    key = f"{title}::{year}"

    if key in cache:
        return cache[key]
    

    result = tmdb.get_movie_by_title_and_year(title, year)
    cache[key] = result

    return result