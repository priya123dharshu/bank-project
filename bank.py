import mysql.connector

# created Bank class

class Bank:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="dckap",
            password="welcome",  
            database="bank_management"
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.current_user = None

# user Register
    def register(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        email = input("Enter your email: ")

        self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if self.cursor.fetchone():
            print("A user with this email already exists.")
            return

        self.cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        self.conn.commit()
        print("Registration successful!")

# user Login

    def login(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        self.cursor.execute(
            "SELECT * FROM users WHERE name = %s AND password = %s",
            (name, password)
        )
        user = self.cursor.fetchone()
        if user:
            self.current_user = user
            print("Login successful!")
        else:
            print("Invalid credentials.")

# inherite Bank to Account class

class Account(Bank):

    def deposit(self):
        if not self.current_user:
            print("Please log in first.")
            return

        amount = int(input("Enter deposit amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return

        new_balance = self.current_user['balance'] + amount

        self.cursor.execute(
            "UPDATE users SET balance = %s WHERE id = %s",
            (new_balance, self.current_user['id'])
        )
        self.cursor.execute(
            "INSERT INTO transactions (user_id, type, amount, description) VALUES (%s, %s, %s, %s)",
            (self.current_user['id'], 'deposit', amount, 'Deposit')
        )
        self.conn.commit()

        self.current_user['balance'] = new_balance
        print(f"₹{amount} deposited successfully.")

# withdraw method

    def withdraw(self):
        if not self.current_user:
            print("Please log in first.")
            return

        amount = int(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return

        # Check latest balance
        self.cursor.execute("SELECT balance FROM users WHERE id = %s", (self.current_user['id'],))
        balance = self.cursor.fetchone()['balance']

        if amount > balance:
            print("Insufficient funds.")
            return

        new_balance = balance - amount

        # Update balance and log transaction
        self.cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (new_balance, self.current_user['id']))
        self.cursor.execute(
            "INSERT INTO transactions (user_id, type, amount, description) VALUES (%s, %s, %s, %s)",
            (self.current_user['id'], 'withdraw', amount, 'Withdrawal')
        )
        self.conn.commit()

        self.current_user['balance'] = new_balance
        print(f"₹{amount} withdrawn successfully.")

# transfer amount your friends or family

    def transfer(self):
        if not self.current_user:
            print("Please log in first.")
            return

        receiver_email = input("Enter receiver's email: ")
        amount = int(input("Enter transfer amount: "))

        if amount <= 0:
            print("Transfer amount must be positive.")
            return

        # Find receiver
        self.cursor.execute("SELECT * FROM users WHERE email = %s", (receiver_email,))
        receiver = self.cursor.fetchone()

        if not receiver:
            print("Receiver not found.")
            return

        if receiver['id'] == self.current_user['id']:
            print("You cannot transfer money to yourself.")
            return

        # Get sender balance
        self.cursor.execute("SELECT balance FROM users WHERE id = %s", (self.current_user['id'],))
        sender_balance = self.cursor.fetchone()['balance']

        if amount > sender_balance:
            print("Insufficient funds.")
            return

        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver['balance'] + amount

        # Perform the transfer: update balances
        self.cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (new_sender_balance, self.current_user['id']))
        self.cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (new_receiver_balance, receiver['id']))

        # Log transactions for both users
        self.cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, related_user_id, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.current_user['id'], 'transfer_sent', amount, receiver['id'], f"Transferred to {receiver_email}"))

        self.cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, related_user_id, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (receiver['id'], 'transfer_received', amount, self.current_user['id'], f"Received from {self.current_user['email']}"))

        self.conn.commit()

        self.current_user['balance'] = new_sender_balance
        print(f"₹{amount} transferred successfully to {receiver_email}.")

# check your balance

    def check_balance(self):
        if not self.current_user:
            print("Please log in first.")
            return

        self.cursor.execute("SELECT balance FROM users WHERE id = %s", (self.current_user['id'],))
        balance = self.cursor.fetchone()['balance']
        print(f"Hello {self.current_user['name']}, your balance is ₹{balance}")

# see your transaction history

    def transaction_history(self):
        if not self.current_user:
            print("Please log in first.")
            return

        self.cursor.execute("""
            SELECT type, amount, description, created_at 
            FROM transactions 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (self.current_user['id'],))

        transactions = self.cursor.fetchall()

        print("===== Transaction History: =====")
        for txn in transactions:
            print(f"{txn['created_at']} | {txn['type']} | ₹{txn['amount']} | {txn['description']}")

    

bank = Account()

# Main loop

while True:
    if not bank.current_user:
        # Not logged in: Show Main Menu2 v
        print("\nMain Menu")
        print("===== Welcome to DCKAP Bank =====")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            bank.login()
        elif choice == "2":
            bank.register()
        elif choice == "3":
            print("Thank you for visiting DCKAP Bank.")
            break
        else:
            print("Invalid choice. Please try again.")

    else:
        # Logged in: Show Banking Options
        print(f"\nWelcome {bank.current_user['name']} to DCKAP Bank")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            bank.check_balance()
        elif choice == "2":
            bank.deposit()
        elif choice == "3":
            bank.withdraw()
        elif choice == "4":
            bank.transfer()
        elif choice == "5":
            bank.transaction_history()
        elif choice == "6":
            print(f"Goodbye {bank.current_user['name']}! Logging out...")
            bank.current_user = None
        else:
            print("Invalid choice. Please try again.")


