from typing import Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _similarity(resume_text: str, job_text: str) -> float:
    if not resume_text.strip() or not job_text.strip():
        return 0.0

    vect = TfidfVectorizer(stop_words="english")
    tfidf = vect.fit_transform([resume_text, job_text])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return float(sim)


def score_job_rule_based(resume_text: str, job: Dict) -> int:
    """
    Returns an integer score 0–10 based on your rules.
    If 0 => we will skip the job later.
    job dict needs:
      - title
      - description
      - city
      - salary_text (optional)
      - benefits_text (optional)
      - job_type (optional)
    """
    title = job.get("title", "")
    desc = job.get("description", "")
    city = job.get("city", "")
    salary_text = job.get("salary_text", "") or ""
    benefits_text = job.get("benefits_text", "") or ""
    job_type = (job.get("job_type", "") or "").lower()

    full_text = f"{title}\n{desc}\n{city}".lower()

    # 1) German language → 0 points, skip
    german_keywords = [" german ", " deutsch", " deutschkenntnisse", " deutschkenntnis"]
    if any(k in full_text for k in german_keywords):
        return 0

    # 2) Resume match points (0, 2, or 4)
    sim = _similarity(resume_text, full_text)
    # thresholds tuned based on your resume (TF-IDF sims are usually small)
    if sim >= 0.12:
        match_points = 4
    elif sim >= 0.06:
        match_points = 2
    else:
        match_points = 0

    # 3) Salary points (0–3)
    salary_points = 0
    st = salary_text.lower()
    if "€" in st or "eur" in st or "per year" in st or "year" in st:
        # Very rough heuristic for "good" salary
        good_words = ["55000", "60000", "65000", "70000", "80000", "90000", "100000"]
        ok_words = ["45000", "48000", "50000"]
        if any(w in st for w in good_words):
            salary_points = 3
        elif any(w in st for w in ok_words):
            salary_points = 2

    # 4) Remote (0–1)
    remote_points = 1 if "remote" in full_text else 0

    # 5) Benefits (0–1)
    btext = (benefits_text + " " + desc).lower()
    benefit_keywords = ["benefits", "health insurance", "bonus", "stock", "pension", "paid time off", "vacation"]
    benefits_points = 1 if any(k in btext for k in benefit_keywords) else 0

    # 6) Full-time (0–1)
    if "full-time" in full_text or job_type == "full-time":
        fulltime_points = 1
    else:
        fulltime_points = 0

    total = match_points + salary_points + remote_points + benefits_points + fulltime_points

    # Clamp to 0–10 just in case
    if total < 0:
        total = 0
    if total > 10:
        total = 10

    return int(total)
