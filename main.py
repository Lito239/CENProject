class Card:
    def __init__(self, card_number, cardholder_name, expiration_date, cvv):
        self.card_number = card_number
        self.cardholder_name = cardholder_name
        self.expiration_date = expiration_date
        self.cvv = cvv

    def __str__(self):
        return f"Card(card_number='{self.card_number}', cardholder_name='{self.cardholder_name}', expiration_date='{self.expiration_date}')"
    
    def edit_card(self, card_number=None, cardholder_name=None, expiration_date=None, cvv=None):
        if card_number is not None:
            self.card_number = card_number
        if cardholder_name is not None:
            self.cardholder_name = cardholder_name
        if expiration_date is not None:
            self.expiration_date = expiration_date
        if cvv is not None:
            self.cvv = cvv

class Expense:
    def __init__(self, amount, category, DOTW, day, month, year, card, description=""):
        self.amount = amount
        self.category = category
        self.date_DOTW = DOTW #Day of the week (Monday, Tuesday, etc.)
        self.date_day = day
        self.date_month = month
        self.date_year = year
        self.card = card
        self.description = description

    def __str__(self):
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date_DOTW}, {self.date_day}/{self.date_month}/{self.date_year}', card='{self.card}', description='{self.description}')"

    def edit_expense(self, amount=None, category=None, DOTW=None, day=None, month=None, year=None, card=None, description=None):
        if amount is not None:
            self.amount = amount
        if category is not None:
            self.category = category
        if DOTW is not None:
            self.date_DOTW = DOTW
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
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password #Maybe check strength of password, Suggested password generator?
        self.expenses = []

    #Methods
    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_expense(self, expense):
        if expense in self.expenses:
            self.expenses.remove(expense)
        else:
            print("Expense not found.")

    def print_expenses(self):
        for expense in self.expenses:
            print(expense)

    def edit_user(self, name=None, email=None, password=None):
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password

def CheckEmailValidity(email):
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

def CheckPasswordStrength(password): #Change to rating system (1-4?)
    if len(password) < 8:
        return False
    return True

def main():
    #Only for testing
    user = User("J", "j@j.com", "pass")
    OneExpense = Expense(10, "Food", "Monday", 1, 1, 2024, "Visa", "Lunch")
    user.add_expense(OneExpense)
    TwoExpense = Expense(20, "Flood", "Tuesday", 2, 2, 2024, "Visa", "Lunch")
    user.add_expense(TwoExpense)
    ThreeExpense = Expense(30, "Frodo", "Wednesday", 3, 3, 2024, "Visa", "Brunch")
    user.add_expense(ThreeExpense)
    user.print_expenses()
    user.expenses[0].edit_expense(amount=50, description="Dinner")
    print(user.expenses[0])
    print(CheckEmailValidity("user@example.com"))
    print(CheckEmailValidity("test"))
    print(CheckEmailValidity("test@test"))
    print(CheckEmailValidity("test@test."))
    print(CheckEmailValidity("@test.com"))
    print(CheckEmailValidity("test@test.c1m"))
    print(CheckEmailValidity("test.test@com"))
    print(CheckEmailValidity("test@test.com"))
    pass

if __name__ == "__main__":
    main()
