class Goal:
    def __init__(self, max_spending, current_spending):
        self.max_spending = max_spending
        self.current_spending = current_spending

    def __str__(self):
        return f"Goal(max_spending={self.max_spending}, current_spending={self.current_spending})"
    
    def update_spending(self, amount):
        self.current_spending += amount
    
    def edit_max_spending(self, new_max_spending):
        self.max_spending = new_max_spending

class Card:
    def __init__(self, card_type, cardholder_name, expiration_date, is_debit, balance):
        self.card_type = card_type
        self.cardholder_name = cardholder_name
        self.expiration_date = expiration_date
        self.is_debit = is_debit
        self.balance = balance

    def __str__(self):
        return f"Card(card_type='{self.card_type}', cardholder_name='{self.cardholder_name}', expiration_date='{self.expiration_date}', is_debit={self.is_debit}, balance={self.balance})"

    def edit_card(self, card_type=None, cardholder_name=None, expiration_date=None, is_debit=None, balance=None):
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
    def __init__(self, amount, category, day, month, year, card, description=""):
        self.amount = amount
        self.category = category
        self.date_day = day
        self.date_month = month
        self.date_year = year
        self.card = card
        self.description = description

    def __str__(self):
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date_day}/{self.date_month}/{self.date_year}', card='{self.card}', description='{self.description}')"

    def edit_expense(self, amount=None, category=None, day=None, month=None, year=None, card=None, description=None):
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
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password #Maybe check strength of password
        self.expenses = []
        self.goals = []

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

    def add_goal(self, goal):
        self.goals.append(goal)

    def remove_goal(self, goal):
        if goal in self.goals:
            self.goals.remove(goal)
        else:
            print("Goal not found.")

    def get_expenses_year(self, year):
        return [expense for expense in self.expenses if expense.date_year == year]
    
    def get_expenses_month(self, month, year):
        return [expense for expense in self.expenses if expense.date_month == month and expense.date_year == year]
    
    def get_expenses_week(self, start_date, month, year):
        return [expense for expense in self.expenses if expense.date_day >= start_date and expense.date_day <= start_date + 6 and expense.date_month == month and expense.date_year == year]

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

def CheckPasswordStrength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char.isupper() for char in password) and any(char.islower() for char in password):
        score += 1
    if any(not char.isalnum() for char in password):
        score += 1
    return score

def RandomPasswordGenerator(length=12):
    import random
    import string
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return password

def main():
    #Only for testing
    user = User("J", "j@j.com", "pass")
    OneExpense = Expense(10, "Food", 1, 1, 2024, "Visa", "Lunch")
    user.add_expense(OneExpense)
    TwoExpense = Expense(20, "Flood", 2, 2, 2024, "Visa", "Lunch")
    user.add_expense(TwoExpense)
    ThreeExpense = Expense(30, "Frodo", 3, 3, 2024, "Visa", "Brunch")
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
    print(RandomPasswordGenerator())
    pass

if __name__ == "__main__":
    main()
