
document.addEventListener("DOMContentLoaded", function () {

    console.log("Comparison Report Loaded");

    const score = document.querySelector(".score-circle");

    if(score){

        score.animate(

            [

                {

                    transform:"scale(0.5)",

                    opacity:0

                },

                {

                    transform:"scale(1)",

                    opacity:1

                }

            ],

            {

                duration:700,

                easing:"ease-out"

            }

        );

    }

});