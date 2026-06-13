from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
from collections import Counter

def encodeCastAndCrew(df):
    df = encode(df, "directors")
    df = encode(df, "actors")
    return df


def encode(df, column_name):
    mlb = MultiLabelBinarizer()

    matrix = mlb.fit_transform(df[column_name])
    new_df = pd.DataFrame(matrix, columns=[str(c) for c in mlb.classes_])

    df = pd.concat([df.reset_index(drop=True), new_df], axis=1)

    return df

def get_top_n(series, n):
    counter = Counter()

    for items in series:
        counter.update(items)

    return set([item for item, _ in counter.most_common(n)])