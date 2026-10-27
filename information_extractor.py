"""
resume_parser/information_extractor.py
----------------------------------------
Extracts structured personal/professional info from raw resume text
using simple, explainable rules (regex + keyword heuristics) --
no ML needed for this part, which keeps it easy to defend in a viva.

Each function does ONE job and can be tested independently.
"""

import re

# --------------------------------------------------------------------
# EMAIL
# --------------------------------------------------------------------

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def extract_email(text):
    """Returns the first email address found, or None."""
    match = EMAIL_PATTERN.search(text)
    return match.group(0) if match else None


# --------------------------------------------------------------------
# PHONE
# --------------------------------------------------------------------

# Matches common formats: +91 9876543210, (123) 456-7890, 123-456-7890, 9876543210
PHONE_PATTERN = re.compile(
    r"(\+?\d{1,3}[\s-]?)?(\(?\d{3,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}"
)


def extract_phone(text):
    """
    Returns the first plausible phone number found (as a cleaned string),
    or None. Filters out short matches that are likely not phone numbers.
    """
    for match in PHONE_PATTERN.finditer(text):
        candidate = match.group(0)
        digits_only = re.sub(r"\D", "", candidate)
        if 10 <= len(digits_only) <= 13:
            return candidate.strip()
    return None


# --------------------------------------------------------------------
# NAME
# --------------------------------------------------------------------

def extract_name(text):
    """
    Heuristic name extraction: resumes almost always put the candidate's
    name on one of the first few lines, before contact details.

    Rule: look at the first 5 non-empty lines and pick the first one that:
    - has 1 to 4 words
    - contains no digits
    - contains no email/phone patterns
    - is not all uppercase section-header-looking text like "RESUME" or "CURRICULUM VITAE"
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    header_blocklist = {"resume", "curriculum vitae", "cv", "bio-data", "biodata"}

    for line in lines[:5]:
        if EMAIL_PATTERN.search(line):
            continue
        if any(char.isdigit() for char in line):
            continue
        if line.lower() in header_blocklist:
            continue

        word_count = len(line.split())
        if 1 <= word_count <= 4 and len(line) <= 50:
            return line.title() if line.isupper() else line

    return None


# --------------------------------------------------------------------
# EDUCATION
# --------------------------------------------------------------------

EDUCATION_KEYWORDS = [
    "bachelor", "master", "b.tech", "btech", "m.tech", "mtech",
    "b.e.", "b.e", "m.e.", "m.e", "bsc", "msc", "b.sc", "m.sc",
    "mba", "ph.d", "phd", "doctorate", "diploma",
    "university", "college", "institute of technology", "high school",
]


def extract_education(text):
    """
    Returns a list of lines from the resume that look like education
    entries (degree names, institutions), based on keyword matching.
    Deduplicates while preserving order.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    matches = []
    seen = set()

    for line in lines:
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in EDUCATION_KEYWORDS):
            if lower_line not in seen:
                matches.append(line)
                seen.add(lower_line)

    return matches


# --------------------------------------------------------------------
# EXPERIENCE
# --------------------------------------------------------------------

EXPERIENCE_SECTION_HEADERS = [
    "work experience", "professional experience", "experience",
    "employment history", "internship",
]

# Matches "3 years", "2+ years", "5 yrs", etc.
YEARS_PATTERN = re.compile(r"(\d+)\+?\s*(?:years|yrs)", re.IGNORECASE)

# Matches date ranges like "Jan 2020 - Dec 2021", "2019 - 2021", "2020 - Present"
DATE_RANGE_PATTERN = re.compile(
    r"(?:[A-Za-z]{3,9}\s)?\d{4}\s*[-–to]+\s*(?:[A-Za-z]{3,9}\s)?(?:\d{4}|Present|present)",
)


def extract_experience(text):
    """
    Returns a list of experience-related lines: date ranges (job durations)
    plus any explicit "X years of experience" style mentions.
    Kept intentionally simple -- a full work-history parser is out of
    scope for a college project and is not needed for the match score.

    Lines that already look like EDUCATION entries (e.g. "B.Tech ..., 2018 - 2022")
    are excluded here even if they also contain a date range, so a single
    line doesn't get double-counted in both sections.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    experience_entries = []
    seen = set()

    for line in lines:
        lower_line = line.lower()
        is_education_line = any(keyword in lower_line for keyword in EDUCATION_KEYWORDS)

        if is_education_line:
            continue

        if DATE_RANGE_PATTERN.search(line) and lower_line not in seen:
            experience_entries.append(line)
            seen.add(lower_line)

    years_matches = YEARS_PATTERN.findall(text)
    if years_matches:
        max_years = max(int(y) for y in years_matches)
        summary = f"{max_years}+ years of experience (mentioned in resume)"
        if summary.lower() not in seen:
            experience_entries.insert(0, summary)

    return experience_entries


# --------------------------------------------------------------------
# COMBINED HELPER
# --------------------------------------------------------------------

def extract_all(text):
    """Convenience function that runs every extractor and returns one dict."""
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
    }


if __name__ == "__main__":
    sample = """John Smith
    john.smith@email.com | +91 9876543210

    EDUCATION
    B.Tech in Computer Science, XYZ University, 2018 - 2022

    EXPERIENCE
    Software Engineer Intern, ABC Corp, Jan 2022 - Jun 2022
    2 years of experience in web development
    """
    print(extract_all(sample))
