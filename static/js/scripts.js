/* ==========================================
   Show / Hide Password
========================================== */

function togglePassword(inputId, icon) {

    const input = document.getElementById(inputId);

    const eye = icon.querySelector("i");

    if (input.type === "password") {

        input.type = "text";

        eye.classList.remove("fa-eye");

        eye.classList.add("fa-eye-slash");
    }

    else
    {
        input.type = "password";

        eye.classList.remove("fa-eye-slash");

        eye.classList.add("fa-eye");
    }
}

/* ==========================================
   Password Strength Checker
========================================== */

const passwordInput = document.getElementById("password");

const strengthBox = document.getElementById("passwordStrength");


if (passwordInput && strengthBox) {

    passwordInput.addEventListener("input", function () {

        const password = passwordInput.value;

        let strength = "";

        let color = "";

        if (password.length === 0) {

            strength = "";

        }

        else if (password.length < 6) {

            strength = "Weak Password";

            color = "#dc2626";

        }

        else if (

            password.match(/[A-Z]/) &&
            password.match(/[a-z]/) &&
            password.match(/[0-9]/)

        ) {

            strength = "Strong Password";

            color = "#16a34a";

        }

        else {

            strength = "Medium Password";

            color = "#f59e0b";

        }

        strengthBox.textContent = strength;

        strengthBox.style.color = color;

    });

}

/* ==========================================
   Confirm Password Validation
========================================== */

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function (event) {

        const password = document.getElementById("password").value;

        const confirmPassword =
            document.getElementById("confirm_password").value;

        if (password !== confirmPassword) {

            alert("Passwords do not match.");

            event.preventDefault();

        }

    });

}

/* ==========================================
   Loading Button Animation
========================================== */

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function () {

        const button = loginForm.querySelector("button");

        button.disabled = true;

        button.innerHTML = "Logging in...";

    });

}

if (registerForm) {

    registerForm.addEventListener("submit", function () {

        const button = registerForm.querySelector("button");

        button.disabled = true;

        button.innerHTML = "Creating Account...";

    });

}

/* ==========================================
   Welcome Message
========================================== */

console.log("TenderIQ Authentication Module Loaded Successfully.");