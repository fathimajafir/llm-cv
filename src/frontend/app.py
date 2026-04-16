import streamlit as st
import requests

st.title("AI CV Screener")
st.caption("Paste a job description, upload CVs — get ranked candidates instantly")

jd = st.text_area("Job Description", height=200,
                   placeholder="Paste the full job description here...")
cvs = st.file_uploader("Upload CV(s)", accept_multiple_files=True, type=["pdf"])

if st.button("Screen Candidates") and cvs and jd:
    with st.spinner("Analyzing..."):
        files = [("cvs", (cv.name, cv, "application/pdf")) for cv in cvs]
        r = requests.post("http://localhost:8000/batch-screen",
                         files=files, data={"job_description": jd})
        data = r.json()

    for i, candidate in enumerate(data["ranked_candidates"]):
        score = candidate["screening_result"]["score"]
        verdict = candidate["screening_result"]["verdict"]
        color = "🟢" if score >= 75 else "🟡" if score >= 50 else "🔴"

        with st.expander(f"{color} Candidate {i+1} — Score: {score}/100 — {verdict}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Matched skills:**",
                         ", ".join(candidate["gap_analysis"]["matched_skills"]))
                st.write("**Missing skills:**",
                         ", ".join(candidate["gap_analysis"]["missing_skills"]))
            with col2:
                st.write("**Interview questions:**")
                for q in candidate["screening_result"]["interview_questions"]:
                    st.markdown(f"- {q}")