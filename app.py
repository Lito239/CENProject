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
            return redirect(url_for("homePage"))

        return render_template(
            "singin_screen.html",
            registrationMessage=registrationMessage)
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
    goals = database.get_goals(user["id"])
    return render_template("home_screen.html", transactions = transactions, username = username, goals=goals)

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
@app.route("/goals", methods=["POST"])
def addGoal():
    if "username" not in session:
        return jsonify({
            "successful": False,
            "message":"You must be logged in."
        }), 401
    goalData=request.get_json()
    if goalData is None:
        return jsonify({
            "successful": False,
            "message": "No goal data received."
        }), 400
    goalName = goalData.get("goalName").strip()
    startDate =goalData.get("startDate")
    endDate=goalData.get("endDate")
    goalAmount= goalData.get("goalAmount")
    if goalName=="" or startDate =="" or endDate =="" or goalAmount in(None, ""):
        return jsonify({
            "successful": False,
            "message": "All goal fields are required."
        }),400
    try:
        goalAmount = float(goalAmount)
    except (TypeError, ValueError):
        return jsonify({
            "successful": False, 
            "message": "Goal amount must be a valid number."
        }),400
    if goalAmount <= 0:
        return jsonify({
            "successful": False,
            "message": "Goal amount must be greater than zero."
        }), 400
    if endDate< startDate:
        return jsonify({
            "successful": False,
            "message": "End date cannot be before start date."
        }), 400
    username = session["username"]
    user =database.get_user_by_username(username)
    if user is None:
        return jsonify({
            "successful": False,
            "message": "Logged-in user could not be found."
        }), 404
    goalID = database.add_goal(
        user["id"], goalName, startDate, endDate, goalAmount
    )
    return jsonify({
        "successful": True, "message": "Goal saved.", "goal":{ "id": goalID, "name": goalName, "startDate":startDate, "endDate": endDate, "goalAmount": goalAmount}
    })
@app.route("/goals/<int:goalID>",methods=["PUT"])
def updateGoal(goalID):
    if "username" not in session:
        return jsonify({
            "successful":False,
            "message": "You must be logged in."
        }),401
    goalData = request.get_json()
    if goalData is None:
        return jsonify({
            "successful": False,
            "message":"No goal data received."
        }),400
    goalName =goalData.get("goalName","").strip()
    startDate=goalData.get("startDate")
    endDate=goalData.get("endDate")
    goalAmount=goalData.get("goalAmount")
    if goalName =="" or startDate=="" or endDate=="" or goalAmount in (None,""):
        return jsonify({
            "successful": False,
            "message":"All goal fields are required."
        }), 400
    try:
        goalAmount = float(goalAmount)
    except (TypeError,ValueError):
        return jsonify({
            "successful": False,
            "message": "Goal amount must be a valid number."
        }),400
    if goalAmount<=0:
        return jsonify({
            "successful": False,
            "message":"Goal amount must be greater than zero."
        }), 400
    if endDate< startDate:
        return jsonify({
            "successful": False,
            "message": "End date cannot be before start date."
        }), 400
    username = session["username"]
    user = database.get_user_by_username(username)
    if user is None:
        return jsonify({
            "successful": False,
            "message": "Logged-in user could not be found."
        }), 404
    goalUpdated = database.update_goal(goalID, user["id"], goalName, startDate, endDate, goalAmount)
    if not goalUpdated:
        return jsonify({
            "successful": False, "message": "Goal could not be found."
        }), 404
    return jsonify({
        "successful": True, "message":"Goal updated.", "goal":{ "id": goalID, "name": goalName,"startDate": startDate,
                                                               "endDate":endDate,"goalAmount":goalAmount}
    })
@app.route("/goals/<int:goalID>", methods=["DELETE"])
def deleteGoal(goalID):
    if"username" not in session: 
        return jsonify({
            "successful":False, "message": "You must be logged in."
        }),401
    username=session["username"]
    user =database.get_user_by_username(username)
    if user is None:
        return jsonify({
            "successful":False,
            "message": "Logged-in user could not be found."
        }),404
    goalDeleted=database.delete_goal(
        goalID, user["id"]
    )
    if not goalDeleted:
        return jsonify({
            "successful": False, "message": "Goal could not be found."
        }),404
    return jsonify({
        "successful":True, "message":"Goal deleted."
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

def editTransaction(transactionID):
    if "username" not in session:
        return jsonify({
            "successful": False,
            "message": "You must be logged in."
        }), 401
    transactionData = request.get_json(silent=True)
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
    user = database.get_user_by_username(session["username"])
    if user is None:
        return jsonify({
            "successful": False,
            "message": "Logged-in user could not be found."
        }), 404
    transactionUpdated = database.update_transaction(
        transaction_id=transactionID,
        user_id=user["id"],
        transaction_name=transactionName,
        amount=amount,
        transaction_date=transactionDate,
        category=category,
        card_name=cardName
    )
    if not transactionUpdated:
        return jsonify({
            "successful": False,
            "message": "Transaction could not be updated."
        }), 404
    return jsonify({
        "successful": True,
        "message": "Transaction updated.",
        "transaction": {
            "id": transactionID,
            "name": transactionName,
            "amount": amount,
            "card": cardName,
            "date": transactionDate,
            "filter": category
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
