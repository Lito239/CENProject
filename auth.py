from werkzeug.security import generate_password_hash, check_password_hash
from main import User, CheckEmailValidity, CheckPasswordStrength

registered_users = []

def find_user_by_email(email):
    for user in registered_users:
        if user.email == email:
            return user
    return None

def register_user(name, email, password):
    if not CheckEmailValidity(email):
        return False, "Invalid email format"
    if not CheckPasswordStrength(password):
        return False, "Password must be at least 6 characters"
    if find_user_by_email(email) is not None:
        return False, "Email is already registered"
    
    hashed_password = generate_password_hash(password)
    
    new_user = User(name, email, hashed_password)
    registered_users.append(new_user)
    return True, "User registered successfully"

def login_user(email,password):
    user = find_user_by_email(email)
    
    if user is None:
        return False, "User not found"
    if not check_password_hash(user.password, password):
        return False, "Incorrect password"
    return True, "Login successful"

def logout_user():
    return True, "User logged out successfully"