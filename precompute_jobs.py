import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "fine_tuned_model"

model = SentenceTransformer(MODEL_NAME)

df = pd.read_csv("data/job_descriptions_clean.csv")

df = df.dropna(subset=["job_description"])
df["job_description"] = df["job_description"].astype(str)

if "job_title" not in df.columns:
    df["job_title"] = "Unknown Job"

print("Encoding job descriptions...")

embeddings = model.encode(
    df["job_description"].tolist(),
    show_progress_bar=True
)

np.save("data/job_embeddings.npy", embeddings)
df.to_csv("data/job_descriptions_with_index.csv", index=False)

print("Saved data/job_embeddings.npy")
print("Saved data/job_descriptions_with_index.csv")