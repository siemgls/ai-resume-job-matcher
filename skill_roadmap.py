import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ROADMAP = {
    "python": "Build 2 small Python projects and practice APIs, file handling, and data processing.",
    "sql": "Practice SELECT, JOIN, GROUP BY, subqueries, and indexing using a sample database.",
    "aws": "Learn EC2, S3, IAM, and deploy one small web app to AWS.",
    "docker": "Containerize a Python or web app and write a Dockerfile plus docker-compose file.",
    "kubernetes": "Learn pods, deployments, services, and deploy a containerized app locally with Minikube.",
    "machine learning": "Train and evaluate models using scikit-learn, then document results.",
    "react": "Build a small frontend app with components, state, props, and API calls.",
    "javascript": "Practice async/await, fetch API, DOM manipulation, and build an interactive app.",
    "typescript": "Convert a JavaScript project to TypeScript and use interfaces and types properly.",
    "git": "Practice branching, pull requests, merge conflicts, and clean commit messages.",
    "linux": "Practice terminal commands, permissions, processes, and shell scripting.",
    "ci/cd": "Create a GitHub Actions pipeline that runs tests and deploys a small app.",
}


def generate_gpt_roadmap(missing_skills):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)

        skills_list = ", ".join(missing_skills[:6])

        prompt = f"""You are a career coach helping someone close skill gaps for a job application.

Missing skills: {skills_list}

For each missing skill provide:
1. A concrete 1-2 sentence learning plan (specific resources, project ideas, or practice approach)
2. One resume bullet point they could add after learning it

Then suggest a focused 2-week action plan to tackle the top 2 skills.

Format your response in clear markdown with a header per skill."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception:
        return None


def generate_rule_based_roadmap(missing_skills):
    lines = []
    lines.append("### Skill Gap Roadmap")
    lines.append("")
    lines.append("To improve your match for this job, focus on these missing skills:")
    lines.append("")

    for skill in missing_skills[:6]:
        suggestion = ROADMAP.get(
            skill.lower(),
            f"Study {skill}, complete a small practical project, and add it to your resume with a clear result."
        )
        lines.append(f"**{skill}**")
        lines.append(f"- Learning plan: {suggestion}")
        lines.append(f"- Resume action: Add one bullet point showing how you used {skill}.")
        lines.append("")

    lines.append("### Suggested 2-week plan")
    lines.append("- Days 1–3: Learn the basics of the top missing skill.")
    lines.append("- Days 4–7: Build a small project using that skill.")
    lines.append("- Days 8–10: Add another missing skill or improve the same project.")
    lines.append("- Days 11–14: Update your resume with project bullets and measurable results.")

    return "\n".join(lines)


def generate_skill_roadmap(missing_skills):
    if not missing_skills:
        return (
            "No major missing skills were detected. Focus on improving impact: "
            "add metrics, stronger action verbs, and more specific examples connected to the job requirements."
        )

    gpt_result = generate_gpt_roadmap(missing_skills)
    if gpt_result:
        return gpt_result

    return generate_rule_based_roadmap(missing_skills)
