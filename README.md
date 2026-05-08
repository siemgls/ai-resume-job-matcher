# AI Resume–Job Matching System

An AI-powered resume analysis platform that compares resumes against job descriptions using semantic AI matching, skill extraction, experience analysis, and personalized improvement feedback.

The system uses transformer-based embeddings to understand the semantic similarity between resumes and jobs rather than relying only on keyword matching.

---

# Features

## Core Matching
- Resume upload (`PDF`, `DOCX`, `TXT`)
- Semantic similarity scoring using Sentence Transformers
- AI-powered job matching
- Fast semantic search with precomputed embeddings
- Final weighted match score

## Skill Analysis
- Automatic skill extraction
- Matched skill detection
- Missing skill identification
- Skill overlap scoring
- Skill gap analysis

## Experience Analysis
- Experience/year extraction
- Resume years vs required years comparison
- Experience match scoring

## AI Feedback
- GPT-powered resume feedback
- Resume strengths and weaknesses
- Personalized improvement suggestions
- Resume enhancement recommendations

## Resume Improvement Tools
- Resume Improvement Generator
- Skill Gap Roadmap Generator
- Learning path suggestions
- Recommendations for improving job compatibility

## Visualization
- Interactive Streamlit dashboard
- Score breakdown charts
- Progress bars and metrics
- Top job match tables

## Performance Improvements
- Fast semantic job retrieval
- Precomputed embedding support
- Hybrid scoring system
- Multi-stage ranking pipeline

---

# Technologies Used

- Python
- Streamlit
- Sentence Transformers
- OpenAI API
- Scikit-learn
- Pandas
- Altair
- NumPy

---

# Project Structure

```bash
project/
│
├── app.py
├── matcher.py
├── fast_matcher.py
├── feedback.py
├── gpt_feedback.py
├── resume_improver.py
├── skill_roadmap.py
├── file_utils.py
├── evaluate.py
│
├── data/
│   ├── job_descriptions.csv
│   ├── job_descriptions_clean.csv
│   └── job_embeddings.pkl
│
├── requirements.txt
└── README.md