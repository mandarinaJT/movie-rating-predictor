import requests
from dotenv import load_dotenv
import os

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

