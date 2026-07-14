// =====================================================
// TenderIQ Compare Report
// compare.js
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("✅ Comparison Report Loaded");

    // ==========================================
    // Score Circle Animation
    // ==========================================

    const scoreCircle = document.querySelector(".score-circle");

    if (scoreCircle) {

        scoreCircle.animate(

            [

                {
                    transform: "scale(0.5)",
                    opacity: 0
                },

                {
                    transform: "scale(1)",
                    opacity: 1
                }

            ],

            {

                duration: 700,

                easing: "ease-out"

            }

        );

    }

    // ==========================================
    // Progress Bar Animation
    // ==========================================

    const progressBar = document.getElementById("progressBar");

    if (progressBar) {

        const progress = progressBar.dataset.progress;

        progressBar.style.width = "0%";

        setTimeout(() => {

            progressBar.style.width = progress + "%";

        }, 100);

    }

    // ==========================================
    // Animated Percentage Counter
    // ==========================================

    if (scoreCircle) {

        const finalValue = parseFloat(

            scoreCircle.innerText.replace("%", "")

        );

        let current = 0;

        const interval = setInterval(function () {

            current += 1;

            scoreCircle.innerHTML = current + "%";

            if (current >= finalValue) {

                scoreCircle.innerHTML = finalValue + "%";

                clearInterval(interval);

            }

        }, 20);

    }

    // ==========================================
    // Print Button
    // ==========================================

    const printButton = document.querySelector(".print-btn");

    if (printButton) {

        printButton.addEventListener(

            "click",

            function () {

                const confirmPrint = confirm(

                    "Do you want to print this comparison report?"

                );

                if (confirmPrint) {

                    window.print();

                }

            }

        );

    }

    console.log("✅ Compare Module Ready");

});