const monitoringDemo = {
    total: 100,
    flagged: 8,
    legitimate: 92,
    fraudRate: 8.0,
    meanProbability: 0.142,
    referenceMeanProbability: 0.118,
    probabilityShift: 0.024,
    driftStatus: "STABLE"
};

function renderMonitoring() {
    const ids = {
        monitoringTotal: monitoringDemo.total,
        monitoringFlagged: monitoringDemo.flagged,
        monitoringFraudRate: `${monitoringDemo.fraudRate.toFixed(2)}%`,
        monitoringMean: monitoringDemo.meanProbability.toFixed(3),
        monitoringShift: `${monitoringDemo.probabilityShift >= 0 ? "+" : ""}${monitoringDemo.probabilityShift.toFixed(3)}`,
        monitoringStatus: monitoringDemo.driftStatus
    };

    Object.entries(ids).forEach(([id, value]) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    });
}

document.addEventListener("DOMContentLoaded", renderMonitoring);
