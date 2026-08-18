# Signal Over Noise — Individual Q&A Cheat Sheet

**What part of the original business problem does this address?**  
It addresses alert overload by prioritizing alerts so analysts can review higher-risk alerts first.

**What information enters the system?**  
Synthetic AML, Fraud, or Cybersecurity alert information such as amount, new beneficiary, unusual location, failed access, and rapid activity.

**What does the system produce?**  
A risk score, High/Medium/Low priority, and an explanation.

**What is simulated?**  
The financial data and the connection to real bank systems are simulated. The ML model is also simplified.

**Which RFP requirement does this demonstrate?**  
It demonstrates the risk-based alert-prioritization requirement.

**How does it create business value?**  
It helps analysts spend their time on higher-risk alerts first.

**How would it integrate with the real process?**  
Existing Fraud, AML, and Cyber systems would send alerts through secure APIs. The vendor solution would score them before analyst review.

**What did the LLM generate?**  
We used an LLM to help generate parts of the frontend, Flask backend, API logic, synthetic data, and simple ML code.

**What limitation would you address next?**  
The biggest limitation is synthetic data. The next step is a controlled pilot using approved representative data.

**Did this prototype prove the 70% reduction target?**  
No. It demonstrates the prioritization capability only. The KPI must be validated during a controlled pilot.

**Does a High-priority AML alert mean money laundering?**  
No. It means the alert has higher-risk characteristics and should be reviewed first.
