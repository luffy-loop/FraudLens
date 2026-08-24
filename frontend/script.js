const API_URL = "http://127.0.0.1:5000/predict";

const modeButtons = document.querySelectorAll(".mode-card");

const demoMode = document.getElementById("demoMode");
const csvMode = document.getElementById("csvMode");
const advancedMode = document.getElementById("advancedMode");

const resultCard = document.getElementById("result");
const resultText = document.getElementById("resultText");
const probabilityText = document.getElementById("probabilityText");
const thresholdText = document.getElementById("thresholdText");


// --------------------------------------------------
// SAMPLE TRANSACTION
// --------------------------------------------------

const sampleTransaction = {
    Time: 61290.0,
    V1: 1.2288211502379,
    V2: -0.0634077165201056,
    V3: 0.274145142235826,
    V4: 0.647465021810117,
    V5: -0.0481345611508765,
    V6: 0.372073028593297,
    V7: -0.22423058741343,
    V8: 0.0799390492455152,
    V9: 0.640758817066441,
    V10: -0.273053702248503,
    V11: -1.25272793883718,
    V12: 0.465078770741453,
    V13: 0.400502115321077,
    V14: -0.292841860600363,
    V15: -0.10177401599731,
    V16: -0.399835897844616,
    V17: 0.0343356567914817,
    V18: -0.783550254934187,
    V19: 0.141344900433949,
    V20: -0.0965659023514416,
    V21: -0.129554448055005,
    V22: -0.0837793282428063,
    V23: -0.151661473916324,
    V24: -0.700371597289218,
    V25: 0.598550164523483,
    V26: 0.491409070563651,
    V27: 0.0029892597250263,
    V28: 0.0017822861144491,
    Amount: 11.5
};


// --------------------------------------------------
// MODE SWITCHING
// --------------------------------------------------

modeButtons.forEach(button => {

    button.addEventListener("click", () => {

        const selectedMode = button.dataset.mode;

        modeButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        demoMode.classList.add("hidden");
        csvMode.classList.add("hidden");
        advancedMode.classList.add("hidden");

        if (selectedMode === "demo") {
            demoMode.classList.remove("hidden");
        }

        if (selectedMode === "csv") {
            csvMode.classList.remove("hidden");
        }

        if (selectedMode === "advanced") {
            advancedMode.classList.remove("hidden");
        }

    });

});


// --------------------------------------------------
// DISPLAY RESULT
// --------------------------------------------------

function showResult(data) {

    resultCard.classList.remove("hidden");

    resultText.textContent = data.result;

    probabilityText.textContent =
        `${(data.fraud_probability * 100).toFixed(2)}%`;

    thresholdText.textContent =
        data.threshold;

    document.getElementById(
        "totalTransactions"
    ).textContent = "1";

    document.getElementById(
        "fraudCount"
    ).textContent =
        data.prediction === 1 ? "1" : "0";

    document.getElementById(
        "legitimateCount"
    ).textContent =
        data.prediction === 0 ? "1" : "0";

    document.getElementById(
        "fraudRate"
    ).textContent =
        data.prediction === 1 ? "100%" : "0%";
}


// --------------------------------------------------
// API REQUEST
// --------------------------------------------------

async function predictTransaction(transaction) {

    resultCard.classList.remove("hidden");

    resultText.textContent = "Analyzing...";
    probabilityText.textContent = "—";

    try {

        const response = await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(transaction)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Prediction failed"
            );
        }

        showResult(data);

    } catch (error) {

        resultCard.classList.remove("hidden");

        resultText.textContent = "ERROR";

        probabilityText.textContent =
            error.message;
    }
}


// --------------------------------------------------
// QUICK DEMO
// --------------------------------------------------

document
    .getElementById("demoButton")
    .addEventListener("click", () => {

        predictTransaction(sampleTransaction);

    });


// --------------------------------------------------
// ADVANCED MODE
// --------------------------------------------------

document
    .getElementById("fraudForm")
    .addEventListener("submit", event => {

        event.preventDefault();

        const transaction = {};

        transaction.Time =
            Number(document.getElementById("Time").value);

        for (let i = 1; i <= 28; i++) {

            transaction[`V${i}`] =
                Number(
                    document.getElementById(`V${i}`).value
                );

        }

        transaction.Amount =
            Number(document.getElementById("Amount").value);

        predictTransaction(transaction);

    });

// --------------------------------------------------
// CSV BATCH UPLOAD
// --------------------------------------------------

document
    .getElementById("csvFile")
    .addEventListener("change", async function (event) {

        const file = event.target.files[0];

        if (!file) {
            return;
        }

        try {

            const text = await file.text();

            const rows = text
                .trim()
                .split(/\r?\n/);

            if (rows.length < 2) {
                throw new Error(
                    "CSV file contains no transaction data."
                );
            }

            const headers = rows[0]
                .split(",")
                .map(header => header.trim());

            const requiredFeatures = [
                "Time",
                ...Array.from(
                    { length: 28 },
                    (_, i) => `V${i + 1}`
                ),
                "Amount"
            ];

            const missingFeatures =
                requiredFeatures.filter(
                    feature => !headers.includes(feature)
                );

            if (missingFeatures.length > 0) {

                throw new Error(
                    `Missing columns: ${missingFeatures.join(", ")}`
                );
            }


            resultCard.classList.remove("hidden");

            resultText.textContent =
                "Analyzing CSV...";

            probabilityText.textContent =
                `${rows.length - 1} transactions`;


            let fraudCount = 0;
            let legitimateCount = 0;
            let totalProbability = 0;


            for (let rowIndex = 1; rowIndex < rows.length; rowIndex++) {

                if (!rows[rowIndex].trim()) {
                    continue;
                }

                const values = rows[rowIndex]
                    .split(",")
                    .map(value => value.trim());

                const transaction = {};

                requiredFeatures.forEach(feature => {

                    const index = headers.indexOf(feature);

                    transaction[feature] =
                        Number(values[index]);

                });


                const invalidValues =
                    requiredFeatures.filter(
                        feature =>
                            !Number.isFinite(
                                transaction[feature]
                            )
                    );


                if (invalidValues.length > 0) {

                    throw new Error(
                        `Invalid values in row ${rowIndex + 1}`
                    );
                }


                const response = await fetch(
                    API_URL,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(transaction)
                    }
                );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        `Prediction failed for row ${rowIndex + 1}`
                    );
                }


                totalProbability +=
                    data.fraud_probability;


                if (data.prediction === 1) {
                    fraudCount++;
                } else {
                    legitimateCount++;
                }

            }


            const totalTransactions =
                fraudCount + legitimateCount;


            const fraudRate =
                totalTransactions > 0
                    ? (fraudCount / totalTransactions) * 100
                    : 0;


            const averageProbability =
                totalTransactions > 0
                    ? totalProbability / totalTransactions
                    : 0;


            resultCard.classList.remove("hidden");

resultText.textContent =
    "BATCH ANALYSIS COMPLETE";

document.getElementById(
    "totalTransactions"
).textContent =
    totalTransactions;

document.getElementById(
    "fraudCount"
).textContent =
    fraudCount;

document.getElementById(
    "legitimateCount"
).textContent =
    legitimateCount;

document.getElementById(
    "fraudRate"
).textContent =
    `${fraudRate.toFixed(2)}%`;

probabilityText.textContent =
    `${(averageProbability * 100).toFixed(2)}%`;

thresholdText.textContent =
    "0.65";


        } catch (error) {

            resultCard.classList.remove("hidden");

            resultText.textContent =
                "CSV ERROR";

            probabilityText.textContent =
                error.message;

            thresholdText.textContent =
                "Please check the CSV format.";

        }

    });