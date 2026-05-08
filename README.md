# AI Resume-Job Matching System

## Overview

The AI Resume–Job Matching System is an intelligent recruitment assistant that analyzes how well a resume matches a job description using Natural Language Processing (NLP), transformer embeddings, semantic similarity, and AI-generated feedback.

The application helps users:
- Compare resumes with job descriptions
- Detect matched and missing skills
- Evaluate experience relevance
- Generate resume improvement suggestions
- Create personalized skill gap roadmaps
- Find the best matching jobs automatically

The project uses transformer-based embeddings with semantic search to simulate modern AI recruitment systems.

---

# Features

## Resume Analysis
- Upload resumes in:
  - PDF
  - DOCX
  - TXT

## Semantic Matching
- Uses Sentence Transformers to compare semantic meaning between resumes and jobs
- Detects relevance even when wording differs

## AI Skill Extraction
- Automatically extracts technical and professional skills
- Detects:
  - Matched skills
  - Missing skills

## Experience Detection
- Extracts years of experience from:
  - Resume
  - Job description
- Calculates an experience match score

## Final AI Match Score
The final score combines:
- Semantic similarity
- Skill overlap
- Experience relevance

## GPT Feedback
Uses OpenAI GPT models to generate:
- Strengths
- Weaknesses
- Resume advice
- Improvement suggestions

## Resume Improvement Generator
Generates:
- Better bullet points
- Stronger achievement descriptions
- Resume optimization suggestions

## Skill Gap Roadmap
Creates a personalized learning roadmap for missing skills:
- What to learn
- Learning priorities
- Suggested improvement direction

## Fast Semantic Job Search
Precomputed embeddings allow fast matching against large job datasets.

## Interactive Dashboard
Built using Streamlit:
- Score charts
- Progress bars
- Interactive tables
- AI feedback sections

---

# Technologies Used

- Python
- Streamlit
- Sentence Transformers
- OpenAI API
- Pandas
- Scikit-learn
- Altair

---

# AI & NLP Techniques Used

## Semantic Similarity
Model:
```text
all-MiniLM-L6-v2

Used for:

Resume embeddings
Job description embeddings
Cosine similarity scoring
Skill Matching

Custom NLP-based skill extraction system:

Skill detection
Skill overlap scoring
Missing skill analysis
Experience Matching

Regex and NLP-based extraction of:

Years of experience
Required experience
Experience scoring
GPT-Based Feedback

OpenAI GPT models generate:

Resume feedback
Career coaching suggestions
Resume improvements
Learning roadmaps
Scoring System

The final score combines:

Component	Weight
Semantic Similarity	50%
Skill Match	35%
Experience Match	15%
Project Structure
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
├── generate_embeddings.py
│
├── data/
│   ├── job_descriptions.csv
│   ├── job_descriptions_clean.csv
│   └── job_embeddings.pkl
│
├── requirements.txt
└── README.md
Running the Application
1. Install dependencies
pip install -r requirements.txt
2. Add your OpenAI API key

Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here

This is required for:

GPT feedback
Resume improvement suggestions
Skill roadmap generation
3. Start the Streamlit app
streamlit run app.py

The application will open automatically in your browser.

4. Optional: Enable Fast Semantic Search

Generate precomputed job embeddings:

python generate_embeddings.py

This creates:

data/job_embeddings.pkl

which enables much faster job matching.

5. Optional: Run Evaluation
python evaluate.py

Evaluation includes:

Accuracy
Precision
Recall
F1 score
Example Workflow
Single Job Mode
Upload resume
Paste job description
Analyze match
Receive:
Match score
Missing skills
AI feedback
Resume improvements
Skill roadmap
Automatic Job Matching Mode
Upload resume
Search entire job dataset
Find top matching jobs
Receive:
Ranked job recommendations
Match scores
AI optimization suggestions
Evaluation

The system was evaluated using manually labeled resume-job pairs.

Metrics used:

Accuracy
Precision
Recall
F1 Score

Fine-tuning and improved scoring significantly increased matching quality.

Future Improvements

Potential future upgrades:

Advanced NLP skill extraction
Resume section analysis
ATS compatibility scoring
Multi-resume ranking
Cover letter generation
Interview preparation assistant
Real-time job API integration
PDF export for reports
Vector database integration
RAG-based AI recruiter assistant
Author

Developed as an AI/NLP project focused on intelligent recruitment systems, semantic search, and resume optimization.