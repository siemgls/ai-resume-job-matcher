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
    "communication": "Improve resume bullets by explaining impact clearly and using measurable outcomes.",
}


def generate_skill_roadmap(missing_skills):
    if not missing_skills:
        return (
            "No major missing skills were detected. Focus on improving impact: "
            "add metrics, stronger action verbs, and more specific examples connected to the job requirements."
        )

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