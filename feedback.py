def generate_feedback(final_score, semantic_score, skill_score, missing_skills):
    feedback = []

    feedback.append(f"The resume received a final match score of {final_score}%.")

    if final_score >= 80:
        feedback.append("This appears to be a strong match for the job description.")
    elif final_score >= 60:
        feedback.append("This appears to be a moderate match, but there is room for improvement.")
    else:
        feedback.append("This appears to be a weak match for the job description.")

    feedback.append(
        f"The semantic similarity score is {semantic_score}%, which shows how closely the resume and job description match in meaning."
    )

    feedback.append(
        f"The skill match score is {skill_score}%, based on the overlap between required job skills and resume skills."
    )

    if missing_skills:
        feedback.append(
            "The main missing skills are: " + ", ".join(missing_skills) + "."
        )
    else:
        feedback.append("No major required skills were missing from the resume.")

    return " ".join(feedback)