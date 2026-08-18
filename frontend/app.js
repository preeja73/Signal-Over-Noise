let alerts = [];

async function checkHealth(){
  try{
    const r = await fetch("/api/health");
    await r.json();
    document.getElementById("health").textContent = "Backend + AI: Connected";
  }catch(e){
    document.getElementById("health").textContent = "Backend: Not connected";
  }
}

function renderKpis(kpis){
  document.getElementById("total").textContent = kpis.total_alerts_today;
  document.getElementById("highRisk").textContent = kpis.high_risk_alerts;
  document.getElementById("fpRate").textContent = kpis.false_positive_rate;
  document.getElementById("waiting").textContent = kpis.waiting_for_review;
  document.getElementById("avgTime").textContent = kpis.avg_investigation_time;
}

function statusClass(status){
  return status.split(" ")[0];
}

function renderQueue(){
  document.getElementById("rows").innerHTML = alerts.map((a,i)=>`
    <tr>
      <td>#${i+1}</td>
      <td>${a.customer}<span class="account">${a.account}</span></td>
      <td>${a.alert_type}</td>
      <td><b>${a.risk_score}</b></td>
      <td><span class="badge ${a.priority}">${a.priority}</span></td>
      <td>${a.explanation}</td>
      <td>${a.received_at}</td>
      <td><span class="badge status ${statusClass(a.status)}">${a.status}</span></td>
      <td><button onclick="openAlert('${a.alert_id}')">Open</button></td>
    </tr>
  `).join("");
}

async function loadAlerts(){
  const r = await fetch("/api/alerts");
  const data = await r.json();
  alerts = data.alerts;
  renderKpis(data.kpis);
  renderQueue();
}

function evidenceList(alert){
  const items = [];
  if (Number(alert.amount) > 0) items.push(`Transaction amount: $${Number(alert.amount).toLocaleString()} CAD`);
  if (Number(alert.new_beneficiary)) items.push("New beneficiary");
  if (Number(alert.unusual_location)) items.push("Unusual location or device");
  if (Number(alert.repeated_failures)) items.push("Repeated failed access");
  if (Number(alert.rapid_activity)) items.push("Multiple rapid transfers / repeated activity");
  if (Number(alert.known_normal_pattern)) items.push("Matches the customer's normal pattern");
  else items.push("Activity inconsistent with the customer's normal pattern");
  return items.map(item => `<li>${item}</li>`).join("");
}

function openAlert(alertId){
  const alert = alerts.find(a => a.alert_id === alertId);
  if (!alert) return;

  document.getElementById("drawerTitle").textContent = `${alert.alert_id} · ${alert.alert_type}`;
  document.getElementById("drawerBody").innerHTML = `
    <p class="note">Review the evidence, then decide. The model ranks this alert; the analyst makes the final call.</p>
    <p><b>${alert.customer}</b><span class="account">${alert.account}</span></p>
    <p>${alert.description}</p>
    <p>
      <b>Risk score:</b> ${alert.risk_score}/100
      <span class="badge ${alert.priority}">${alert.priority}</span>
      <span class="badge status ${statusClass(alert.status)}">${alert.status}</span>
    </p>
    <p><b>Reason for the score:</b> ${alert.explanation}</p>
    <p><b>Time received:</b> ${alert.received_at}</p>
    ${alert.disposition ? `<p><b>Disposition:</b> ${alert.disposition}</p>` : ""}
    <div class="evidence">
      <b>Evidence</b>
      <ul>${evidenceList(alert)}</ul>
    </div>
    <div class="actions">
      <button onclick="decideAlert('${alert.alert_id}','investigate')">Investigate</button>
      <button class="primary" style="margin-top:0" onclick="decideAlert('${alert.alert_id}','escalate')">Escalate</button>
      <button class="danger" onclick="decideAlert('${alert.alert_id}','close')">Close as false positive</button>
    </div>
  `;
  document.getElementById("drawer").classList.remove("hidden");
}

function closeAlert(){
  document.getElementById("drawer").classList.add("hidden");
}

async function decideAlert(alertId, action){
  const r = await fetch(`/api/alerts/${alertId}/decision`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({action})
  });
  const data = await r.json();
  if (!r.ok) {
    window.alert(data.error || "Decision failed");
    return;
  }
  renderKpis(data.kpis);
  alerts = alerts.map(a => a.alert_id === alertId ? data.alert : a);
  renderQueue();
  openAlert(alertId);
}

async function scoreAlert(){
  const payload = {
    alert_type: document.getElementById("alert_type").value,
    amount: Number(document.getElementById("amount").value || 0),
    new_beneficiary: document.getElementById("new_beneficiary").checked ? 1 : 0,
    unusual_location: document.getElementById("unusual_location").checked ? 1 : 0,
    repeated_failures: document.getElementById("repeated_failures").checked ? 1 : 0,
    rapid_activity: document.getElementById("rapid_activity").checked ? 1 : 0,
    known_normal_pattern: document.getElementById("known_normal_pattern").checked ? 1 : 0
  };

  const r = await fetch("/api/score", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(payload)
  });

  const data = await r.json();

  document.getElementById("result").innerHTML = `
    <b>Risk score:</b> ${data.risk_score}/100<br>
    <b>Priority:</b> <span class="badge ${data.priority}">${data.priority}</span><br>
    <b>Explanation:</b> ${data.explanation}<br><br>
    <small>Important: A high or critical score means higher-risk characteristics for review. It does not prove fraud or money laundering. The analyst still decides whether to escalate or close the alert.</small>
  `;
}

checkHealth();
loadAlerts();
