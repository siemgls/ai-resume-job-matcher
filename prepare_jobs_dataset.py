import pandas as pd
from pathlib import Path

INPUT_PATH = "data/job_descriptions.csv"
OUTPUT_PATH = "data/job_descriptions_clean.csv"

df = pd.read_csv(INPUT_PATH)

print("Original columns:")
print(df.columns.tolist())

# Try to automatically detect title and description columns
possible_title_cols = ["job_title", "title", "Job Title", "JobTitle", "position", "Position"]
possible_desc_cols = ["job_description", "description", "Job Description", "JobDescription", "desc", "Description"]

title_col = None
desc_col = None

for col in possible_title_cols:
    if col in df.columns:
        title_col = col
        break

for col in possible_desc_cols:
    if col in df.columns:
        desc_col = col
        break

if title_col is None or desc_col is None:
    print("\nCould not automatically detect columns.")
    print("Please check the printed column names above.")
    raise ValueError("Missing job title or job description column.")

clean_df = df[[title_col, desc_col]].copy()
clean_df.columns = ["job_title", "job_description"]

clean_df = clean_df.dropna()
clean_df["job_title"] = clean_df["job_title"].astype(str)
clean_df["job_description"] = clean_df["job_description"].astype(str)

# Remove very short descriptions
clean_df = clean_df[clean_df["job_description"].str.len() > 50]

# Keep first 500 jobs so the app stays fast
clean_df = clean_df.head(500)

Path("data").mkdir(exist_ok=True)
clean_df.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved cleaned job dataset to {OUTPUT_PATH}")
print("Rows:", len(clean_df))
print(clean_df.head())