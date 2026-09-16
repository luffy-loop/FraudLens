const originalFetch = window.fetch;

window.fetch = async function(...args) {
    const response = await originalFetch(...args);
    const url = typeof args[0] === "string" ? args[0] : args[0]?.url;

    if (url && url.includes("/predict")) {
        response.clone().json().then(data => {
            renderShap(data);
        }).catch(() => {});
    }

    return response;
};

function renderShap(data) {
    const list = document.getElementById("shapList");

    if (!list) return;

    list.innerHTML = "";

    if (!Array.isArray(data.shap_explanations) || data.shap_explanations.length === 0) {
        list.innerHTML = '<div class="risk-signal-empty">SHAP explanation unavailable</div>';
        return;
    }

    data.shap_explanations.forEach(item => {
        const row = document.createElement("div");
        row.className = "shap-item";

        const value = Number(item.shap_value);
        const direction = item.direction === "fraud" ? "fraud" : "legitimate";
        const sign = value >= 0 ? "+" : "";

        row.innerHTML = `
            <div class="shap-item-main">
                <strong class="shap-feature">${item.feature}</strong>
                <span class="shap-value ${direction}">${sign}${value.toFixed(6)}</span>
            </div>
            <div class="shap-direction">Pushes toward ${direction}</div>
        `;

        list.appendChild(row);
    });
}
