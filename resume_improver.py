from gpt_feedback import generate_gpt_feedback


def generate_rule_based_improvements(job_title, missing_skills):
    if not missing_skills:
        return (
            "No major missing skills were detected. To improve the resume further, "
            "add stronger measurable achievements, clearer project descriptions, "
            "and keywords from the job description."
        )

    lines = []
    lines.append(f"Resume improvement suggestions for: {job_title}")
    lines.append("")
    lines.append("Suggested resume additions:")

    for skill in missing_skills[:5]:
        lines.append(
            f"- Add a bullet showing experience with {skill}, for example: "
            f"'Applied {skill} in a project to solve a practical problem and improve results.'"
        )

    lines.append("")
    lines.append("General improvements:")
    lines.append("- Add measurable results such as percentages, time saved, or users supported.")
    lines.append("- Use action verbs such as Built, Developed, Improved, Automated, Designed, or Optimized.")
    lines.append("- Tailor your summary section to include keywords from the job description.")

    return "\n".join(lines)


def generate_resume_improvements(resume_text, job_description, job_title, missing_skills):
    gpt_result = generate_gpt_feedback(
        resume_text,
        f"""
Job title: {job_title}

Job description:
{job_description}

Missing skills:
{missing_skills}

Generate resume improvement suggestions:
1. Rewrite the resume summary in 2-3 sentences.
2. Suggest 3 strong resume bullet points.
3. Suggest project ideas for missing skills.
"""
    )

    if gpt_result:
        return gpt_result

    return generate_rule_based_improvements(job_title, missing_skills)