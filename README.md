# AI Resume–Job Matching System

An intelligent career tool that scores how well a resume matches a job description using fine-tuned transformer embeddings, skill extraction, experience matching, and GPT-powered feedback.

Built with Streamlit. Developed as an Advanced AI individual project (BCS).

---

## Features

### Two matching modes
- **Single job mode** — paste any job description and get an instant match analysis
- **Auto mode (default)** — scan all 500 jobs and get a ranked list of the best matches

### Match scoring
The final score is a weighted combination of three signals:

| Component | Weight |
|---|---|
| Semantic similarity | 60% |
| Skill match | 25% |
| Experience match | 15% |

### AI feedback & improvement
- **AI Feedback** — GPT-4o-mini returns strengths and weaknesses specific to the selected job
- **Resume Improvements** — separate GPT prompt rewrites the summary, adds bullet points, and suggests project ideas for missing skills
- **Apply & Download** — GPT rewrites the full resume and exports it as a styled PDF (name, section headers, bullets formatted with ReportLab)
- **Skill Gap Roadmap** — GPT generates a 2-week learning plan per missing skill with resume bullets to add

### UX
- PDF preview of uploaded resume rendered directly in the browser
- Results displayed on a dedicated results page with a back button
- Job selector dropdown to switch between top-10 matches without re-running the scan
- Email button that opens your mail client with a pre-composed results email to the candidate
- Uploading a new resume automatically clears all previous results

---

## How It Works

### 1. Fine-tuned sentence embeddings
- Base model: `sentence-transformers/all-MiniLM-L6-v2`
- Fine-tuned on 816 labelled resume–job pairs using `CosineSimilarityLoss`
- Pushes matching pairs close together and non-matching pairs apart in vector space
- Saved to `fine_tuned_model/`

### 2. Skill extraction (KeyBERT)
- KeyBERT extracts candidate skill phrases from both resume and job description
- Phrases are mapped to a curated `KNOWN_SKILLS` list via embedding similarity (threshold 0.55)
- Skill score = `0.70 × job_coverage + 0.30 × resume_relevance`

### 3. Experience matching
- Regex extracts years of experience from both texts
- Score is 100% if the candidate meets or exceeds the required years

### 4. Two-stage retrieval (fast mode)
- All 500 job embeddings are pre-computed once and saved to `data/job_embeddings.npy`
- On resume upload: one matrix multiply compares the resume against all 500 jobs instantly
- Full weighted scoring only runs on the top-K candidates

---

## Datasets

| Dataset | Source | Use |
|---|---|---|
| `hf_dataset.csv` | HuggingFace — `netsol/resume-score-details` | 1,021 labelled resume–job pairs for fine-tuning |
| `job_descriptions_clean.csv` | Kaggle job descriptions | 500 real job postings for matching |

The HuggingFace dataset was split 80/20 (stratified): **816 training / 205 test**.

---

## Evaluation Results

Evaluated on the **held-out 205-example test set** (never seen during training):

| Metric | Result |
|---|---|
| Accuracy | **89.8%** |
| F1 Score | **92.4%** |
| Precision (match) | 86% |
| Recall (match) | **99%** |
| Top-1 Ranking Accuracy | **100%** |
| Top-3 Ranking Accuracy | **100%** |

In all 3 ranking tests the correct resume was ranked #1, scoring 80–93% vs distractors below 44%.

---

## Project Structure

```
ai-resume-job-matcher/
│
├── app.py                    # Streamlit app (home + results pages)
├── matcher.py                # Final weighted match score
├── fast_matcher.py           # Pre-computed embedding scan
├── skills.py                 # KeyBERT skill extraction & scoring
├── experience.py             # Regex experience extraction & scoring
├── feedback.py               # Rule-based fallback feedback
├── gpt_feedback.py           # GPT-4o-mini strengths/weaknesses
├── resume_improver.py        # GPT improvements + styled PDF builder
├── skill_roadmap.py          # GPT skill gap roadmap
├── file_utils.py             # PDF/DOCX/TXT text extraction
│
├── train.py                  # Fine-tune model (80/20 split)
├── evaluate.py               # Accuracy, F1, ranking evaluation
├── precompute_jobs.py        # Pre-compute job embeddings
├── load_hf_dataset.py        # Build hf_dataset.csv from HuggingFace
├── prepare_jobs_dataset.py   # Clean Kaggle job descriptions
│
├── data/
│   ├── hf_dataset.csv                  # Full labelled dataset
│   ├── hf_test.csv                     # Held-out test set (205 rows)
│   ├── job_descriptions_clean.csv      # 500 cleaned job postings
│   ├── job_descriptions_with_index.csv # Jobs with stable index for embeddings
│   ├── job_embeddings.npy              # Pre-computed job vectors (gitignored)
│   ├── evaluation_results.csv          # Binary classification results
│   └── ranking_results.csv             # Ranking evaluation results
│
├── fine_tuned_model/         # Saved fine-tuned sentence transformer
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your OpenAI API key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

Required for: AI feedback, resume improvements, skill roadmap, and resume rewriting.
All GPT features fall back to rule-based output if the key is missing or invalid.

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Enable fast matching (recommended, one-time)

```bash
python precompute_jobs.py
```

Pre-computes embeddings for all 500 jobs and saves them to `data/job_embeddings.npy`.
Without this the app falls back to slower per-job scoring.

### 5. (Optional) Retrain the model

```bash
python train.py
```

Reads `data/hf_dataset.csv`, performs an 80/20 stratified split, fine-tunes `all-MiniLM-L6-v2`, and saves the model to `fine_tuned_model/`. Also writes `data/hf_test.csv` for evaluation.

### 6. (Optional) Run evaluation

```bash
python evaluate.py
```

Runs binary classification and ranking evaluation on `data/hf_test.csv` and saves results to `data/evaluation_results.csv` and `data/ranking_results.csv`.

---

## Known Limitations

- Job dataset only covers developer roles (Python, Java, DevOps, etc.) — no cybersecurity, design, or business jobs
- Skill extraction is limited to the `KNOWN_SKILLS` list; unlisted skills are missed
- Experience matching uses a simple year-count regex, not seniority-level NER
- GPT features require a paid OpenAI API key

---

## Future Improvements

- Add cybersecurity, design, and business job categories to the dataset
- Replace keyword skill extraction with a fine-tuned NER model
- ATS compatibility scoring and cover letter generation
- Real-time job scraping instead of a static dataset
- Cloud deployment with authentication
