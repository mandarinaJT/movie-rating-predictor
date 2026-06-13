from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import ast

GENRE_MAP = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

def oneHotGenres(my_movies_df: pd.DataFrame, popular_movies_df: pd.DataFrame):

    mlb = MultiLabelBinarizer()

    all_genres = pd.concat([
        my_movies_df["genre_ids"],
        popular_movies_df["genre_ids"]
    ])

    all_genres = all_genres.apply(ast.literal_eval)

    mlb.fit(all_genres)

    my_movies_df = oneHotGenresSingle(my_movies_df, mlb)
    popular_movies_df = oneHotGenresSingle(popular_movies_df, mlb)

    return my_movies_df, popular_movies_df, mlb


def oneHotGenresSingle(df: pd.DataFrame, mlb):

    df = df.copy()

    df["genre_ids"] = df["genre_ids"].apply(ast.literal_eval)

    genre_matrix = mlb.transform(df["genre_ids"])

    genre_df = pd.DataFrame(genre_matrix, columns=[str(c) for c in mlb.classes_])

    df = pd.concat([df.reset_index(drop=True), genre_df], axis=1)

    return df
