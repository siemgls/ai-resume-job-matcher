SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "nosql",
    "machine learning", "deep learning", "nlp", "natural language processing",
    "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy",
    "data analysis", "data visualization", "power bi", "tableau",
    "aws", "azure", "google cloud", "docker", "kubernetes",
    "git", "linux", "api", "rest api", "flask", "django",
    "react", "node.js", "html", "css",
    "communication", "leadership", "problem solving", "teamwork"
]

def find_skills(text: str) -> set[str]:
    """Find known skills mentioned in text using simple keyword matching."""
    text = text.lower()
    found = set()

    for skill in SKILLS:
        if skill in text:
            found.add(skill)

    return found


def skill_match_score(resume_text: str, job_text: str) -> dict:
    """Compare skills in resume and job description."""
    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_text)

    if not job_skills:
        return {
            "skill_score": 0.0,
            "resume_skills": sorted(resume_skills),
            "job_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    score = (len(matched_skills) / len(job_skills)) * 100

    return {
        "skill_score": round(score, 2),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }
