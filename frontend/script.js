const form = document.getElementById("fraudForm");

const resultCard = document.getElementById("result");
const resultText = document.getElementById("resultText");
const probabilityText = document.getElementById("probabilityText");
const thresholdText = document.getElementById("thresholdText");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const transaction = {};

    transaction["Time"] =
        Number(document.getElementById("Time").value);

    for (let i = 1; i <= 28; i++) {

        transaction[`V${i}`] =
            Number(document.getElementById(`V${i}`).value);
    }

    transaction["Amount"] =
        Number(document.getElementById("Amount").value);


    resultCard.classList.remove("hidden");

    resultText.textContent = "Analyzing...";
    probabilityText.textContent = "—";


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
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
            throw new Error(data.error || "Prediction failed");
        }


        resultText.textContent = data.result;

        probabilityText.textContent =
            `${(data.fraud_probability * 100).toFixed(2)}%`;

        thresholdText.textContent =
            data.threshold;


    } catch (error) {

        resultText.textContent = "ERROR";

        probabilityText.textContent =
            error.message;
    }

});
