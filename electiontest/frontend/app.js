const BASE = "http://127.0.0.1:8000";
let barChart = null;
let pieChart = null;

const translations = {
  en: {
    title: "Election AI Dashboard",
    subtitle: "Government of Nepal",
    uploadTitle: "Upload Data",
    electionLabel: "Election CSV",
    socialLabel: "Social Media CSV",
    pmTitle: "Prime Minister Prediction",
    candidateTitle: "Top Candidate Predictions",
    chartTitle: "Election Visualization",
    accuracyTitle: "Model Accuracy",
    reportTitle: "Reports"
  },
  np: {
    title: "निर्वाचन एआई ड्यासबोर्ड",
    subtitle: "नेपाल सरकार",
    uploadTitle: "डाटा अपलोड गर्नुहोस्",
    electionLabel: "निर्वाचन CSV",
    socialLabel: "सामाजिक सञ्जाल CSV",
    pmTitle: "प्रधानमन्त्री पूर्वानुमान",
    candidateTitle: "शीर्ष उम्मेदवार पूर्वानुमान",
    chartTitle: "निर्वाचन दृश्यकरण",
    accuracyTitle: "मोडेल शुद्धता",
    reportTitle: "रिपोर्टहरू"
  }
};

function setLang(lang) {
  const t = translations[lang];
  Object.keys(t).forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = t[id];
  });
}

function upload(type) {
  const file = document.getElementById(type).files[0];
  if (!file) return alert("Select file first");

  const form = new FormData();
  form.append("file", file);

  fetch(`${BASE}/upload/${type}`, { method: "POST", body: form })
    .then(() => alert("Upload successful"))
    .catch(() => alert("Upload failed"));
}

async function runPrediction() {
  try {
    const res = await fetch(`${BASE}/predict`);
    const data = await res.json();

    renderPM(data.pm_prediction);
    renderAccuracy(data.model_accuracy);
    renderCards(data.predictions);
    renderCharts(data.predictions);
  } catch {
    alert("Prediction failed");
  }
}

function renderPM(pm) {
  document.getElementById("pmCard").innerHTML = `
    <p><b>Party:</b> ${pm.pm_party}</p>
    <p><b>Seats:</b> ${pm.seats}</p>
    <p><b>Majority:</b> ${pm.majority}</p>
  `;
}

function renderAccuracy(acc) {
  document.getElementById("accuracyValue").textContent = `Accuracy: ${acc}%`;
}

function renderCards(preds) {
  const cards = document.getElementById("cards");
  cards.innerHTML = "";

  preds
    .sort((a, b) => b.win_probability - a.win_probability)
    .slice(0, 10)
    .forEach(p => {
      cards.innerHTML += `
        <div class="card">
          <b>${p.candidate_id}</b>
          <p>${(p.win_probability * 100).toFixed(2)}%</p>
        </div>
      `;
    });
}

function renderCharts(preds) {
  const top = preds
    .sort((a, b) => b.win_probability - a.win_probability)
    .slice(0, 6);

  const labels = top.map(p => p.candidate_id);
  const values = top.map(p => (p.win_probability * 100).toFixed(2));

  if (barChart) barChart.destroy();
  if (pieChart) pieChart.destroy();

  barChart = new Chart(barChartEl(), {
    type: "bar",
    data: { labels, datasets: [{ data: values, backgroundColor: "#c62828" }] },
    options: { maintainAspectRatio: false, plugins: { legend: { display: false } } }
  });

  pieChart = new Chart(pieChartEl(), {
    type: "pie",
    data: { labels, datasets: [{ data: values }] },
    options: { maintainAspectRatio: false }
  });
}

function barChartEl() {
  return document.getElementById("barChart");
}

function pieChartEl() {
  return document.getElementById("pieChart");
}

function downloadPDF() {
  window.open(`${BASE}/download/pdf`);
}

function downloadShap() {
  window.open(`${BASE}/download/shap`);
}

function resetAll() {
  fetch(`${BASE}/reset`, { method: "POST" }).then(() => location.reload());
}





