# Signal Over Noise — Final Exam MVP/PoC

## What this prototype demonstrates
One core capability of the proposed Signal Over Noise vendor solution:
**risk-based prioritization of AML, Fraud, and Cybersecurity alerts**.

## End-to-end function
Input
→ Flask API
→ Simple ML risk scoring
→ Risk score + priority + explanation
→ Prioritized analyst dashboard
→ Business value: analyst reviews higher-risk alerts first

## What is working
- Frontend dashboard
- Python Flask backend
- REST API
- Simple Logistic Regression ML model
- Synthetic training data
- Alert scoring
- High / Medium / Low prioritization
- Explanation text

## What is simulated
- Real banking/customer data
- Real connection to the bank's fraud / AML / cyber systems
- Production cybersecurity
- Production authentication and audit logging
- Production ML model validation
- Final business KPI validation

## RFP connection
The MVP demonstrates the **risk-based alert-prioritization capability** of the selected vendor solution.

The MVP does **not** prove the project's final KPI targets.
Those must be validated in a controlled pilot using representative approved data.

## Windows
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python backend\app.py
```

Open:
http://127.0.0.1:5000

## macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/app.py
```

Open:
http://127.0.0.1:5000

## Best live demo
- Alert type: AML
- Amount: 30000
- New beneficiary: checked
- Rapid/repeated activity: checked

Click **Score Alert**.

Then explain:
1. Input: synthetic AML alert
2. Processing: frontend → Flask API → ML model
3. Output: risk score + priority + explanation
4. Business value: analyst reviews higher-risk alerts first
