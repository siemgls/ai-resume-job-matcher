SKILL_MAP = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "sql": ["sql", "mysql", "postgresql"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "neural networks"],
    "nlp": ["nlp", "natural language processing"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github"],
    "linux": ["linux"],
    "react": ["react", "react.js", "reactjs"],
    "html": ["html"],
    "css": ["css"],
    "api": ["api", "rest api", "rest"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "excel": ["excel"],
    "figma": ["figma"],
    "photoshop": ["photoshop"],
    "communication": ["communication"],
    "leadership": ["leadership"],
    "agile": ["agile", "scrum"],
    "jira": ["jira"],
    "cybersecurity": ["cybersecurity", "security"],
    "siem": ["siem"],
    "incident response": ["incident response"],
}


def find_skills(text):
    text = text.lower()
    found_skills = set()

    for skill, synonyms in SKILL_MAP.items():
        for synonym in synonyms:
            if synonym in text:
                found_skills.add(skill)
                break

    return found_skills


def skill_match_score(resume_text, job_text):
    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_text)

    if not job_skills:
        return {
            "skill_score": 0,
            "resume_skills": sorted(resume_skills),
            "job_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    score = len(matched_skills) / len(job_skills) * 100

    return {
        "skill_score": round(score, 2),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }