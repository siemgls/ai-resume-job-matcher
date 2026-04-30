from matcher import final_match_score

def rank_resumes(job_description, resumes):
    results = []

    for resume in resumes:
        score = final_match_score(resume, job_description)["final_score"]
        results.append((resume, score))

    # Sort by score descending
    ranked = sorted(results, key=lambda x: x[1], reverse=True)

    return ranked