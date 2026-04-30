import os
import json
import pandas as pd
from huggingface_hub import snapshot_download

repo_path = snapshot_download(
    repo_id="netsol/resume-score-details",
    repo_type="dataset"
)

rows = []

for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith(".json"):
            path = os.path.join(root, file)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    item = json.load(f)

                input_data = item.get("input", {})
                output_data = item.get("output", {})

                resume = input_data.get("resume", "")
                job = input_data.get("job_description", "")

                label = 1 if file.startswith("match") else 0

                if resume and job:
                    rows.append({
                        "resume": resume,
                        "job_description": job,
                        "label": label
                    })

            except Exception as e:
                print("Skipped file:", file, "| Error:", e)

df = pd.DataFrame(rows)

print("Loaded rows:", len(df))
print(df["label"].value_counts())

df.to_csv("data/hf_dataset.csv", index=False)

print("Saved to data/hf_dataset.csv")