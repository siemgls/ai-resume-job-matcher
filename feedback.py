def generate_feedback(final_score, semantic_score, skill_score, missing_skills):
    feedback = []

    # =====================
    # Overall summary
    # =====================
    feedback.append(f"Final match score: {final_score}%.")

    if final_score >= 80:
        feedback.append("Strong match for this role.")
    elif final_score >= 60:
        feedback.append("Moderate match. Some improvements will increase your chances.")
    else:
        feedback.append("Weak match. Resume needs significant improvement.")

    # =====================
    # Detailed explanation
    # =====================
    feedback.append(f"Semantic similarity: {semantic_score}% (how well your experience matches the job).")
    feedback.append(f"Skill match: {skill_score}% (overlap with required skills).")

    # =====================
    # Missing skills
    # =====================
    if missing_skills:
        feedback.append("Missing key skills: " + ", ".join(missing_skills))

        feedback.append("\nHow to improve your resume:")

        for skill in missing_skills[:5]:
            feedback.append(
                f"- Add {skill} with a real example (project, internship, or work experience)."
            )

        feedback.append("- Include measurable results (e.g., improved performance by X%).")
        feedback.append("- Use strong action verbs (Built, Developed, Optimized).")
        feedback.append("- Tailor your resume to match job keywords.")
    else:
        feedback.append("Great job — no major skills are missing.")

    return "\n".join(feedback)