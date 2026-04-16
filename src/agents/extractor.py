from transformers import pipeline

extractor = pipeline("text2text-generation", model="google/flan-t5-large")

def extract_skills(cv_text: str) -> dict:
    prompt = f"""Extract from this CV:
- years_experience (number)
- skills (comma-separated list)
- education (highest degree)
- job_titles (list of previous titles)

CV: {cv_text[:1500]}

Respond only in this format:
years_experience: X
skills: skill1, skill2, skill3
education: degree name
job_titles: title1, title2"""

    raw = extractor(prompt, max_new_tokens=200)[0]["generated_text"]
    # Parse into dict
    result = {}
    for line in raw.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
    return result