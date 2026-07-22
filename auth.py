from werkzeug.security import generate_password_hash, check_password_hash
from main import User, CheckEmailValidity, CheckPasswordStrength
from database import PythonDatabase

database = PythonDatabase()

def findUserByEmail(email):
    return database.get_user_by_email(email)

def findUserByUsername(username):
    return database.get_user_by_username(username)

def getPasswordStrengthLevel(password):
    score = CheckPasswordStrength(password)
    
    if score< 1:
        score = 1
    if score > 4:
        score = 4
    levels = {
        1: "Very Weak",
        2: "Weak",
        3: "Strong",
        4: "Very Strong"
    }
    return score, levels[score]

def registerUser(name, email, password):
    if not CheckEmailValidity(email):
        return False, "Invalid email format"
    passwordScore, passwordLevel = getPasswordStrengthLevel(password)
    if passwordScore < 3:
        return False, f"Password is too weak. Strength: {passwordLevel}"
    if findUserByEmail(email) is not None:
        return False, "Email is already registered"
    
    hashedPassword = generate_password_hash(password)
    result = database.add_user(
        username=name,
        email=email,
        password=hashedPassword
    )
    if result == "username already exists":
        return False, "Username is already registered"
    if result == "email already exists":
        return False, "Email is already registered"
    return True, "User registered successfully"

def loginUser(userName, password):
    user = findUserByUsername(userName)
    
    if user is None:
        return False, "User not found"
    
    if not check_password_hash(user["password"], password):
        return False, "Incorrect password"
    return True, "Login successful"

def logoutUser():
    return True, "User logged out successfully"
