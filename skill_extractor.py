"""
resume_parser/skill_extractor.py
---------------------------------
Extracts skills mentioned in a resume by matching against a shared
vocabulary file (data/skills_master.csv). This SAME file is reused by
Member 3's ML module for matched/missing skill detection, so both
parts of the project always agree on what counts as a "skill".

Matching is simple, explainable keyword matching (word-boundary,
case-insensitive) -- easy to defend in a viva, no black-box behavior.
"""

import os
import re
import csv

# Path to the shared skill vocabulary (project_root/data/skills_master.csv)
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_CSV_PATH = os.path.join(_CURRENT_DIR, "..", "data", "skills_master.csv")


def load_skills_vocabulary(csv_path=SKILLS_CSV_PATH):
    """
    Reads data/skills_master.csv and returns a list of skill names.
    Falls back to a small built-in list if the CSV is missing, so the
    app never crashes just because a data file wasn't found.
    """
    skills = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                skill_name = row.get("skill", "").strip()
                if skill_name:
                    skills.append(skill_name)
    except FileNotFoundError:
        skills = ["Python", "Java", "SQL", "Communication", "Teamwork"]

    return skills


def _build_skill_pattern(skill):
    """
    Builds a case-insensitive regex pattern for a skill name that:
    - Matches whole words/phrases only (avoids matching "Java" inside "JavaScript")
    - Escapes special regex characters (e.g. "C++")
    """
    escaped = re.escape(skill)
    return re.compile(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", re.IGNORECASE)


def extract_skills(text, vocabulary=None):
    """
    Main function: scans `text` for any skill in the vocabulary.

    Args:
        text: raw resume text (string)
        vocabulary: optional list of skill names; loads from CSV if not given

    Returns:
        A sorted list of matched skill names (original casing from the CSV),
        with duplicates removed.
    """
    if not text:
        return []

    if vocabulary is None:
        vocabulary = load_skills_vocabulary()

    found = set()
    for skill in vocabulary:
        pattern = _build_skill_pattern(skill)
        if pattern.search(text):
            found.add(skill)

    return sorted(found)


if __name__ == "__main__":
    # Quick manual test
    sample = "Experienced in Python, Flask, and Machine Learning. Familiar with Docker and SQL."
    print(extract_skills(sample))
