from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]
TRAINING_DATA = ROOT / "data" / "synthetic_training_data.csv"

FEATURES = [
    "alert_type",
    "amount",
    "new_beneficiary",
    "unusual_location",
    "repeated_failures",
    "rapid_activity",
    "known_normal_pattern",
]

class SignalOverNoiseModel:
    """
    Proof-of-concept model only.
    Trained on synthetic data to demonstrate the risk-prioritization workflow.
    """

    def __init__(self):
        self.pipeline = None

    def train(self):
        df = pd.read_csv(TRAINING_DATA)
        X = df[FEATURES]
        y = df["high_risk"]

        categorical = ["alert_type"]
        numeric = [c for c in FEATURES if c not in categorical]

        preprocessor = ColumnTransformer([
            ("category", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("numeric", StandardScaler(), numeric),
        ])

        self.pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42))
        ])
        self.pipeline.fit(X, y)

    def predict(self, alert):
        if self.pipeline is None:
            self.train()

        row = pd.DataFrame([{
            "alert_type": alert["alert_type"],
            "amount": float(alert.get("amount", 0)),
            "new_beneficiary": int(alert.get("new_beneficiary", 0)),
            "unusual_location": int(alert.get("unusual_location", 0)),
            "repeated_failures": int(alert.get("repeated_failures", 0)),
            "rapid_activity": int(alert.get("rapid_activity", 0)),
            "known_normal_pattern": int(alert.get("known_normal_pattern", 0)),
        }])

        probability = float(self.pipeline.predict_proba(row)[0][1])
        risk_score = round(probability * 100, 1)

        if risk_score >= 85:
            priority = "Critical"
        elif risk_score >= 70:
            priority = "High"
        elif risk_score >= 40:
            priority = "Medium"
        else:
            priority = "Low"

        amount = float(alert.get("amount", 0))
        new_beneficiary = int(alert.get("new_beneficiary", 0))
        unusual_location = int(alert.get("unusual_location", 0))
        repeated_failures = int(alert.get("repeated_failures", 0))
        rapid_activity = int(alert.get("rapid_activity", 0))
        known_normal_pattern = int(alert.get("known_normal_pattern", 0))

        reasons = []
        if amount >= 20000:
            reasons.append("unusual transaction amount")
        if new_beneficiary:
            reasons.append("new beneficiary")
        if unusual_location:
            reasons.append("unusual location/device")
        if repeated_failures:
            reasons.append("repeated failed access")
        if rapid_activity:
            reasons.append("multiple rapid transfers")
        if known_normal_pattern:
            reasons.append("consistent with the customer's normal pattern")
        elif amount >= 20000 or new_beneficiary or unusual_location or rapid_activity:
            reasons.append("activity inconsistent with the customer's normal pattern")

        if not reasons:
            reasons = ["combined model features"]

        return {
            "risk_score": risk_score,
            "priority": priority,
            "explanation": ", ".join(reasons)
        }
