from transformers import pipeline

# Fix: use text-generation + a decoder model (flan-t5 is encoder-decoder, not supported in new transformers)
extractor = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

def extract_skills(cv_text: str) -> dict:
    prompt = f"""Extract information from this CV and respond ONLY in this exact format, nothing else:
years_experience: X
skills: skill1, skill2, skill3
education: degree name
job_titles: title1, title2

CV: {cv_text[:1500]}

Response:"""

    raw = extractor(
        prompt,
        max_new_tokens=200,
        do_sample=False,
        temperature=1.0,
        pad_token_id=2
    )[0]["generated_text"]

    # Extract only the part after "Response:"
    if "Response:" in raw:
        raw = raw.split("Response:")[-1]

    result = {}
    for line in raw.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip().lower().replace(" ", "_")
            if k in ["years_experience", "skills", "education", "job_titles"]:
                result[k] = v.strip()
    return result