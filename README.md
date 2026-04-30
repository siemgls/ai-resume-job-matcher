# AI Resume-Job Matching System

This project is an AI-based system that evaluates how well a resume matches a job description.

The system compares the semantic meaning of both texts using a transformer-based model and gives a match score. It also detects important skills from the job description and identifies which skills are missing from the resume.

## Features

- Resume and job description input
- Semantic similarity score using Sentence Transformers
- Skill detection
- Missing skill identification
- Final match score
- Simple feedback for the user
- Evaluation using accuracy and F1 score

## Technologies Used

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Pandas

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt