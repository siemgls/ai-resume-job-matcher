import streamlit as st
from matcher import final_match_score
from feedback import generate_feedback

st.set_page_config(page_title="AI Resume Job Matcher", page_icon="📄")

st.title("AI Resume-to-Job Matching System")
st.write("Paste a resume and a job description to calculate a match score and identify missing skills.")

resume_text = st.text_area("Paste Resume Text", height=250)
job_text = st.text_area("Paste Job Description", height=250)

if st.button("Analyze Match"):
    if not resume_text.strip() or not job_text.strip():
        st.warning("Please enter both a resume and a job description.")
    else:
        with st.spinner("Analyzing..."):
            result = final_match_score(resume_text, job_text)

        st.subheader("Match Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Final Match Score", f"{result['final_score']}%")
        col2.metric("Semantic Score", f"{result['semantic_score']}%")
        col3.metric("Skill Score", f"{result['skill_score']}%")

        st.subheader("Detected Skills")
        st.write("**Job Skills:**", result["job_skills"])
        st.write("**Resume Skills:**", result["resume_skills"])
        st.write("**Matched Skills:**", result["matched_skills"])

        st.subheader("Missing Skills")
        if result["missing_skills"]:
            st.write(result["missing_skills"])
        else:
            st.success("No missing skills detected from the current skill list.")

        st.subheader("AI Feedback")
        st.write(generate_feedback(result))
