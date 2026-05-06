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
{resume_text[:2000]}

Job Description:
{job_description[:2000]}

Return structured feedback:

1. Strengths
- What matches well

2. Weaknesses
- What is missing or weak

3. Improvements (MOST IMPORTANT)
- Exact skills to add
- Example projects to include
- Specific resume bullet improvements

Be specific and practical.
Avoid generic advice like "improve your resume".
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        # Better UX than silent failure
        return None