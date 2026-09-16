const modelData = [
    { name: "Logistic Regression", precision: 5.64, recall: 87.37, f1: 10.59, roc: 96.56, pr: 67.19 },
    { name: "Decision Tree", precision: 6.83, recall: 83.16, f1: 12.62, roc: 91.48, pr: 46.96 },
    { name: "Random Forest", precision: 77.66, recall: 76.84, f1: 77.25, roc: 97.46, pr: 78.22 }
];

function addComparisonStyles() {
    const s = document.createElement("style");
    s.textContent = `
        .comparison-panel{margin:26px 0;padding:28px;border:1px solid var(--border);border-radius:var(--radius);background:linear-gradient(145deg,rgba(17,25,37,.94),rgba(10,14,21,.94));box-shadow:var(--shadow)}
        .model-table{margin-top:20px;overflow-x:auto;border:1px solid var(--border);border-radius:12px}
        .model-row{display:grid;grid-template-columns:1.7fr repeat(5,1fr);min-width:760px;border-bottom:1px solid var(--border)}
        .model-row:last-child{border-bottom:0}
        .model-row>*{padding:15px 14px;font-size:12px}
        .model-row span{text-align:right;color:var(--muted);font-variant-numeric:tabular-nums}
        .model-row strong{font-weight:750}
        .model-head{background:rgba(255,255,255,.025)}
        .model-head>*{color:var(--muted-2)!important;font-size:9px!important;font-weight:850;letter-spacing:.12em}
        #modelComparisonBody .model-row:last-child{background:rgba(61,126,255,.055)}
        #modelComparisonBody .model-row:last-child strong{color:var(--accent)}
        .comparison-note{margin-top:15px;color:var(--muted-2);font-size:11px;line-height:1.65}
        @media(max-width:800px){.comparison-panel{padding:20px}.model-row>*{padding:13px 10px}}
    `;
    document.head.appendChild(s);
}

function renderModelComparison() {
    const body = document.getElementById("modelComparisonBody");
    if (!body) return;
    body.innerHTML = modelData.map(m => `
        <div class="model-row">
            <strong>${m.name}</strong>
            <span>${m.precision.toFixed(2)}%</span>
            <span>${m.recall.toFixed(2)}%</span>
            <span>${m.f1.toFixed(2)}%</span>
            <span>${m.roc.toFixed(2)}%</span>
            <span>${m.pr.toFixed(2)}%</span>
        </div>
    `).join("");
}

document.addEventListener("DOMContentLoaded", () => {
    addComparisonStyles();
    renderModelComparison();
});
