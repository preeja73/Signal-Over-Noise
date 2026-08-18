# Signal Over Noise — 8–10 Minute Demonstration Script

## 1. Business Problem
“Our project is Signal Over Noise, based on a Canadian financial operations case.

The original business problem is alert overload. Our project case identified more than 500 alerts per day and a high false-positive workload.

Our Month-18 business targets are 150 or fewer alerts per day and a false-positive rate of 30 percent or less.

For this final exam, we are not trying to prove those business KPIs. We are demonstrating one core capability that supports the solution: risk-based alert prioritization.”

## 2. Winning Solution
“Through our Mix-and-Match process, we selected a phased hybrid solution from our winning vendor.

The vendor solution includes alert prioritization as an important capability.

Phase 1 focuses on a licensed prioritization platform, while Phase 2 moves toward an explainable machine-learning capability.”

## 3. Prototype Scope
“We intentionally selected only one capability for the MVP: alert prioritization.

We chose this because it directly addresses our original problem. Instead of treating every alert equally, the system helps analysts identify which alerts should be reviewed first.”

## 4. Live Demonstration
“First, this dashboard shows six synthetic AML, Fraud, and Cybersecurity alerts.

The system ranks them by risk, so higher-risk alerts appear first.

Now I will test a new synthetic AML alert.

I will use a $30,000 transaction to a new beneficiary with rapid activity.

This is the input.

When I click Score Alert, the frontend sends the alert information to our Flask backend through an API.

The backend passes the data to our simple ML model.

The model calculates a risk probability.

The output is the risk score, High/Medium/Low priority, and an explanation of the main risk indicators.

This does not mean the transaction is definitely money laundering or fraud. It only means the alert has higher-risk characteristics and should receive higher priority for analyst review.”

## 5. Input → Processing → Output → Business Value
“So the end-to-end flow is:

Input: synthetic AML, Fraud, or Cybersecurity alert.

Processing: Flask API plus ML risk scoring.

Output: risk score, priority, and explanation.

Business value: analysts can review higher-risk alerts first instead of treating every alert equally.”

## 6. Project / RFP Connection
“This prototype is not a new project. It directly continues our Signal Over Noise Mix-and-Match project.

We started with the Canadian business problem, completed our TBP analysis, selected the phased hybrid countermeasure, created our Project Charter, developed the RFI and RFP, evaluated vendors, and selected the winning vendor.

This MVP demonstrates our RFP risk-based alert-prioritization capability.

The MVP proves that the prioritization workflow can work end to end as a proof of concept.

It does not prove our final alert-volume or false-positive KPI targets.”

## 7. What Is Simulated
“For this prototype, the financial data is synthetic.

The connection to real banking systems is mocked.

The ML model is simplified and trained on synthetic data.

We have not implemented production authentication, audit logging, full cybersecurity, or production model monitoring.”

## 8. Next Step
“The next practical step would be a controlled pilot.

We would connect approved representative data through secure APIs, validate the model, add authentication, audit logging, monitoring, and security controls, and then measure performance against our formal RFP acceptance criteria.”

## 9. Closing
“To conclude, this MVP demonstrates the core idea behind Signal Over Noise.

A financial alert enters the system, the model evaluates the risk, the dashboard produces a priority and explanation, and the analyst can focus on higher-risk alerts first.

This moves our project from a business proposal toward the beginning of implementation.”
