"""Model and data helpers for Cardio Monitor (Streamlit edition).

The model is trained from heart.csv when the app starts and cached by
Streamlit. No database and no pickled model files are needed.
"""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = Path(__file__).parent / "heart.csv"

FEATURES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]

# Dropdown label -> numeric code used in heart.csv
SEX = {"Male": 1, "Female": 0}
CHEST_PAIN = {
    "Typical angina": 0,
    "Atypical angina": 1,
    "Non-anginal pain": 2,
    "Asymptomatic": 3,
}
YES_NO = {"Yes": 1, "No": 0}
SLOPE = {
    "Upsloping: better heart rate with exercise (uncommon)": 0,
    "Flat: minimal change (typical healthy heart)": 1,
    "Downsloping: signs of unhealthy heart": 2,
}
THAL = {
    "Normal": 2,
    "Fixed defect: used to be a defect but OK now": 1,
    "Reversible defect: no proper blood movement when exercising": 3,
}
REST_ECG = {
    "Nothing to note": 0,
    "ST-T wave abnormality": 1,
    "Possible or definite left ventricular hypertrophy": 2,
}


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def train_model():
    """Train a MinMax-scaled KNN (k=7) on heart.csv.

    Returns (model, test_accuracy). In this dataset target 1 means
    low risk and target 0 means high risk.
    """
    df = load_data()
    X, y = df[FEATURES], df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=0
    )
    model = make_pipeline(MinMaxScaler(), KNeighborsClassifier(n_neighbors=7))
    model.fit(X_train, y_train)
    accuracy = float(model.score(X_test, y_test))
    # Refit on all rows so the live model uses every record.
    model.fit(X, y)
    return model, accuracy


def reference_values() -> pd.Series:
    """Average value of each feature for the low-risk group (target == 1)."""
    df = load_data()
    return df[df["target"] == 1][FEATURES].mean()


def predict(model, record: dict):
    """Return (label, low_risk_probability). label 1 = low risk, 0 = high risk."""
    row = pd.DataFrame([record], columns=FEATURES)
    label = int(model.predict(row)[0])
    low_risk_prob = float(model.predict_proba(row)[0][list(model.classes_).index(1)])
    return label, low_risk_prob
