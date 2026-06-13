import pandas as pd
from res import genres, cast_and_crew
from res.model import Preprocessor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import ast



my_movies_df = pd.read_csv("data/movies_enriched.csv")

popular_movies_df = pd.read_csv("data/popular.csv")

popular_movies_df = popular_movies_df[
    ~popular_movies_df["tmdb_id"].isin(my_movies_df["tmdb_id"])
]



for col in ["genre_ids", "actors", "directors"]:
    my_movies_df[col] = my_movies_df[col].apply(ast.literal_eval)

for col in ["genre_ids", "actors", "directors"]:
    popular_movies_df[col] = popular_movies_df[col].apply(ast.literal_eval)

pre = Preprocessor()

pre.split(my_movies_df)
assert pre.X_train.columns.is_unique
pre.fit(pre.X_train)

train_df = pre.transform(pre.X_train)
val_df = pre.transform(pre.X_val)
test_df = pre.transform(pre.X_test)
popular_df = pre.transform(popular_movies_df)


feature_cols = (
    [f"genre__{c}" for c in pre.genre_mlb.classes_]
    + [f"actor__{c}" for c in pre.actor_mlb.classes_]
    + [f"director__{c}" for c in pre.director_mlb.classes_]
    + ["vote_average", "vote_count", "popularity", "year"]
)


X_train = train_df[feature_cols]
X_val = val_df[feature_cols]
X_test = test_df[feature_cols]
X_popular = popular_df[feature_cols]

y_train = pre.y_train
y_val = pre.y_val
y_test = pre.y_test

model = RandomForestRegressor(
    n_estimators=200,
    random_state=None,
)


model.fit(X_train, y_train)

val_preds = model.predict(X_val)
print("Validation MAE:", mean_absolute_error(y_val, val_preds))

test_preds = model.predict(X_test)
print("Test MAE:", mean_absolute_error(y_test, test_preds))

print("\n--- Recommendation Quality Check (Top-K) ---")

    # combine test predictions with actual ratings
test_eval = X_test.copy()
test_eval["actual"] = y_test.values
test_eval["predicted"] = test_preds



    # sort by predicted rating (what model "recommends")
top_k = 20
top_preds = test_eval.sort_values("predicted", ascending=False).head(top_k)
print(top_preds)

print(f"\nTop {top_k} predicted movies stats:")
print("Average actual rating in top-K:", top_preds["actual"].mean())
print("Average predicted rating in top-K:", top_preds["predicted"].mean())

    # how many are actually good (>= 4.5 for example)
good_movies = (top_preds["actual"] >= 4).sum()
print(f"Highly rated movies in Top-{top_k}: {good_movies}/{top_k}")

popular_df["predicted_rating"] = model.predict(X_popular)

recommendations = popular_df.sort_values(
    "predicted_rating",
    ascending=False,
).head(10)

print(recommendations[["title", "predicted_rating"]])




