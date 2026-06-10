import pandas as pd
from res import tmdb, cache

df = pd.read_csv("data/ratings.csv")

my_cache = cache.open_cache()

results = tmdb.get_all_movies_from_ratings(my_cache, df)

results_df = pd.DataFrame(results)

results_df.to_csv("data/movies_enriched.csv", index=False)

cache.save_cache(my_cache)