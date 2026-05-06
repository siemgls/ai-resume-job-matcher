import re


def extract_years(text):
    text = text.lower()

    patterns = [
        r"(\d+)\+?\s*years",
        r"(\d+)\+?\s*yrs",
        r"(\d+)\+?\s*year"
    ]

    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                years.append(int(match))
            except ValueError:
                pass

    return max(years) if years else 0


def experience_match_score(resume_text, job_text):
    resume_years = extract_years(resume_text)
    job_years = extract_years(job_text)

    if job_years == 0:
        return {
            "experience_score": 100,
            "resume_years": resume_years,
            "job_years": job_years
        }

    score = min(resume_years / job_years, 1.0) * 100

    return {
        "experience_score": round(score, 2),
        "resume_years": resume_years,
        "job_years": job_years
    }