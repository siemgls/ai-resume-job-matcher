import pandas as pd
import streamlit as st

from matcher import final_match_score
from feedback import generate_feedback
from file_utils import extract_resume_text
from gpt_feedback import generate_gpt_feedback

st.set_page_config(
    page_title="AI Resume-Job Matcher",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume–Job Matching System")
st.write("Upload a resume and match it to jobs automatically.")

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

resume_text = ""

if uploaded_resume is not None:
    try:
        resume_text = extract_resume_text(uploaded_resume)
        st.success("Resume extracted successfully")

        with st.expander("Preview Resume"):
            st.write(resume_text[:2000])
    except Exception as e:
        st.error(f"Error reading file: {e}")

mode = st.radio(
    "Choose mode",
    [
        "Compare with one job description",
        "Find best matching jobs automatically"
    ]
)

if mode == "Compare with one job description":

    job_text = st.text_area("Paste Job Description", height=250)

    if st.button("Analyze Match"):
        if not resume_text or not job_text:
            st.warning("Upload resume and enter job description.")
        else:
            with st.spinner("Analyzing resume and job description..."):
                result = final_match_score(resume_text, job_text)

            st.subheader("Match Results")
            st.metric("Final Score", f"{result['final_score']}%")
            st.progress(min(int(result["final_score"]), 100))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Semantic Score", f"{result['semantic_score']}%")

            with col2:
                st.metric("Skill Match", f"{result['skill_score']}%")

            with col3:
                st.metric("Experience Match", f"{result['experience_score']}%")

            st.write(f"Resume Years Detected: {result['resume_years']}")
            st.write(f"Job Years Required: {result['job_years']}")

            st.subheader("Skills")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("Job Skills")
                st.write(result["job_skills"])

            with col2:
                st.write("Matched")
                st.write(result["matched_skills"])

            with col3:
                st.write("Missing")
                st.write(result["missing_skills"])

            st.subheader("Feedback")

            with st.spinner("Trying GPT feedback..."):
                gpt_feedback = generate_gpt_feedback(
                    resume_text,
                    job_text
                )

            if gpt_feedback:
                st.success("AI Feedback")
                st.write(gpt_feedback)
            else:
                st.info("Using built-in feedback because GPT is unavailable.")
                basic_feedback = generate_feedback(
                    result["final_score"],
                    result["semantic_score"],
                    result["skill_score"],
                    result["missing_skills"]
                )
                st.write(basic_feedback)

else:

    st.write("Using built-in job dataset. You can optionally upload your own CSV.")

    job_file = st.file_uploader("Upload custom job CSV", type=["csv"])

    if job_file is not None:
        jobs_df = pd.read_csv(job_file)
        st.info("Using uploaded job dataset")
    else:
        try:
            jobs_df = pd.read_csv("data/job_descriptions_clean.csv")
            st.info("Using cleaned built-in dataset: data/job_descriptions_clean.csv")
        except FileNotFoundError:
            try:
                jobs_df = pd.read_csv("data/job_descriptions.csv")
                st.warning("Using raw built-in dataset: data/job_descriptions.csv")
            except FileNotFoundError:
                jobs_df = None
                st.error("No job dataset found. Please add data/job_descriptions_clean.csv or upload a CSV.")

    if jobs_df is not None:

        jobs_df.columns = [c.strip().lower() for c in jobs_df.columns]

        if "job_title" not in jobs_df.columns:
            jobs_df["job_title"] = "Unknown Job"

        if "job_description" not in jobs_df.columns:
            st.error("Dataset must contain a job_description column.")
            st.stop()

        jobs_df = jobs_df.dropna(subset=["job_description"])
        jobs_df["job_description"] = jobs_df["job_description"].astype(str)
        jobs_df["job_title"] = jobs_df["job_title"].astype(str)

        max_jobs = st.slider(
            "Number of jobs to compare",
            min_value=50,
            max_value=min(500, len(jobs_df)),
            value=min(300, len(jobs_df)),
            step=50
        )

        jobs_df = jobs_df.head(max_jobs)

        st.write(f"Loaded {len(jobs_df)} jobs")
        st.dataframe(jobs_df[["job_title", "job_description"]].head(20))

        if st.button("Find Best Jobs"):

            if not resume_text:
                st.warning("Upload a resume first")
            else:
                results = []

                progress_bar = st.progress(0)
                status_text = st.empty()

                with st.spinner("Scoring jobs..."):
                    total_jobs = len(jobs_df)

                    for i, (_, row) in enumerate(jobs_df.iterrows(), start=1):
                        job_desc = str(row["job_description"])

                        try:
                            result = final_match_score(resume_text, job_desc)

                            results.append({
                                "job_title": row["job_title"],
                                "job_description": job_desc,
                                "score": result["final_score"],
                                "semantic_score": result["semantic_score"],
                                "skill_score": result["skill_score"],
                                "experience_score": result["experience_score"],
                                "resume_years": result["resume_years"],
                                "job_years": result["job_years"],
                                "matched": ", ".join(result["matched_skills"]),
                                "missing": ", ".join(result["missing_skills"]),
                                "missing_list": result["missing_skills"],
                            })

                        except Exception:
                            continue

                        progress = int((i / total_jobs) * 100)
                        progress_bar.progress(progress)
                        status_text.write(f"Processed {i}/{total_jobs} jobs")

                if not results:
                    st.error("No jobs could be scored.")
                    st.stop()

                results_df = pd.DataFrame(results)
                results_df = results_df.sort_values(by="score", ascending=False)

                st.subheader("Top Matches")
                st.dataframe(
                    results_df[
                        [
                            "job_title",
                            "score",
                            "semantic_score",
                            "skill_score",
                            "experience_score",
                            "resume_years",
                            "job_years",
                            "matched",
                            "missing"
                        ]
                    ].head(10)
                )

                best = results_df.iloc[0]

                st.subheader("Best Job Recommendation")
                st.metric("Job", best["job_title"])
                st.metric("Score", f"{best['score']}%")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Semantic Score", f"{best['semantic_score']}%")

                with col2:
                    st.metric("Skill Score", f"{best['skill_score']}%")

                with col3:
                    st.metric("Experience Score", f"{best['experience_score']}%")

                st.write(f"Resume Years Detected: {best['resume_years']}")
                st.write(f"Job Years Required: {best['job_years']}")

                st.write("Matched Skills:")
                st.write(best["matched"])

                st.write("Missing Skills:")
                st.write(best["missing"])

                st.subheader("Feedback")

                with st.spinner("Trying GPT feedback..."):
                    gpt_feedback = generate_gpt_feedback(
                        resume_text,
                        best["job_description"]
                    )

                if gpt_feedback:
                    st.success("AI Feedback")
                    st.write(gpt_feedback)
                else:
                    st.info("Using built-in feedback because GPT is unavailable.")
                    basic_feedback = generate_feedback(
                        best["score"],
                        best["semantic_score"],
                        best["skill_score"],
                        best["missing_list"]
                    )
                    st.write(basic_feedback)