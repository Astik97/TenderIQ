// =====================================================
// Compare JavaScript
// =====================================================

document.addEventListener("DOMContentLoaded", function(){

    // ==========================================
    // Score Circle Animation
    // ==========================================

    const scoreCircle = document.querySelector(".score-circle");

    if (scoreCircle){

        scoreCircle.animate(
            
            [

                {transform: "scale(0.5)",opacity: 0},

                {transform: "scale(1)",opacity: 1}
            
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

    if (progressBar){

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

        const finalValue = parseFloat(scoreCircle.innerText.replace("%", ""));

        const step = finalValue / 50;

        let current = 0;

        const interval = setInterval(function () {

            current += step;

            if (current >= finalValue)
                
            {
                
                current = finalValue;

                clearInterval(interval);
            }

            scoreCircle.innerHTML = current.toFixed(2) + "%";

        }, 20);

    }

    // =======================================
    // Search Box
    // =======================================

    const searchInput=document.getElementById("clauseSearch");
    
    if(searchInput)
        
    {
        
        searchInput.addEventListener("keyup",function(){

        const value=this.value.toLowerCase();

        const cards=document.querySelectorAll(".clause-card");

        cards.forEach(card=>{

        const text=card.innerText.toLowerCase();

        card.style.display=text.includes(value)?"block":"none";
    
    });
    
    });
}

    // ==========================================
    // Print Button
    // ==========================================

    const printButton = document.querySelector(".print-btn");

    if (printButton){

        printButton.addEventListener("click",

            function(){

                if
                (
                    confirm("Do you want to print this comparison report?")
                )

                { 
                    window.print(); 
                }

            });

        }

    document.querySelectorAll(".risk-box").forEach(card=>{
        
        if(card.dataset.risk==="Critical Risk"){
            
            card.animate(
            
            [
                
                {transform:"translateX(-5px)"},
                
                {transform:"translateX(5px)"},
                
                {transform:"translateX(0px)"}
            ],
                
            {
                duration:400
            }

        );
    
    }

    });

});