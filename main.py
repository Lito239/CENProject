"""
Backend module for CurrencyCare.

This module manages backend connections and user financial data.
"""
class Card:
    """Handles all backend operations in regards to cards for CurrencyCare."""
    def __init__(self, card_type, cardholder_name, expiration_date, is_debit, balance):
        self.card_type = card_type
        self.cardholder_name = cardholder_name
        self.expiration_date = expiration_date
        self.is_debit = is_debit
        self.balance = balance

    def __str__(self):
        """Create a string representation of the object."""
        return (f"Card(card_type='{self.card_type}', cardholder_name='{self.cardholder_name}', "
                f"expiration_date='{self.expiration_date}', is_debit={self.is_debit}, "
                f"balance={self.balance})")

    def edit_card(self, card_type=None, cardholder_name=None,
                  expiration_date=None, is_debit=None, balance=None):
        """Edit an existing card object."""
        if card_type is not None:
            self.card_type = card_type
        if cardholder_name is not None:
            self.cardholder_name = cardholder_name
        if expiration_date is not None:
            self.expiration_date = expiration_date
        if is_debit is not None:
            self.is_debit = is_debit
        if balance is not None:
            self.balance = balance

class Expense:
    """Handles all backend operations in regards to expenses for CurrencyCare."""
    def __init__(self, amount, category, day, month, year, card, description=""):
        self.amount = amount
        self.category = category
        self.date_day = day
        self.date_month = month
        self.date_year = year
        self.card = card
        self.description = description

    def __str__(self):
        """Create a string representation of the object."""
        return (f"Expense(amount={self.amount}, category='{self.category}', "
                f"date='{self.date_day}/{self.date_month}/{self.date_year}', "
                f"card='{self.card}', description='{self.description}')")

    def edit_expense(self, amount=None, category=None,
                     day=None, month=None, year=None, card=None, description=None):
        """Edit an existing expense object."""
        if amount is not None:
            self.amount = amount
        if category is not None:
            self.category = category
        if day is not None:
            self.date_day = day
        if month is not None:
            self.date_month = month
        if year is not None:
            self.date_year = year
        if card is not None:
            self.card = card
        if description is not None:
            self.description = description

class User:
    """Handles all user operations in regards to users for CurrencyCare."""
    def __init__(self, name, email, password):
        """Initialize the user object."""
        self.name = name
        self.email = email
        self.password = password #Maybe check strength of password
        self.expenses = []

    #Methods
    def add_expense(self, expense):
        """Add an expense to the user."""
        self.expenses.append(expense)

    def remove_expense(self, expense):
        """Remove an expense from the user."""
        if expense in self.expenses:
            self.expenses.remove(expense)
        else:
            print("Expense not found.")

    def print_expenses(self):
        """Print the expenses stored in the user."""
        for expense in self.expenses:
            print(expense)

    def edit_user(self, name=None, email=None, password=None):
        """Edit an existing user object."""
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password

def CheckEmailValidity(email):
    """Check if an email address is valid."""
    if "@" not in email or "." not in email:
        return False
    last_dot = email.rfind(".")
    last_at = email.rfind("@")
    if last_at <= 0 or last_dot < last_at:
        return False
    if last_dot == len(email) - 1:
        return False
    if not email[last_dot + 1:].isalpha():
        return False
    return True

def CheckPasswordStrength(password):
    """Check if a password is good enough to our standard."""
    score = 0
    if len(password) >= 8:
        score += 1
    if any(character.isdigit() for character in password):
        score += 1
    if (any(character.isupper() for character in password) and
            any(character.islower() for character in password)):
        score += 1
    special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
    if any(character in special_characters for character in password):
        score += 1
    return score

def RandomPasswordGenerator(length=12):
    """Generate a random password."""
    import random
    import string
    password = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    #Change to check if the password is string enough
    return password

def main():
    pass

if __name__ == "__main__":
    main()
