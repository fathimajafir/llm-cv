from fastapi import FastAPI, UploadFile, File, Form
import fitz, json
from agents.extractor import extract_skills
from agents.gap_analyzer import analyze_gaps
from agents.scorer import score_candidate

app = FastAPI(title="LLM CV Screener API")

def parse_jd_skills(jd_text: str) -> list[str]:
    # Simple keyword extraction — swap for NER model for production
    keywords = ["python", "fastapi", "llm", "pytorch", "mlops", "rag",
                "huggingface", "docker", "kubernetes", "sql", "aws", "azure"]
    return [k for k in keywords if k in jd_text.lower()]

@app.post("/screen")
async def screen_cv(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Extract CV text
    content = await cv_file.read()
    with open("/tmp/cv.pdf", "wb") as f:
        f.write(content)
    doc = fitz.open("/tmp/cv.pdf")
    cv_text = " ".join(page.get_text() for page in doc)

    # Run agents in sequence
    cv_data = extract_skills(cv_text)
    cv_skills = cv_data.get("skills", "").split(",")
    jd_skills = parse_jd_skills(job_description)

    gap = analyze_gaps(cv_skills, jd_skills)
    result = score_candidate(gap, cv_data, job_description)

    return {
        "candidate_profile": cv_data,
        "gap_analysis": gap,
        "screening_result": result
    }

@app.post("/batch-screen")
async def batch_screen(cvs: list[UploadFile] = File(...), job_description: str = Form(...)):
    results = []
    for cv in cvs:
        r = await screen_cv(cv, job_description)
        results.append(r)
    # Sort by score
    results.sort(key=lambda x: x["screening_result"]["score"], reverse=True)
    return {"ranked_candidates": results, "total": len(results)}