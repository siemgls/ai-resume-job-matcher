import base64
import re
import urllib.parse
import pandas as pd
import streamlit as st
import altair as alt

from matcher import final_match_score
from feedback import generate_feedback
from file_utils import extract_resume_text
from gpt_feedback import generate_gpt_feedback
from resume_improver import generate_resume_improvements, generate_updated_resume, build_resume_pdf
from skill_roadmap import generate_skill_roadmap

try:
    from fast_matcher import find_top_jobs
    FAST_MATCHER_AVAILABLE = True
except Exception:
    FAST_MATCHER_AVAILABLE = False


for key, default in {
    "page": "home",
    "single_result": None,
    "single_job_text": "",
    "best_job": None,
    "results_df": None,
    "resume_text": "",
    "resume_bytes": None,
    "resume_filename": "",
    "resume_improvements": "",
    "skill_roadmap": "",
    "updated_resume_bytes": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def show_score_chart(scores, title):
    order = ["Semantic", "Skills", "Experience"]
    score_data = pd.DataFrame({"Metric": order, "Score": scores})
    chart = alt.Chart(score_data).mark_bar().encode(
        x=alt.X("Metric", sort=order),
        y=alt.Y("Score", scale=alt.Scale(domain=[0, 100]))
    ).properties(title=title)
    st.altair_chart(chart, use_container_width=True)


def extract_email_from_text(text):
    match = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else ""


def build_mailto_url(to, job_title, score, matched, missing, improvements):
    subject = f"Resume Match Results – {job_title}"

    improvements_section = ""
    if improvements:
        short = improvements[:800] + ("..." if len(improvements) > 800 else "")
        improvements_section = f"\n\nSuggested improvements for your resume:\n{short}"

    body = f"""Hi,

Your resume was analyzed against the following job:
Role: {job_title}
Overall match score: {score}%

Matched skills: {matched or 'None'}
Missing skills: {missing or 'None'}
{improvements_section}

Could you let us know:
1. Does this job interest you?
2. Are you happy with the suggested improvements?

Reply to this email with your thoughts.
"""
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body)
    return f"mailto:{to}?subject={encoded_subject}&body={encoded_body}"


def show_pdf(pdf_bytes):
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600px" type="application/pdf"></iframe>',
        unsafe_allow_html=True
    )


st.set_page_config(
    page_title="AI Resume-Job Matcher",
    page_icon="📄",
    layout="wide"
)

# ── RESULTS PAGE ──────────────────────────────────────────────────────────────
if st.session_state.page == "results":
    results_df = st.session_state.results_df
    best = st.session_state.best_job
    resume_text = st.session_state.resume_text

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.session_state.resume_improvements = ""
        st.session_state.skill_roadmap = ""
        st.rerun()

    st.title("Match Results")

    st.subheader("Top Matches")
    display_cols = ["job_title", "score", "semantic_score", "skill_score", "experience_score", "matched", "missing"]
    st.dataframe(results_df[display_cols].head(10), use_container_width=True)

    st.subheader("Best Job")
    col1, col2 = st.columns(2)
    col1.metric("Role", best["job_title"])
    col2.metric("Final Score", f"{best['score']}%")

    c1, c2, c3 = st.columns(3)
    c1.metric("Semantic", f"{best['semantic_score']}%")
    c2.metric("Skills", f"{best['skill_score']}%")
    c3.metric("Experience", f"{best['experience_score']}%")

    show_score_chart(
        [best["semantic_score"], best["skill_score"], best["experience_score"]],
        "Best Job Score Breakdown"
    )

    st.write("**Matched Skills:**", best["matched"] or "None")
    st.write("**Missing Skills:**", best["missing"] or "None")

    st.subheader("AI Feedback")
    with st.spinner("Generating AI feedback..."):
        gpt_feedback = generate_gpt_feedback(resume_text, best["job_description"])
    if gpt_feedback:
        st.write(gpt_feedback)
    else:
        st.info("GPT unavailable — using built-in feedback.")
        st.write(generate_feedback(
            best["score"], best["semantic_score"], best["skill_score"], best["missing_list"]
        ))

    st.subheader("Resume Improvement")
    if st.button("Generate Resume Improvements"):
        st.session_state.resume_improvements = generate_resume_improvements(
            resume_text, best["job_description"], best["job_title"], best["missing_list"]
        )
    if st.session_state.resume_improvements:
        st.write(st.session_state.resume_improvements)

        if st.button("Apply improvements to resume & download"):
            with st.spinner("Rewriting resume..."):
                updated_text = generate_updated_resume(resume_text, st.session_state.resume_improvements)
            if updated_text:
                st.session_state.updated_resume_bytes = build_resume_pdf(updated_text)
            else:
                st.error("Could not rewrite resume — check your API key.")

        if st.session_state.updated_resume_bytes:
            st.download_button(
                label="Download updated resume (PDF)",
                data=st.session_state.updated_resume_bytes,
                file_name="resume_updated.pdf",
                mime="application/pdf"
            )

    st.subheader("Skill Gap Roadmap")
    if st.button("Generate Skill Roadmap"):
        st.session_state.skill_roadmap = generate_skill_roadmap(best["missing_list"])
    if st.session_state.skill_roadmap:
        st.markdown(st.session_state.skill_roadmap)

    st.subheader("Send Results by Email")
    detected_email = extract_email_from_text(resume_text)
    recipient = st.text_input("Recipient email address", value=detected_email)

    if recipient:
        mailto = build_mailto_url(
            to=recipient,
            job_title=best["job_title"],
            score=best["score"],
            matched=best["matched"],
            missing=best["missing"],
            improvements=st.session_state.resume_improvements,
        )
        st.link_button("Open in mail client", mailto)

# ── HOME PAGE ─────────────────────────────────────────────────────────────────
else:
    st.title("AI Resume–Job Matching System")
    st.write("Upload a resume and match it to jobs automatically.")

    uploaded_resume = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    if uploaded_resume is not None:
        if uploaded_resume.name != st.session_state.resume_filename:
            st.session_state.single_result = None
            st.session_state.single_job_text = ""
            st.session_state.best_job = None
            st.session_state.results_df = None
            st.session_state.resume_improvements = ""
            st.session_state.skill_roadmap = ""
            st.session_state.updated_resume_bytes = None

        try:
            file_bytes = uploaded_resume.read()
            st.session_state.resume_bytes = file_bytes
            st.session_state.resume_filename = uploaded_resume.name
            uploaded_resume.seek(0)
            resume_text = extract_resume_text(uploaded_resume)
            st.session_state.resume_text = resume_text
            st.success("Resume extracted successfully")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    if st.session_state.resume_bytes:
        with st.expander("Preview Resume"):
            if st.session_state.resume_filename.lower().endswith(".pdf"):
                show_pdf(st.session_state.resume_bytes)
            else:
                st.write(st.session_state.resume_text[:2000])

    resume_text = st.session_state.resume_text

    mode = st.radio(
        "Choose mode",
        ["Compare with one job description", "Find best matching jobs automatically"],
        index=1
    )

    # ── SINGLE JOB MODE ───────────────────────────────────────────────────────
    if mode == "Compare with one job description":
        job_text = st.text_area("Paste Job Description", height=250)

        if st.button("Analyze Match"):
            if not resume_text or not job_text:
                st.warning("Upload resume and enter job description.")
            else:
                with st.spinner("Analyzing..."):
                    result = final_match_score(resume_text, job_text)
                st.session_state.single_result = result
                st.session_state.single_job_text = job_text
                st.session_state.resume_improvements = ""
                st.session_state.skill_roadmap = ""

        result = st.session_state.single_result
        saved_job_text = st.session_state.single_job_text

        if result is not None:
            st.subheader("Match Results")
            st.metric("Final Score", f"{result['final_score']}%")
            st.progress(min(int(result["final_score"]), 100))

            col1, col2, col3 = st.columns(3)
            col1.metric("Semantic", f"{result['semantic_score']}%")
            col2.metric("Skill Match", f"{result['skill_score']}%")
            col3.metric("Experience", f"{result['experience_score']}%")

            show_score_chart(
                [result["semantic_score"], result["skill_score"], result["experience_score"]],
                "Score Breakdown"
            )

            st.write(f"Resume Years: {result['resume_years']}")
            st.write(f"Required Years: {result['job_years']}")

            st.subheader("Skills")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write("Job Skills")
                st.write(result["job_skills"])
            with c2:
                st.write("Matched Skills")
                st.write(result["matched_skills"])
            with c3:
                st.write("Missing Skills")
                st.write(result["missing_skills"])

            st.subheader("Feedback")
            gpt_feedback = generate_gpt_feedback(resume_text, saved_job_text)
            if gpt_feedback:
                st.success("AI Feedback")
                st.write(gpt_feedback)
            else:
                st.info("Using built-in feedback because GPT is unavailable.")
                st.write(generate_feedback(
                    result["final_score"], result["semantic_score"],
                    result["skill_score"], result["missing_skills"]
                ))

            st.subheader("Resume Improvement")
            if st.button("Improve Resume"):
                st.session_state.resume_improvements = generate_resume_improvements(
                    resume_text, saved_job_text, "Custom Job", result["missing_skills"]
                )
            if st.session_state.resume_improvements:
                st.write(st.session_state.resume_improvements)

                if st.button("Apply improvements to resume & download"):
                    with st.spinner("Rewriting resume..."):
                        updated_text = generate_updated_resume(resume_text, st.session_state.resume_improvements)
                    if updated_text:
                        st.session_state.updated_resume_bytes = build_resume_pdf(updated_text)
                    else:
                        st.error("Could not rewrite resume — check your API key.")

                if st.session_state.updated_resume_bytes:
                    st.download_button(
                        label="Download updated resume (PDF)",
                        data=st.session_state.updated_resume_bytes,
                        file_name="resume_updated.pdf",
                        mime="application/pdf"
                    )

            st.subheader("Skill Gap Roadmap")
            if st.button("Generate Skill Roadmap"):
                st.session_state.skill_roadmap = generate_skill_roadmap(result["missing_skills"])
            if st.session_state.skill_roadmap:
                st.markdown(st.session_state.skill_roadmap)

    # ── AUTO MODE ─────────────────────────────────────────────────────────────
    else:
        if FAST_MATCHER_AVAILABLE:
            st.success("Fast matcher enabled")
        else:
            st.warning("Fast matcher not available. Falling back to slower mode.")

        top_k = st.slider(
            "How many top jobs to analyze in detail",
            min_value=5, max_value=50, value=25, step=5
        )

        if st.button("Find Best Jobs"):
            if not resume_text:
                st.warning("Upload a resume first.")
                st.stop()

            results = []

            if FAST_MATCHER_AVAILABLE:
                with st.spinner("Finding top jobs using precomputed embeddings..."):
                    candidate_jobs = find_top_jobs(resume_text, top_k=top_k)

                progress_bar = st.progress(0)
                with st.spinner("Running detailed scoring on top matches..."):
                    for i, job in enumerate(candidate_jobs, start=1):
                        result = final_match_score(resume_text, job["job_description"])
                        results.append({
                            "job_title": job["job_title"],
                            "job_description": job["job_description"],
                            "score": result["final_score"],
                            "semantic_score": result["semantic_score"],
                            "skill_score": result["skill_score"],
                            "experience_score": result["experience_score"],
                            "matched": ", ".join(result["matched_skills"]),
                            "missing": ", ".join(result["missing_skills"]),
                            "missing_list": result["missing_skills"],
                        })
                        progress_bar.progress(int((i / len(candidate_jobs)) * 100))
            else:
                try:
                    jobs_df = pd.read_csv("data/job_descriptions_clean.csv").head(100)
                except FileNotFoundError:
                    st.error("No job dataset found. Please add data/job_descriptions_clean.csv.")
                    st.stop()

                progress_bar = st.progress(0)
                with st.spinner("Scoring jobs slowly..."):
                    for i, row in jobs_df.iterrows():
                        result = final_match_score(resume_text, row["job_description"])
                        results.append({
                            "job_title": row.get("job_title", "Unknown Job"),
                            "job_description": row["job_description"],
                            "score": result["final_score"],
                            "semantic_score": result["semantic_score"],
                            "skill_score": result["skill_score"],
                            "experience_score": result["experience_score"],
                            "matched": ", ".join(result["matched_skills"]),
                            "missing": ", ".join(result["missing_skills"]),
                            "missing_list": result["missing_skills"],
                        })
                        progress_bar.progress(int(((i + 1) / len(jobs_df)) * 100))

            if not results:
                st.error("No jobs found.")
                st.stop()

            results_df = pd.DataFrame(results).sort_values(by="score", ascending=False)
            st.session_state.results_df = results_df
            st.session_state.best_job = results_df.iloc[0].to_dict()
            st.session_state.resume_improvements = ""
            st.session_state.skill_roadmap = ""
            st.session_state.page = "results"
            st.rerun()
