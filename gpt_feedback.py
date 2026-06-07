import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_gpt_feedback(resume_text, job_description):
    api_key = os.getenv("OPENAI_API_KEY")

    # No API key → fallback
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are an expert career coach.

Analyze the resume against the job description.

Resume:
{resume_text[:4000]}

Job Description:
{job_description[:2000]}

Return structured feedback with exactly two sections:

1. Strengths
- What matches well between the resume and the job

2. Weaknesses
- What is missing or weak compared to the job requirements

Be specific and practical. Do not include improvement suggestions or action items.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception:
        # Better UX than silent failure
        return None