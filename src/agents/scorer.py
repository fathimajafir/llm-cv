def score_candidate(gap_analysis: dict, cv_data: dict, jd_text: str) -> dict:
    score = gap_analysis["match_percentage"]
    
    # Boost score for experience
    yoe = int(cv_data.get("years_experience", 0) or 0)
    if yoe >= 5:
        score = min(100, score + 10)
    elif yoe >= 3:
        score = min(100, score + 5)

    # Generate interview questions for missing skills
    missing = gap_analysis["missing_skills"]
    questions = [
        f"Can you describe any experience you have with {skill}?"
        for skill in missing[:3]
    ]

    verdict = "Strong fit" if score >= 75 else "Possible fit" if score >= 50 else "Weak fit"

    return {
        "score": round(score, 1),
        "verdict": verdict,
        "interview_questions": questions,
        "missing_skills": missing
    }