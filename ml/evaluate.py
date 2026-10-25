"""
ml/evaluate.py
---------------
Evaluates the trained supervised classifier (from ml/train.py) on a
FRESH synthetic dataset (different random seed than training), and
prints accuracy, a classification report, and a confusion matrix.

This is the file to run before a viva to have concrete evaluation
numbers ready to show/discuss.

Usage:
    python ml/evaluate.py
"""

import os
import joblib

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from ml.train import generate_synthetic_dataset, MODEL_PATH


def evaluate_model():
    if not os.path.exists(MODEL_PATH):
        print("No trained model found. Run 'python ml/train.py' first.")
        return

    model = joblib.load(MODEL_PATH)

    # Fresh test set with a different random_state than training,
    # so this is genuinely unseen data.
    X_test, y_test = generate_synthetic_dataset(n_samples=300, random_state=99)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    labels = sorted(set(y_test) | set(y_pred))

    print(f"Evaluation accuracy: {accuracy:.4f}\n")

    print("Classification report:")
    print(classification_report(y_test, y_pred, labels=labels))

    print("Confusion matrix (rows = actual, columns = predicted):")
    print("Labels order:", labels)
    print(confusion_matrix(y_test, y_pred, labels=labels))


if __name__ == "__main__":
    evaluate_model()
