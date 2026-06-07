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

Return ONLY the resume text using this exact format — no extra commentary:

Line 1: Full name only
Line 2: City, Country | email@example.com | phone number
Line 3: blank

Then use ALL CAPS for every section header (e.g. PROFILE, EXPERIENCE, SKILLS, EDUCATION, CERTIFICATIONS, PROJECTS).
Under each job write the job title and company on one line, then the date range on the next line.
Use • for every bullet point.
Leave a blank line between each job or section block."""

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
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    DARK    = colors.HexColor("#2c3e50")
    GREY    = colors.HexColor("#666666")
    ACCENT  = colors.HexColor("#2980b9")

    name_style = ParagraphStyle("name", fontSize=22, fontName="Helvetica-Bold",
                                alignment=TA_CENTER, spaceAfter=4, textColor=DARK)
    contact_style = ParagraphStyle("contact", fontSize=9, fontName="Helvetica",
                                   alignment=TA_CENTER, spaceAfter=12, textColor=GREY)
    section_style = ParagraphStyle("section", fontSize=11, fontName="Helvetica-Bold",
                                   spaceBefore=14, spaceAfter=4, textColor=ACCENT)
    job_title_style = ParagraphStyle("job_title", fontSize=10, fontName="Helvetica-Bold",
                                     spaceAfter=1, textColor=DARK)
    date_style = ParagraphStyle("date", fontSize=9, fontName="Helvetica-Oblique",
                                spaceAfter=3, textColor=GREY)
    body_style = ParagraphStyle("body", fontSize=9, fontName="Helvetica",
                                spaceAfter=3, leading=13, textColor=DARK)
    bullet_style = ParagraphStyle("bullet", fontSize=9, fontName="Helvetica",
                                  spaceAfter=3, leading=13, leftIndent=12, textColor=DARK)

    lines = resume_text.split("\n")
    story = []
    i = 0

    # First line = name, second line = contact
    if lines:
        name_line = lines[0].strip()
        if name_line:
            story.append(Paragraph(name_line, name_style))
        i = 1

    if i < len(lines):
        contact_line = lines[i].strip()
        if contact_line and not contact_line.isupper():
            story.append(Paragraph(contact_line.replace("|", " • ").replace("&", "&amp;"), contact_style))
            i += 1

    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=6))

    section_keywords = {
        "PROFILE", "SUMMARY", "EXPERIENCE", "WORK EXPERIENCE", "SKILLS",
        "EDUCATION", "CERTIFICATIONS", "PROJECTS", "LANGUAGES", "AWARDS"
    }

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        clean = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        i += 1

        if not stripped:
            story.append(Spacer(1, 4))
            continue

        upper = stripped.upper().rstrip(":").strip()
        if upper in section_keywords or (stripped.isupper() and len(stripped) > 2):
            story.append(Paragraph(stripped.rstrip(":"), section_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT, spaceAfter=5))
            continue

        if stripped.startswith("•") or stripped.startswith("-"):
            bullet_text = clean.lstrip("•- ").strip()
            story.append(Paragraph(f"• {bullet_text}", bullet_style))
            continue

        # Detect date lines (contain year patterns)
        import re
        if re.search(r'\b(19|20)\d{2}\b', stripped) and len(stripped) < 60:
            story.append(Paragraph(clean, date_style))
            continue

        # Lines with a dash separator are likely job title — company lines
        if " — " in stripped or " - " in stripped:
            story.append(Paragraph(clean, job_title_style))
        else:
            story.append(Paragraph(clean, body_style))

    doc.build(story)
    return buffer.getvalue()