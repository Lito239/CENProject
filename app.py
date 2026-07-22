from flask import Flask, render_template, request, redirect, url_for, session
from auth import registerUser, loginUser

app = Flask(__name__)
app.secret_key = "currencycare-development-key"

@app.route("/")
def index():
    return redirect(url_for("loginPage"))

@app.route("/login", methods=["GET", "POST"])
def loginPage():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        loginSuccessful, loginMessage = loginUser(username, password)
        if loginSuccessful:
            session["username"] = username
            return redirect(url_for("homePage"))
        
        return render_template(
            "login_screen.html", 
            loginMessage = loginMessage)
    return render_template("login_screen.html")

@app.route("/register", methods=["GET", "POST"])
def registerPage():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        registrationSuccessful, registrationMessage = registerUser(username, email, password)
        if registrationSuccessful:
            session["username"] = username
            return redirect(url_for("loginPage"))
        
        return render_template(
            "singin_screen.html", 
            registrationMessage = registrationMessage)
    return render_template("singin_screen.html")

@app.route("/home", methods=["GET"])
def homePage():
    if "username" not in session:
        return redirect(url_for("loginPage"))
    return render_template("home_screen.html")

@app.route("/logout", methods=["GET"])
def logoutPage():
    session.clear()
    return redirect(url_for("loginPage"))

if __name__ == "__main__":
    app.run(debug=True)