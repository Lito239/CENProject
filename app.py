from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import registerUser, loginUser, database

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
    username = session["username"]
    user = database.get_user_by_username(username)
    if user is None:
        session.clear()
        return redirect(url_for("loginPage"))
    transactions = database.get_transactions(user["id"])
    return render_template("home_screen.html", transactions = transactions, username = username)

@app.route("/logout", methods=["GET"])
def logoutPage():
    session.clear()
    return redirect(url_for("loginPage"))

@app.route("/transactions", methods = ["POST"])
def addTransaction():
    if "username" not in session:
        return jsonify({
            "successful": False,
            "message": "You must be logged in."
        }), 401
    transactionData = request.get_json()

    if transactionData is None:
        return jsonify({
            "successful": False,
            "message": "No transaction data received."
        }),400
    transactionName = transactionData.get("transactionName", "").strip()
    amount = transactionData.get("amount")
    transactionDate = transactionData.get("transactionDate")
    category = transactionData.get("category")
    cardName = transactionData.get("card", "").strip()

    if transactionName == "" or amount in (None, ""):
        return jsonify({
            "successful": False, 
            "message": "Transaction name and amount are required."
        }), 400
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({
            "successful": False,
            "message": "Amount must be a valid number."
        }), 400
    username = session["username"]
    user = database.get_user_by_username(username)

    if user is None:
        return jsonify({
            "successful": False,
            "message": "Logged-in user could not be found."
        }), 404
    transactionID = database.add_transaction(
        user["id"],
        None,
        transactionName,
        amount,
        transactionDate,
        category,
        cardName
    )
    return jsonify({
        "successful": True,
        "message": "Transaction saved.",
        "transaction":{
            "id": transactionID,
            "name": transactionName,
            "amount": amount,
            "card": transactionData.get("card", ""),
            "date": transactionDate,
            "filter": category
        }
    })

@app.route("/transactions/<int:transactionID>", methods=["DELETE"])
def deleteTransaction(transactionID):
    if "username" not in session:
        return jsonify({
            "successful": False, 
            "message": "You must be logged in."
        }), 401
    username = session["username"]
    user = database.get_user_by_username(username)
    if user is None:
        return jsonify({
            "successful": False,
            "message": "Logged-in user could not be found."
        }), 404
    transactionDeleted = database.delete_transaction(
        transactionID,
        user["id"]
    )
    if not transactionDeleted:
        return jsonify({
            "successful": False,
            "message": "Transaction could not be found."
        }), 404
    return jsonify({
        "successful": True,
        "message": "Transaction deleted."
    })
if __name__ == "__main__":
    app.run(debug=True)
