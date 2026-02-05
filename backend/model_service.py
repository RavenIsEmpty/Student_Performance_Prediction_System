from __future__ import annotations
import os
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

DATA_PATH = os.path.join(ROOT_DIR, "data", "student_data.csv")
MODEL_PATH = os.path.join(ROOT_DIR, "model", "model.joblib")

FEATURES = ["attendance", "assignment", "quiz", "exam"]
TARGET_COL = "result"  # expects "Pass"/"Fail"


def train_and_save_model() -> dict:
    """Train Decision Tree on student_data.csv and save model.joblib"""
    df = pd.read_csv(DATA_PATH)

    # basic validation
    for col in FEATURES:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    if TARGET_COL not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COL}")

    df = df.dropna(subset=FEATURES + [TARGET_COL]).copy()

    # encode target
    df["result_num"] = df[TARGET_COL].map({"Fail": 0, "Pass": 1})

    X = df[FEATURES]
    y = df["result_num"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(random_state=42, max_depth=4)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"model": model, "accuracy": acc}, MODEL_PATH)

    return {"accuracy": acc, "model_path": MODEL_PATH}


def load_model():
    payload = joblib.load(MODEL_PATH)
    # Backward compatible: if old joblib was just a model, wrap it
    if not isinstance(payload, dict) or "model" not in payload:
        payload = {"model": payload}
    return payload


def predict(attendance: float, assignment: float, quiz: float, exam: float) -> dict:
    """Predict Pass/Fail + confidence using predict_proba."""
    payload = load_model()
    model = payload["model"]

    X_new = pd.DataFrame([{
        "attendance": float(attendance),
        "assignment": float(assignment),
        "quiz": float(quiz),
        "exam": float(exam),
    }])

    proba = model.predict_proba(X_new)[0]  # [p_fail, p_pass]
    p_pass = float(proba[1])
    outcome = "PASS" if p_pass >= 0.5 else "FAIL"
    confidence = int(round(max(p_pass, 1 - p_pass) * 100))

    return {
        "outcome": outcome,
        "confidence": confidence,
        "p_pass": round(p_pass, 4),
        "accuracy": float(payload.get("accuracy", 0.0))
    }
