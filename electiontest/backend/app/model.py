from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

FEATURES = ["vote_share", "sentiment", "engagement"]

def train_and_predict(df):
    df["winner"] = df.groupby("constituency_id")["votes"] \
        .transform(lambda x: x == x.max()).astype(int)

    X = df[FEATURES]
    y = df["winner"]

    model = LogisticRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)

    df["score"] = model.predict_proba(X)[:, 1]
    df["win_probability"] = (
        df["score"] /
        df.groupby("constituency_id")["score"].transform("sum")
    )

    return df, model, accuracy



