"""
The authorization module for CurrencyCare.

This module manages every authorization when loggin into currency care.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from main import CheckEmailValidity, CheckPasswordStrength
from database import PythonDatabase
database = PythonDatabase()

def findUserByEmail(email):
    """Find a user by email."""
    return database.get_user_by_email(email)

def findUserByUsername(username):
    """Find a user by username."""
    return database.get_user_by_username(username)

def getPasswordStrengthLevel(password):
    """Get password strength level."""
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
    """Register a new user."""
    if not CheckEmailValidity(email):
        return False, "Invalid email format"
    password_score, password_level = getPasswordStrengthLevel(password)
    if password_score < 3:
        return False, f"Password is too weak. Strength: {password_level}"
    if findUserByEmail(email) is not None:
        return False, "Email is already registered"
    hashed_password = generate_password_hash(password)
    result = database.add_user(
        username=name,
        email=email,
        password=hashed_password
    )
    if result == "username already exists":
        return False, "Username is already registered"
    if result == "email already exists":
        return False, "Email is already registered"
    return True, "User registered successfully"

def loginUser(user_name, password):
    """Login a user."""
    user = findUserByUsername(user_name)
    if user is None:
        return False, "User not found"
    if not check_password_hash(user["password"], password):
        return False, "Incorrect password"
    return True, "Login successful"

def logoutUser():
    """Logout a user."""
    return True, "User logged out successfully"
