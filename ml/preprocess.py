"""
ml/preprocess.py
-----------------
Standard NLP preprocessing pipeline used before TF-IDF vectorization.

Steps (classic, easy to explain in a viva):
1. Lowercase
2. Remove punctuation/special characters (keep letters, numbers, spaces)
3. Tokenize
4. Remove stopwords (NLTK's English stopword list)
5. Lemmatize (reduce words to their dictionary/root form)

Used identically on BOTH the resume text and the job description, so
TF-IDF compares them on equal footing.
"""

import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

_NLTK_READY = False


def ensure_nltk_data():
    """
    Downloads the NLTK data packages this module needs, but only if
    they aren't already present. Safe to call multiple times.
    """
    global _NLTK_READY
    if _NLTK_READY:
        return

    required_packages = {
        "tokenizers/punkt": "punkt",
        "tokenizers/punkt_tab": "punkt_tab",
        "corpora/stopwords": "stopwords",
        "corpora/wordnet": "wordnet",
        "corpora/omw-1.4": "omw-1.4",
    }

    for path, package_name in required_packages.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package_name, quiet=True)

    _NLTK_READY = True


_lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """
    Main function: runs the full preprocessing pipeline on a piece of
    text and returns a single cleaned string (tokens joined by spaces),
    ready to be fed into TfidfVectorizer.
    """
    ensure_nltk_data()

    if not text:
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation/special characters, keep letters/numbers/spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # 3. Tokenize
    tokens = word_tokenize(text)

    # 4. Remove stopwords (and very short leftover tokens)
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

    # 5. Lemmatize
    tokens = [_lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)


if __name__ == "__main__":
    sample = "Developing scalable APIs using Python, Flask, and SQL databases."
    print("Original :", sample)
    print("Cleaned  :", clean_text(sample))
