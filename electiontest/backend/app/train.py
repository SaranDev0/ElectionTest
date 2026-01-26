import pandas as pd
from model import train_model

elections = pd.read_csv("backend/app/data/elections.csv")
social = pd.read_csv("backend/app/data/social.csv")

df = elections.merge(social, on="candidate_id")
df["vote_share"] = df["votes"] / df["total_votes"]

df["winner"] = df.groupby("constituency_id")["votes"] \
                 .transform(lambda x: x == x.max()) \
                 .astype(int)

train_model(df)
print("✅ Model trained and saved")
