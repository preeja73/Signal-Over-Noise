async function checkHealth(){
  try{
    const r = await fetch("/api/health");
    await r.json();
    document.getElementById("health").textContent = "Backend + AI: Connected";
  }catch(e){
    document.getElementById("health").textContent = "Backend: Not connected";
  }
}

async function loadAlerts(){
  const r = await fetch("/api/alerts");
  const alerts = await r.json();

  document.getElementById("total").textContent = alerts.length;
  document.getElementById("high").textContent = alerts.filter(a=>a.priority==="High").length;
  document.getElementById("medium").textContent = alerts.filter(a=>a.priority==="Medium").length;
  document.getElementById("low").textContent = alerts.filter(a=>a.priority==="Low").length;

  document.getElementById("rows").innerHTML = alerts.map((a,i)=>`
    <tr>
      <td>#${i+1}</td>
      <td>${a.alert_id}</td>
      <td>${a.alert_type}</td>
      <td>${a.description}</td>
      <td><b>${a.risk_score}</b></td>
      <td><span class="badge ${a.priority}">${a.priority}</span></td>
      <td>${a.explanation}</td>
    </tr>
  `).join("");
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
    <small>Important: High priority means higher-risk characteristics for review. It does not prove fraud or money laundering.</small>
  `;
}

checkHealth();
loadAlerts();
