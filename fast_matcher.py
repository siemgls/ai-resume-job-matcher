import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "fine_tuned_model"

model = SentenceTransformer(MODEL_NAME)

job_embeddings = np.load("data/job_embeddings.npy")
jobs_df = pd.read_csv("data/job_descriptions_with_index.csv")


def find_top_jobs(resume_text, top_k=10):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    scores = util.cos_sim(resume_embedding, job_embeddings)[0].cpu().numpy()
    top_indices = scores.argsort()[::-1][:top_k]

    results = []

    for idx in top_indices:
        results.append({
            "job_title": jobs_df.iloc[idx]["job_title"],
            "job_description": jobs_df.iloc[idx]["job_description"],
            "semantic_score": round(scores[idx] * 100, 2)
        })

    return results