# llm-cv
Agentic LLM CV–Job Screener
# 🤖 LLM CV Screener

An agentic AI pipeline that screens CVs against job descriptions — producing ranked candidates, skill gap analysis, fit scores, and auto-generated interview questions. Built with HuggingFace Transformers and FastAPI.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?style=flat-square)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=flat-square)
---

## Why I Built This

Hiring teams in fast-growing markets like the UAE spend hours manually screening CVs against job descriptions. This project automates that pipeline end-to-end using a multi-agent LLM architecture — no paid API keys required, fully local and deployable.

This project demonstrates:
- Multi-agent LLM orchestration with sequential reasoning steps
- Structured output extraction from unstructured text (CVs)
- REST API design with FastAPI for real-world integration
- Batch processing of 50+ CVs ranked by fit score

---

## Features

- **Upload any CV** (PDF format) and paste a job description
- **Agent 1 — Skill Extractor:** Pulls years of experience, skills, education, and job titles from raw CV text
- **Agent 2 — Gap Analyzer:** Compares extracted CV skills against job requirements and identifies matched, missing, and bonus skills
- **Agent 3 — Scorer:** Produces a 0–100 fit score with a verdict (Strong / Possible / Weak fit)
- **Interview question generator:** Auto-generates targeted questions for each skill gap
- **Batch mode:** Screen and rank multiple CVs against one job description in a single request
- **Streamlit dashboard:** Clean UI for non-technical recruiters
- **REST API:** JSON responses for integration into any ATS or HR system

---

## Architecture

```
CV (PDF)  ──┐
            ├──► Agent 1: Skill Extractor  ──► Agent 2: Gap Analyzer  ──► Agent 3: Scorer  ──► JSON Report
JD (text) ──┘         (HuggingFace LLM)          (rule-based match)        (scored output)
```

**Tech stack:**

| Layer | Technology |
|---|---|
| LLM inference | HuggingFace Transformers (TinyLlama 1.1B) |
| PDF parsing | PyMuPDF (fitz) |
| API backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Language | Python 3.11 |

---

## 📁 Project Structure

```
llm-cv-screener/
├── src/
│   ├── main.py                  # FastAPI app + endpoints
│   ├── agents/
│   │   ├── extractor.py         # Agent 1: skill extraction from CV
│   │   ├── gap_analyzer.py      # Agent 2: skill gap analysis
│   │   └── scorer.py            # Agent 3: fit scoring + interview Qs
│   └── frontend/
│       └── app.py               # Streamlit dashboard
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/llm-cv-screener.git
cd llm-cv-screener
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        
venv\Scripts\activate           
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
cd src
uvicorn main:app --reload
```

API is now live at **http://127.0.0.1:8000**
Interactive docs at **http://127.0.0.1:8000/docs**

### 5. Run the Streamlit frontend (separate terminal)

```bash
streamlit run src/frontend/app.py
```

---

## 🔌 API Endpoints

### `POST /screen` — Screen a single CV

```bash
curl -X POST http://127.0.0.1:8000/screen \
  -F "cv_file=@your_cv.pdf" \
  -F "job_description=Looking for a Python developer with FastAPI, LLM, RAG, HuggingFace, Docker, MLOps experience."
```

**Response:**
```json
{
  "candidate_profile": {
    "years_experience": "4",
    "skills": "python, machine learning, nlp, pytorch",
    "education": "Bachelor of Computer Science",
    "job_titles": "ML Engineer, Data Scientist"
  },
  "gap_analysis": {
    "matched_skills": ["python", "pytorch", "nlp"],
    "missing_skills": ["docker", "mlops"],
    "bonus_skills": ["tensorflow"],
    "match_percentage": 65.0
  },
  "screening_result": {
    "score": 70.0,
    "verdict": "Possible fit",
    "interview_questions": [
      "Can you describe any experience you have with docker?",
      "Can you describe any experience you have with mlops?"
    ]
  }
}
```

### `POST /batch-screen` — Rank multiple CVs

```bash
curl -X POST http://127.0.0.1:8000/batch-screen \
  -F "cvs=@cv1.pdf" \
  -F "cvs=@cv2.pdf" \
  -F "job_description=AI Engineer with LLM and RAG experience"
```

Returns candidates sorted by fit score (highest first).

---

## Running Tests

```bash
# Quick smoke test
python src/test_api.py

# Or open the Swagger UI
open http://127.0.0.1:8000/docs
```

---

## 📦 Requirements

```
fastapi
uvicorn
transformers
torch
PyMuPDF
streamlit
pydantic
python-multipart
requests
```

Install all:
```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

The default model is `TinyLlama/TinyLlama-1.1B-Chat-v1.0` — fast, runs on CPU, no API key needed.

To upgrade to a more powerful model (requires GPU), change this line in `agents/extractor.py`:

```python
# Default (CPU-friendly)
extractor = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Upgrade (requires ~16GB VRAM)
extractor = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")
```

---

## 🗺️ Roadmap

- [ ] Docker + docker-compose for one-command deployment
- [ ] Arabic CV support (multilingual embeddings)
- [ ] Export results to PDF report
- [ ] Add ChromaDB to cache extracted CV profiles
- [ ] Support DOCX and plain text CV uploads
- [ ] Authentication for multi-tenant use

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

