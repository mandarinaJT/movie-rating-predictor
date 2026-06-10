import pandas as pd
from res import tmdb

df = pd.read_csv("data/ratings.csv")

print(df.shape)
print(df.head(10))
print(df["Rating"].describe())

# title = str(input("Unesi ime filma: "))
# year = int(input("Unesi godinu snimanja: "))

# print(tmdb.get_movie_by_title_and_year(title, year))