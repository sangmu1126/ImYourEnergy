document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById("signup-modal");
    const btn = document.getElementById("signup-complete");
    const span = document.getElementsByClassName("close")[0];
    const loginButton = document.getElementById("login-button");
  
    btn.onclick = function () {
      modal.style.display = "block";
    }
  
    span.onclick = function () {
      modal.style.display = "none";
    }
  
    window.onclick = function (event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
  
    loginButton.onclick = function () {
      window.location.href = "../newjeanse_loginpage/NewJeanSeLoginPage.html"; // Replace with the actual login page URL
    }
  });
  