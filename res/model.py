from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
from res import cast_and_crew

class Preprocessor:

    def split(self, df):
        X = df.drop(columns=["my_rating"])
        y = df["my_rating"]

        self.X_train, self.X_temp, self.y_train, self.y_temp = train_test_split(X, y, test_size=0.3, random_state=None,
            shuffle=True)
        self.X_val, self.X_test, self.y_val, self.y_test = train_test_split(self.X_temp, self.y_temp, test_size=0.5, random_state=None,
            shuffle=True)

    def fit(self, df):
        self.top_actors = cast_and_crew.get_top_n(df["actors"], 200)
        self.top_directors = cast_and_crew.get_top_n(df["directors"], 50)

        self.genre_mlb = MultiLabelBinarizer()
        self.genre_mlb.fit(df["genre_ids"])

        self.actor_mlb = MultiLabelBinarizer()
        self.actor_mlb.fit(
            df["actors"].apply(
                lambda x: [a for a in x if a in self.top_actors]
            )
        )

        self.director_mlb = MultiLabelBinarizer()
        self.director_mlb.fit(
            df["directors"].apply(
                lambda x: [d for d in x if d in self.top_directors]
            )
        )

        return self

    def transform(self, df):
        df = df.copy()

        # filter actors/directors
        df["actors"] = df["actors"].apply(
            lambda x: [a for a in x if a in self.top_actors]
        )

        df["directors"] = df["directors"].apply(
            lambda x: [d for d in x if d in self.top_directors]
        )

        # reset index so positional concatenation aligns rows correctly
        df = df.reset_index(drop=True)

        actor_df = pd.DataFrame(
            self.actor_mlb.transform(df["actors"]),
            columns=[f"actor__{c}" for c in self.actor_mlb.classes_],
            index=df.index,
        )

        director_df = pd.DataFrame(
            self.director_mlb.transform(df["directors"]),
            columns=[f"director__{c}" for c in self.director_mlb.classes_],
            index=df.index,
        )

        genre_df = pd.DataFrame(
            self.genre_mlb.transform(df["genre_ids"]),
            columns=[f"genre__{c}" for c in self.genre_mlb.classes_],
            index=df.index,
        )

        df = df.drop(columns=["actors", "directors", "genre_ids"])

        df = pd.concat(
            [
                df,
                genre_df,
                actor_df,
                director_df,
            ],
            axis=1,
        )

        return df

# def train_model(X, y):

#     model = RandomForestRegressor(
#         n_estimators = 200,
#         random_state=None
#     )

#     model.fit(self.X_train, self.y_train)

#     val_preds = model.predict(self.X_val)
#     val_mae = mean_absolute_error(self.y_val, val_preds)
#     print("Validation MAE:", val_mae)

#     test_preds = model.predict(self.X_test)
#     test_mae = mean_absolute_error(self.y_test, test_preds)
#     print("TEST MAE:", test_mae)

#     print("\n--- Recommendation Quality Check (Top-K) ---")

#     # combine test predictions with actual ratings
#     test_eval = self.X_test.copy()
#     test_eval["actual"] = self.y_test.values
#     test_eval["predicted"] = test_preds

#     print(test_eval)

#     # sort by predicted rating (what model "recommends")
#     top_k = 20
#     top_preds = test_eval.sort_values("predicted", ascending=False).head(top_k)

#     print(f"\nTop {top_k} predicted movies stats:")
#     print("Average actual rating in top-K:", top_preds["actual"].mean())
#     print("Average predicted rating in top-K:", top_preds["predicted"].mean())

#     # how many are actually good (>= 4.5 for example)
#     good_movies = (top_preds["actual"] >= 4).sum()
#     print(f"Highly rated movies in Top-{top_k}: {good_movies}/{top_k}")

#     return model

