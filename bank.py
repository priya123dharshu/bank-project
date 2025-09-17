# created Bank class

class Bank:
    def __init__(self):
        self.users = []
        self.current_user = None

# user Register
    def register(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        email = input("Enter your email: ")

        for user in self.users:
            if user["email"] == email:
                print("A user with the same email already exists.")
                return

        user = {
            "name": name,
            "password": password,
            "email": email,
            "balance": 0,
            "history": []
        }
        self.users.append(user)
        print("Registration successful!")

# user Login

    def login(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        for user in self.users:
            if user["name"] == name and user["password"] == password:
                self.current_user = user
                print("Login successful!")
                return
        print("Invalid credentials.")

# inherite Bank to Account class

class Account(Bank):
    def __init__(self):
        super().__init__()

# deposit your amount

    def deposit(self):
        if not self.current_user:
            print("Please log in first.")
            return

        amount = int(input("Enter deposit amount: "))
        if amount > 0:
            self.current_user["balance"] += amount
            msg = f"₹{amount} deposited successfully."
            self.current_user["history"].append(msg)
            print(msg)
        else:
            print("amount must be positive...negative value not allowed")

# withdraw method

    def withdraw(self):
        if not self.current_user:
            print("Please log in first.")
            return

        amount = int(input("Enter withdrawal amount: "))
        if amount > self.current_user["balance"]:
            print("Insufficient funds.")
            return

        self.current_user["balance"] -= amount
        msg = f"₹{amount} withdrawn successfully."
        self.current_user["history"].append(msg)
        print(msg)

# transfer amount your friends or family

    def transfer(self):
        if not self.current_user:
            print("Please log in first.")
            return

        receiver_email = input("Enter receiver's email: ")
        amount = int(input("Enter transfer amount: "))

        if amount > self.current_user["balance"]:
            print("Insufficient funds.")
            return
        if amount < 0:
            print("Transfer amount must be positive.")
            return
        

        receiver = None
        for user in self.users:
            if user["email"] == receiver_email:
                if user["email"] == self.current_user["email"]:
                    print("You cannot transfer to yourself.")
                    return
            receiver = user
            break

        if receiver is None:
            print("Receiver not found.")
            return

        self.current_user["balance"] -= amount
        receiver["balance"] += amount

        self.current_user["history"].append(f"Transferred ₹{amount} to {receiver_email}")
        receiver["history"].append(f"Received ₹{amount} from {self.current_user['email']}")

        print("Transfer successful!")

# check your balance

    def check_balance(self):
        if not self.current_user:
            print("Please log in first.")
            return
        
        print("Hii" ,self.current_user["name"]," your balance is: ₹",self.current_user["balance"])

# see your transaction history

    def transaction_history(self):
        if not self.current_user:
            print("Please log in first.")
            return
        print("===== Transaction History: =====")

        for history in self.current_user["history"]:
            print(history)

    

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


