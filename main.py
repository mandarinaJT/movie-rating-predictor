import pandas as pd
from res import tmdb, cache

my_cache = cache.open_cache()


#USER MOVIES


# df = pd.read_csv("data/ratings.csv")
# results = tmdb.get_all_movies_from_ratings(my_cache, df)
# results_df = pd.DataFrame(results)
# results_df.to_csv("data/movies_enriched.csv", index=False)



#ALL MOVIES


# popular = tmdb.get_popular_movies()
# popular_df = pd.DataFrame(popular)
# popular_df.to_csv("data/popular.csv", index=False)


cache.save_cache(my_cache)