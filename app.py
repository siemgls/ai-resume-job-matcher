import streamlit as st
from matcher import final_match_score
from feedback import generate_feedback

st.set_page_config(
    page_title="AI Resume-Job Matcher",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume–Job Matching System")
st.write("Compare a resume with a job description using a fine-tuned transformer model.")

col1, col2 = st.columns(2)

with col1:
    resume_text = st.text_area("Paste Resume Text", height=300)

with col2:
    job_text = st.text_area("Paste Job Description", height=300)

if st.button("Analyze Match"):
    if not resume_text or not job_text:
        st.warning("Please enter both a resume and a job description.")
    else:
        result = final_match_score(resume_text, job_text)

        st.subheader("Match Results")

        st.metric("Final Match Score", f"{result['final_score']}%")
        st.progress(int(result["final_score"]))

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Semantic Similarity", f"{result['semantic_score']}%")

        with col2:
            st.metric("Skill Match", f"{result['skill_score']}%")

        st.subheader("Skill Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Job Skills")
            st.write(result["job_skills"])

        with col2:
            st.write("Matched Skills")
            st.write(result["matched_skills"])

        with col3:
            st.write("Missing Skills")
            st.write(result["missing_skills"])

        st.subheader("Feedback")
        feedback = generate_feedback(
            result["final_score"],
            result["semantic_score"],
            result["skill_score"],
            result["missing_skills"]
        )
        st.write(feedback)