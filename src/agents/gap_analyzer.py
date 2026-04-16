def analyze_gaps(cv_skills: list[str], jd_requirements: list[str]) -> dict:
    cv_set = set(s.lower() for s in cv_skills)
    jd_set = set(r.lower() for r in jd_requirements)

    matched = cv_set & jd_set
    missing = jd_set - cv_set
    bonus = cv_set - jd_set

    match_pct = len(matched) / len(jd_set) * 100 if jd_set else 0

    return {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "bonus_skills": list(bonus),
        "match_percentage": round(match_pct, 1)
    }