def generate_feedback(result: dict) -> str:
    """Generate simple readable feedback without requiring an external API."""
    final_score = result["final_score"]
    semantic_score = result["semantic_score"]
    skill_score = result["skill_score"]
    missing_skills = result["missing_skills"]
    matched_skills = result["matched_skills"]

    feedback = []

    feedback.append(f"The resume received a final match score of {final_score}%.")
    feedback.append(f"The semantic similarity score is {semantic_score}%, which shows how closely the resume matches the job description in meaning.")
    feedback.append(f"The skill match score is {skill_score}% based on the detected job requirements.")

    if matched_skills:
        feedback.append("The resume matches these important skills: " + ", ".join(matched_skills) + ".")

    if missing_skills:
        feedback.append("The resume may be missing or not clearly showing these skills: " + ", ".join(missing_skills) + ".")
    else:
        feedback.append("The resume includes most of the detected skills from the job description.")

    if final_score >= 80:
        feedback.append("Overall, this looks like a strong match for the job.")
    elif final_score >= 60:
        feedback.append("Overall, this looks like a moderate match. The resume could be improved by emphasizing missing skills and relevant experience.")
    else:
        feedback.append("Overall, this looks like a weak match. The applicant may need more relevant skills or experience for this role.")

    return "\n\n".join(feedback)
