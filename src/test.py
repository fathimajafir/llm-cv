import requests

url = "http://127.0.0.1:8000/screen"

# Use any PDF you have handy — even a random one to confirm the pipeline runs
with open("/resume.pdf", "rb") as f:
    response = requests.post(
        url,
        files={"cv_file": ("cv.pdf", f, "application/pdf")},
        data={
            "job_description": """
            We need an AI Engineer with experience in Python, FastAPI, LLM, RAG,
            HuggingFace, PyTorch, Docker, MLOps, machine learning, NLP, 
            transformers, AWS, SQL. 3+ years experience required.
            """
        }
    )

print(response.status_code)
import json
print(json.dumps(response.json(), indent=2))