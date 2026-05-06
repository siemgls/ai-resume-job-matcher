from sentence_transformers import SentenceTransformer, util
from skills import skill_match_score
from experience import experience_match_score

MODEL_NAME = "fine_tuned_model"
model = SentenceTransformer(MODEL_NAME)


def clean_text(text: str) -> str:
    text = text.lower()
    text = text.replace("\n", " ")
    return " ".join(text.split())


def semantic_similarity(resume_text: str, job_text: str) -> float:
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    similarity = util.cos_sim(resume_embedding, job_embedding).item()
    return round(similarity * 100, 2)


def final_match_score(resume_text: str, job_text: str) -> dict:
    semantic_score = semantic_similarity(resume_text, job_text)
    skill_result = skill_match_score(resume_text, job_text)
    experience_result = experience_match_score(resume_text, job_text)

    final_score = (
        0.60 * semantic_score +
        0.25 * skill_result["skill_score"] +
        0.15 * experience_result["experience_score"]
    )

    return {
        "semantic_score": semantic_score,
        "skill_score": skill_result["skill_score"],
        "experience_score": experience_result["experience_score"],
        "resume_years": experience_result["resume_years"],
        "job_years": experience_result["job_years"],
        "final_score": round(final_score, 2),
        "resume_skills": skill_result["resume_skills"],
        "job_skills": skill_result["job_skills"],
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"]
    }