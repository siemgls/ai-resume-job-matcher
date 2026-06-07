import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_gpt_improvements(resume_text, job_description, job_title, missing_skills):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""You are an expert resume coach.

Resume:
{resume_text[:4000]}

Job Title: {job_title}
Job Description:
{job_description[:1500]}

Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

Provide ONLY the following — do not repeat general career feedback:
1. Rewrite the resume summary in 2-3 sentences tailored to this specific job.
2. Write 3 strong resume bullet points the candidate could add for this role.
3. Suggest 1-2 small project ideas to address missing skills.

Be concrete and specific to this job. Do not list strengths or weaknesses."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception:
        return None


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
    gpt_result = generate_gpt_improvements(resume_text, job_description, job_title, missing_skills)

    if gpt_result:
        return gpt_result

    return generate_rule_based_improvements(job_title, missing_skills)


def generate_updated_resume(resume_text, improvements):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""You are an expert resume writer.

Original resume:
{resume_text[:3000]}

Improvement suggestions to apply:
{improvements[:2000]}

Rewrite the full resume incorporating these suggestions.
Keep the same person's real background — do not invent experience they don't have.
Only improve how it is presented: enhance bullet points, update the summary, and add suggested skills where plausible.
Return the complete rewritten resume as plain text with clear section headers (e.g. Profile, Experience, Skills, Education).
Do not add any commentary — return only the resume text."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception:
        return None


def build_resume_pdf(resume_text):
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    heading = ParagraphStyle("heading", fontSize=12, fontName="Helvetica-Bold",
                             spaceBefore=10, spaceAfter=4)
    body = ParagraphStyle("body", fontSize=9, fontName="Helvetica",
                          spaceAfter=3, leading=13)

    story = []
    for line in resume_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
        elif stripped.isupper() or stripped.endswith(":"):
            story.append(Paragraph(stripped, heading))
        else:
            story.append(Paragraph(stripped.replace("&", "&amp;"), body))

    doc.build(story)
    return buffer.getvalue()