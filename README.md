# AI Resume-to-Job Matching System

This project evaluates how well a resume matches a job description.

## Features

- Semantic similarity using a transformer model
- Skill detection
- Missing skills identification
- Final match score
- Readable feedback
- Simple Streamlit interface
- Basic evaluation script

## Setup

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

## Run Evaluation

```bash
python evaluate.py
```

## Current Model

The MVP uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This is a lightweight transformer model suitable for semantic similarity tasks.

## Next Improvements

- Add a larger resume/job dataset
- Fine-tune the sentence transformer
- Add LLM API feedback
- Improve skill extraction using NLP instead of keyword matching
- Add PDF resume upload
