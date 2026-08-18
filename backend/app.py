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
ALERT_STATE = {}


def _int_or_none(value):
    if value in (None, ""):
        return None
    return int(value)


def load_demo_alerts():
    results = []
    with open(SAMPLE_ALERTS, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            alert = {
                "alert_id": row["alert_id"],
                "alert_type": row["alert_type"],
                "customer": row.get("customer", ""),
                "account": row.get("account", ""),
                "description": row["description"],
                "amount": float(row["amount"]),
                "new_beneficiary": int(row["new_beneficiary"]),
                "unusual_location": int(row["unusual_location"]),
                "repeated_failures": int(row["repeated_failures"]),
                "rapid_activity": int(row["rapid_activity"]),
                "known_normal_pattern": int(row["known_normal_pattern"]),
                "received_at": row.get("received_at", ""),
                "status": row.get("status") or "Waiting for review",
                "disposition": row.get("disposition") or "",
                "investigation_minutes": _int_or_none(row.get("investigation_minutes")),
            }
            alert.update(model.predict(alert))
            alert.update(ALERT_STATE.get(alert["alert_id"], {}))
            results.append(alert)
    return sorted(results, key=lambda x: x["risk_score"], reverse=True)


def dashboard_kpis(alerts):
    decided = [a for a in alerts if a["status"] in ("Closed", "Escalated")]
    false_positives = [a for a in decided if a.get("disposition") == "False positive"]
    reviewed_times = [a["investigation_minutes"] for a in decided if a.get("investigation_minutes")]

    if decided:
        false_positive_rate = f"{round(100 * len(false_positives) / len(decided))}%"
    else:
        false_positive_rate = "—"

    if reviewed_times:
        avg_investigation_time = f"{round(sum(reviewed_times) / len(reviewed_times))} min"
    else:
        avg_investigation_time = "—"

    return {
        "total_alerts_today": len(alerts),
        "high_risk_alerts": sum(1 for a in alerts if a["priority"] in ("Critical", "High")),
        "false_positive_rate": false_positive_rate,
        "waiting_for_review": sum(1 for a in alerts if a["status"] == "Waiting for review"),
        "avg_investigation_time": avg_investigation_time,
    }


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "prototype": "Signal Over Noise",
        "model": "Logistic Regression trained on synthetic data"
    })

@app.get("/api/alerts")
def alerts():
    demo_alerts = load_demo_alerts()
    return jsonify({
        "kpis": dashboard_kpis(demo_alerts),
        "alerts": demo_alerts,
    })


@app.post("/api/alerts/<alert_id>/decision")
def decide_alert(alert_id):
    payload = request.get_json(force=True) or {}
    action = payload.get("action")

    updates = {}
    if action == "investigate":
        updates = {"status": "In review"}
    elif action == "escalate":
        updates = {
            "status": "Escalated",
            "disposition": "Escalated for investigation",
            "investigation_minutes": payload.get("investigation_minutes", 15),
        }
    elif action == "close":
        updates = {
            "status": "Closed",
            "disposition": payload.get("disposition", "False positive"),
            "investigation_minutes": payload.get("investigation_minutes", 10),
        }
    else:
        return jsonify({"error": "action must be investigate, escalate, or close"}), 400

    ALERT_STATE[alert_id] = {**ALERT_STATE.get(alert_id, {}), **updates}
    demo_alerts = load_demo_alerts()
    updated = next((a for a in demo_alerts if a["alert_id"] == alert_id), None)
    if not updated:
        return jsonify({"error": "alert not found"}), 404

    return jsonify({"alert": updated, "kpis": dashboard_kpis(demo_alerts)})

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
    print("Signal Over Noise MVP running on http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=True)
