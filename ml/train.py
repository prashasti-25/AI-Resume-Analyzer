"""
ml/train.py
------------
OPTIONAL supervised ML layer for the college viva.

WHY SYNTHETIC DATA:
A real labeled dataset of "resume + JD -> correct match score" does not
exist publicly, and hand-labeling thousands of resume/JD pairs is out of
scope for a college project. Instead, we generate a synthetic dataset
that captures the SAME relationship the rule-based formula in predict.py
already encodes:

    match_score = 60% * text_similarity + 40% * skill_overlap_ratio

We add small random noise so the classifier has to genuinely learn the
decision boundary rather than memorize a perfect formula. This lets the
team train, evaluate, and discuss a real supervised model (features,
train/test split, accuracy) without needing external data -- while the
app's core score still comes from the fully transparent formula in
predict.py, NOT from this classifier.

The trained model predicts one of three labels:
    "Good Match", "Moderate Match", "Needs Improvement"
from two features: [text_similarity, skill_overlap_ratio]

Usage:
    python ml/train.py
"""

import os
import numpy as np
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from ml.predict import get_recommendation

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(_CURRENT_DIR, "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "match_classifier.pkl")


def generate_synthetic_dataset(n_samples=1000, noise_std=6.0, random_state=42):
    """
    Generates n_samples of (text_similarity, skill_overlap_ratio) -> label.
    Both features are drawn uniformly from [0, 1]. The label is derived
    from the same weighted formula used in predict.py, with Gaussian
    noise added to the score before thresholding -- so the classifier
    sees realistic, slightly noisy examples instead of a perfectly
    separable synthetic pattern.
    """
    rng = np.random.default_rng(random_state)

    text_similarity = rng.uniform(0, 1, n_samples)
    skill_overlap_ratio = rng.uniform(0, 1, n_samples)

    base_score = (0.6 * text_similarity * 100) + (0.4 * skill_overlap_ratio * 100)
    noisy_score = base_score + rng.normal(0, noise_std, n_samples)
    noisy_score = np.clip(noisy_score, 0, 100)

    labels = np.array([get_recommendation(s) for s in noisy_score])

    X = np.column_stack([text_similarity, skill_overlap_ratio])
    y = labels

    return X, y


def train_model():
    X, y = generate_synthetic_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Test accuracy: {accuracy:.4f}\n")
    print("Classification report:")
    print(classification_report(y_test, y_pred))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")

    return model, accuracy


if __name__ == "__main__":
    train_model()
