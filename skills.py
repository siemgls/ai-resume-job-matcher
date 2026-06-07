from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "fine_tuned_model"

embedding_model = SentenceTransformer(MODEL_NAME)
kw_model = KeyBERT(model=embedding_model)

KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "mysql", "postgresql",
    "machine learning", "deep learning", "nlp", "pytorch", "tensorflow",
    "scikit-learn", "pandas", "numpy", "aws", "azure", "docker", "kubernetes",
    "git", "github", "linux", "react", "html", "css", "node.js", "spring boot",
    "rest api", "microservices", "ci/cd", "power bi", "tableau",
    "figma", "photoshop", "agile", "scrum", "jira", "cybersecurity", "siem",
    "incident response", "data analysis", "data visualization", "cloud computing",
    "api development"
]


def extract_candidate_skills(text, top_n=25):
    text = text.lower()

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=top_n
    )

    return [kw[0] for kw in keywords]


def map_to_known_skills(candidate_phrases, threshold=0.55):
    found_skills = set()

    if not candidate_phrases:
        return found_skills

    phrase_embeddings = embedding_model.encode(candidate_phrases, convert_to_tensor=True)
    skill_embeddings = embedding_model.encode(KNOWN_SKILLS, convert_to_tensor=True)

    similarity_matrix = util.cos_sim(phrase_embeddings, skill_embeddings)

    for i, _ in enumerate(candidate_phrases):
        best_match_index = similarity_matrix[i].argmax().item()
        best_score = similarity_matrix[i][best_match_index].item()

        if best_score >= threshold:
            found_skills.add(KNOWN_SKILLS[best_match_index])

    return found_skills


def find_skills(text):
    candidate_phrases = extract_candidate_skills(text)
    skills = map_to_known_skills(candidate_phrases)

    # fallback: also catch exact known skill names
    text_lower = text.lower()
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            skills.add(skill)

    return skills


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

    job_coverage = len(matched_skills) / len(job_skills)
    resume_relevance = len(matched_skills) / len(resume_skills) if resume_skills else 0
    score = (0.7 * job_coverage + 0.3 * resume_relevance) * 100

    return {
        "skill_score": round(score, 2),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }