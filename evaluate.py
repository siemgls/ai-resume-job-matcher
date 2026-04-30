import pandas as pd
from matcher import final_match_score
from sklearn.metrics import accuracy_score, f1_score

# Load dataset
df = pd.read_csv("data/sample_pairs.csv")

predictions = []

for _, row in df.iterrows():
    result = final_match_score(row["resume"], row["job_description"])

    # simple threshold
    prediction = 1 if result["final_score"] >= 60 else 0
    predictions.append(prediction)

# Evaluate
accuracy = accuracy_score(df["label"], predictions)
f1 = f1_score(df["label"], predictions)

print("Accuracy:", accuracy)
print("F1 Score:", f1)