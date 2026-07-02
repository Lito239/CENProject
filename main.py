class Card:
    def __init__(self, card_number, cardholder_name, expiration_date, cvv):
        self.card_number = card_number
        self.cardholder_name = cardholder_name
        self.expiration_date = expiration_date
        self.cvv = cvv

    def __str__(self):
        return f"Card(card_number='{self.card_number}', cardholder_name='{self.cardholder_name}', expiration_date='{self.expiration_date}')"

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
        self.password = password #Maybe check strength of password
        self.expenses = []

    #Methods
    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_expense(self, expense):
        if expense in self.expenses:
            self.expenses.remove(expense)
        else:
            print("Expense not found.")

def CheckEmailValidity(email):
    if "@" not in email or "." not in email:
        return False
    return True

def main():
    #Only for testing
    NewExpense = Expense(10, "Food", "Monday", 1, 1, 2024, "Visa", "Lunch")
    print(NewExpense)
    NewExpense.edit_expense(amount=30, description="Dinner")
    print(NewExpense)
    print(CheckEmailValidity("user@example.com"))
    print(CheckEmailValidity("test"))
    pass

if __name__ == "__main__":
    main()
