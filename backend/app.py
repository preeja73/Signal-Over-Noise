from pathlib import Path
import csv
from flask import Flask, jsonify, request, send_from_directory
from ai_model import SignalOverNoiseModel

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
SAMPLE_ALERTS = ROOT / "data" / "sample_alerts.csv"

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
model = SignalOverNoiseModel()
model.train()

def load_demo_alerts():
    results = []
    with open(SAMPLE_ALERTS, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            alert = {
                "alert_id": row["alert_id"],
                "alert_type": row["alert_type"],
                "description": row["description"],
                "amount": float(row["amount"]),
                "new_beneficiary": int(row["new_beneficiary"]),
                "unusual_location": int(row["unusual_location"]),
                "repeated_failures": int(row["repeated_failures"]),
                "rapid_activity": int(row["rapid_activity"]),
                "known_normal_pattern": int(row["known_normal_pattern"]),
            }
            alert.update(model.predict(alert))
            results.append(alert)
    return sorted(results, key=lambda x: x["risk_score"], reverse=True)

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "prototype": "Signal Over Noise",
        "model": "Logistic Regression trained on synthetic data"
    })

@app.get("/api/alerts")
def alerts():
    return jsonify(load_demo_alerts())

@app.post("/api/score")
def score():
    payload = request.get_json(force=True)

    if "alert_type" not in payload:
        return jsonify({"error": "alert_type is required"}), 400
    if "amount" not in payload:
        return jsonify({"error": "amount is required"}), 400

    result = model.predict(payload)
    return jsonify({**payload, **result})

@app.get("/")
def home():
    return send_from_directory(FRONTEND, "index.html")

@app.get("/<path:path>")
def frontend_file(path):
    return send_from_directory(FRONTEND, path)

if __name__ == "__main__":
    print("Signal Over Noise MVP running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
