from werkzeug.security import generate_password_hash, check_password_hash
from main import User, CheckEmailValidity, CheckPasswordStrength

registered_users = []

def findUserByEmail(email):
    for user in registered_users:
        if user.email == email:
            return user
    return None

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
    
    new_user = User(name, email, hashedPassword)
    registered_users.append(new_user)
    return True, "User registered successfully"

def loginUser(email,password):
    user = findUserByEmail(email)
    
    if user is None:
        return False, "User not found"
    
    if not check_password_hash(user.password, password):
        return False, "Incorrect password"
    return True, "Login successful"

def logoutUser():
    return True, "User logged out successfully"