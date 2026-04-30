from sentence_transformers import SentenceTransformer, util
from skills import skill_match_score

# Lightweight transformer model suitable for laptops.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def clean_text(text: str) -> str:
    """Basic text cleaning."""
    text = text.lower()
    text = text.replace("\n", " ")
    return " ".join(text.split())


def semantic_similarity(resume_text: str, job_text: str) -> float:
    """Calculate semantic similarity between resume and job description."""
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    similarity = util.cos_sim(resume_embedding, job_embedding).item()
    return round(similarity * 100, 2)


def final_match_score(resume_text: str, job_text: str) -> dict:
    """Combine semantic similarity and skill matching into a final score."""
    semantic_score = semantic_similarity(resume_text, job_text)
    skill_result = skill_match_score(resume_text, job_text)

    # Weighted score: semantic meaning matters more than exact skill keywords.
    final_score = (0.7 * semantic_score) + (0.3 * skill_result["skill_score"])

    return {
        "semantic_score": semantic_score,
        "skill_score": skill_result["skill_score"],
        "final_score": round(final_score, 2),
        "resume_skills": skill_result["resume_skills"],
        "job_skills": skill_result["job_skills"],
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"]
    }
