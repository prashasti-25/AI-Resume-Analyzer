"""
ml/predict.py
--------------
THIS IS THE MAIN FILE MEMBER 1's app.py CALLS.

Public contract (do not change without telling the team):

    result = analyze_resume(resume_text, job_description)

    Returns:
    {
        "match_score": 82.0,
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["AWS", "Docker"],
        "recommendation": "Good Match"
    }

APPROACH (explainable -- good for a viva):
1. Clean both texts with the same NLP pipeline (ml/preprocess.py)
2. Vectorize both with TF-IDF
3. Compute cosine similarity between the two TF-IDF vectors (0 to 1)
4. Separately extract skills from each text using the SAME skill
   vocabulary Member 2 uses (data/skills_master.csv), then compute:
     - matched_skills = skills in both resume and JD
     - missing_skills = skills in JD but not in resume
5. Combine (3) and (4) into a single 0-100 match_score:
     match_score = 60% * text_similarity + 40% * skill_overlap_ratio
   The 60/40 weighting reflects that overall content similarity matters,
   but explicit required skills matter more -- this is a simple, tunable,
   fully explainable formula (no black box).
6. Convert the score into a human-readable recommendation using
   fixed thresholds.

An OPTIONAL supervised classifier (trained in ml/train.py on a synthetic
dataset) can additionally double-check the recommendation label -- see
`get_ml_recommendation()`. It is not required for the app to work; if no
trained model file exists yet, the app silently falls back to the
threshold-based recommendation above.
"""

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ml.preprocess import clean_text
from resume_parser.skill_extractor import extract_skills, load_skills_vocabulary

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_CURRENT_DIR, "..", "models", "match_classifier.pkl")

# Cache the skill vocabulary once per process instead of re-reading the CSV
# on every single request.
_SKILL_VOCAB = load_skills_vocabulary()


def compute_text_similarity(resume_text, job_description):
    """
    Cleans both texts, vectorizes them with TF-IDF (fit fresh on just
    these two documents -- this is standard practice for one-off
    pairwise comparisons and needs no pre-trained vectorizer file),
    and returns their cosine similarity as a float between 0 and 1.
    """
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    if not resume_clean or not jd_clean:
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(similarity)


def compute_skill_overlap(resume_text, job_description):
    """
    Extracts skills separately from the resume and the JD using the
    shared vocabulary, then returns (matched_skills, missing_skills, overlap_ratio).
    """
    resume_skills = set(extract_skills(resume_text, _SKILL_VOCAB))
    jd_skills = set(extract_skills(job_description, _SKILL_VOCAB))

    matched_skills = sorted(resume_skills & jd_skills)
    missing_skills = sorted(jd_skills - resume_skills)

    overlap_ratio = (len(matched_skills) / len(jd_skills)) if jd_skills else 0.0

    return matched_skills, missing_skills, overlap_ratio


def get_recommendation(match_score):
    """Converts a 0-100 match_score into a human-readable label."""
    if match_score >= 75:
        return "Good Match"
    elif match_score >= 50:
        return "Moderate Match"
    else:
        return "Needs Improvement"


def get_ml_recommendation(text_similarity, skill_overlap_ratio):
    """
    OPTIONAL: uses the trained supervised classifier (ml/train.py) to
    predict a recommendation label from [text_similarity, skill_overlap_ratio].
    Returns None if no trained model is found, so callers can gracefully
    ignore this and rely on get_recommendation() instead.
    """
    if not os.path.exists(MODEL_PATH):
        return None

    try:
        import joblib
        model = joblib.load(MODEL_PATH)
        prediction = model.predict([[text_similarity, skill_overlap_ratio]])
        return prediction[0]
    except Exception:
        return None


def analyze_resume(resume_text, job_description):
    """
    Main function of the ml module. See module docstring for the
    exact contract Member 1's app.py depends on.
    """
    text_similarity = compute_text_similarity(resume_text, job_description)
    matched_skills, missing_skills, skill_overlap_ratio = compute_skill_overlap(
        resume_text, job_description
    )

    raw_score = (0.6 * text_similarity * 100) + (0.4 * skill_overlap_ratio * 100)
    match_score = round(min(max(raw_score, 0), 100), 2)

    recommendation = get_recommendation(match_score)

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    sample_resume = """
    Experienced Python developer skilled in Flask, SQL, and Machine Learning.
    Built REST APIs and worked with Git for version control.
    """
    sample_jd = """
    Looking for a Python developer with Flask experience, knowledge of
    Docker, AWS, and strong SQL skills.
    """
    import json
    print(json.dumps(analyze_resume(sample_resume, sample_jd), indent=2))
