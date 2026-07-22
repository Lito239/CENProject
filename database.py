import json
class PythonDatabase:
    def __init__(self):
        self.filename = "finance_data.json"
        self.data = {"users": [], "cards": [], "transactions": []}
        self.next_ids = {"users": 1, "cards": 1, "transactions": 1}
        self.load()
    def load(self):
        try:
            with open(self.filename, "r") as file:
                saved = json.load(file)
                self.data = saved["data"]
                self.next_ids = saved["next_ids"]
        except (FileNotFoundError, json.JSONDecodeError):
            self.save()
    def save(self):
        with open(self.filename, "w") as file:
            json.dump({"data": self.data, "next_ids": self.next_ids}, file, indent=4)
    def add_user(self, username, email=None, password=None):
        for everyuser in self.data["users"]:
            if everyuser["username"] == username:
                return "username already exists"
            if everyuser["email"] == email:
                return "email already exists"
        new_user = {
            "id": self.next_ids["users"],
            "username": username,
            "email": email,
            "password": password,
        }
        self.data["users"].append(new_user)
        self.next_ids["users"] += 1
        self.save()
        return new_user["id"]
    def login(self, username, password):
        for user in self.data["users"]:
            if user["username"] == username and user["password"] == password:
                return True
        return False
    def get_user(self, user_id):
        for user in self.data["users"]:
            if user["id"] == user_id:
                return user
        return None
    def get_user_by_email(self, email):
        for user in self.data["users"]:
            if user["email"].lower() == email.lower():
                return user
        return None
    def update_user(self, user_id, user_object):
        for stored_user in self.data["users"]:
            if stored_user["id"] == user_id:
                stored_user["username"] = user_object.name
                stored_user["email"] = user_object.email
                stored_user["password"] = user_object.password
                self.save()
                return True
        return False
    def add_card(self, user_id, card):
        new_card = {
            "id": self.next_ids["cards"],
            "user_id": user_id,
            "card_type": card.card_type,
            "cardholder_name": card.cardholder_name,
            "expiration_date": card.expiration_date,
            "is_debit": card.is_debit,
            "balance": card.balance
        }
        self.data["cards"].append(new_card)
        self.next_ids["cards"] += 1
        self.save()
        return new_card["id"]
    def get_cards(self, user_id):
        return [card for card in self.data["cards"] if card["user_id"] == user_id]
    def update_card(self, card_id, user_id, card_object):
        for stored_card in self.data["cards"]:
            if (stored_card["id"] == card_id and stored_card["user_id"] == user_id):
                stored_card["card_type"] = card_object.card_type
                stored_card["cardholder_name"] = (card_object.cardholder_name)
                stored_card["expiration_date"] = (card_object.expiration_date)
                stored_card["is_debit"] = card_object.is_debit
                stored_card["balance"] = card_object.balance
                self.save()
                return True
        return False
    def add_transaction(self, user_id, card_id, transaction_name, amount=None, transaction_date=None, category=None):
        new_transaction = {
            "id": self.next_ids["transactions"],
            "user_id": user_id,
            "card_id": card_id,
            "transaction_name": transaction_name,
            "amount": amount,
            "transaction_date": transaction_date,
            "category": category,
        }
        self.data["transactions"].append(new_transaction)
        self.next_ids["transactions"] += 1
        self.save()
        return new_transaction["id"]

    def get_transactions(self, user_id):
        return [transaction for transaction in self.data["transactions"] if transaction["user_id"] == user_id]

    def update_transaction(self, transaction_id, user_id, transaction_name=None, amount=None, card_id=None, transaction_date=None, category=None):
        expense_object = transaction_name if hasattr(transaction_name, "date_day") else None
        for transaction in self.data["transactions"]:
            if transaction["id"] == transaction_id and transaction["user_id"] == user_id:
                if expense_object is not None:
                    transaction["transaction_name"] = expense_object.description
                    transaction["amount"] = expense_object.amount
                    transaction["transaction_date"] = f"{expense_object.date_year:04d}-{expense_object.date_month:02d}-{expense_object.date_day:02d}"
                    transaction["category"] = expense_object.category
                else:
                    if transaction_name is not None:
                        transaction["transaction_name"] = transaction_name
                    if amount is not None:
                        transaction["amount"] = amount
                    if card_id is not None:
                        transaction["card_id"] = card_id
                    if transaction_date is not None:
                        transaction["transaction_date"] = transaction_date
                    if category is not None:
                        transaction["category"] = category
                self.save()
                return True
        return False

    def delete_transaction(self, transaction_id, user_id):
        for transaction in self.data["transactions"]:
            if transaction["id"] == transaction_id and transaction["user_id"] == user_id:
                self.data["transactions"].remove(transaction)
                self.save()
                return True
        return False
