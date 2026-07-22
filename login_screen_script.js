document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var get_username = document.getElementById("username").value;
    var get_password = document.getElementById("password").value;

    // for now only tests for predefined variables
    // later will look through a database
    if (get_username === "test" && get_password === "test") {
        window.location.href = "home_screen.html";
    }
    else {
        alert("Invalid username or password");
    }
});