document.getElementById("signinForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    var get_email = document.getElementById("email").value;
    var get_username = document.getElementById("username").value;

    // check if either email or user name were already taken
    // later will look through a database
    if (get_email === "test@gmail.com") {
        alert("Email already exists");
    }
    else if (get_username === "test") {
        alert("Username already taken");
    }
    else {
        window.location.href = "home_screen.html";
    }
});