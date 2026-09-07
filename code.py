

import datetime


class BankAccount:
    def __init__(self, owner, account_number, pin, balance=0):
        self.owner = owner
        self.__account_number = account_number  # private
        self.__pin = pin                         # private
        self.__balance = balance                 # private
        self.__transactions = []                 # private history

    # PIN verification
    def verify_pin(self, pin):
        return self.__pin == pin

    # Getters
    def get_balance(self):
        return self.__balance

    def get_account_number(self):
        return self.__account_number

    def get_transactions(self):
        return self.__transactions

    # Deposit
    def deposit(self,amount):
        
        if not isinstance(amount,int):
            print("Amount must be integer(number)")

        elif amount <=0:
            print("insert amount greater than 0:")
            
        else:
            self.__balance+=amount
            print(f"Amount Deposited Successfully now your current balance is {self.__balance} ")
        return True

    # Withdraw
    def withdraw(self, amount):
        if amount <= 0:
            print(" Invalid amount! Please enter a positive value.")
            return False
        if amount > self.__balance:
            print(f"\n Insufficient balance!")
            print(f"   Available Balance: ₹{self.__balance}")
            return False
        self.__balance -= amount
        self.__log_transaction("Withdrawal", amount)
        print(f"\n ₹{amount} withdrawn successfully!")
        print(f"   Remaining Balance: ₹{self.__balance}")
        return True

    # Change PIN
    def change_pin(self, old_pin, new_pin):
        if not self.verify_pin(old_pin):
            print(" Incorrect current PIN!")
            return False
        if len(str(new_pin)) != 4:
            print(" PIN must be exactly 4 digits!")
            return False
        self.__pin = new_pin
        print(" PIN changed successfully!")
        return True

    # Private log method
    def __log_transaction(self, t_type, amount):
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.__transactions.append({
            "type": t_type,
            "amount": amount,
            "balance": self.__balance,
            "time": timestamp
        })

    def __str__(self):
        return f"Account Holder: {self.owner} | Account No: {self.__account_number}"


# ── SavingsAccount (Inheritance) ──
class SavingsAccount(BankAccount):
    INTEREST_RATE = 0.04  # 4% annual interest

    def __init__(self, owner, account_number, pin, balance=0):
        super().__init__(owner, account_number, pin, balance)
        self.account_type = "Savings Account"

    def add_interest(self):
        interest = self.get_balance() * self.INTEREST_RATE
        self.deposit(interest)
        print(f"   (Interest @ {self.INTEREST_RATE * 100}% added)")


# ── CurrentAccount  ──
class CurrentAccount(BankAccount):
    OVERDRAFT_LIMIT = 5000  # can go into overdraft up to ₹5000

    def __init__(self, owner, account_number, pin, balance=0):
        super().__init__(owner, account_number, pin, balance)
        self.account_type = "Current Account"

    def withdraw(self, amount):
        if amount <= 0:
            print(" Invalid amount!")
            return False
        if amount > self.get_balance() + self.OVERDRAFT_LIMIT:
            print(f" Exceeds overdraft limit of ₹{self.OVERDRAFT_LIMIT}!")
            return False
        # Call parent withdraw logic
        return super().withdraw(amount)


# ── ATM Machine Class ──
class ATM:
    def __init__(self):
        self.__accounts = {}  # stores all accounts
        self.__current_account = None
        self.__setup_demo_accounts()

    def __setup_demo_accounts(self):
        """Pre-load some demo accounts"""
        acc1 = SavingsAccount("Sanyam", "ACC001", 1234, 5000)
        acc2 = CurrentAccount("Rahul", "ACC002", 5678, 10000)
        self.__accounts["ACC001"] = acc1
        self.__accounts["ACC002"] = acc2

    def __display_header(self):
        print("\n" + "="*45)
        print("          WELCOME TO PY-BANK ATM  ")
        print("="*45)

    def __login(self):
        print("\n── LOGIN ──")
        acc_no = input("Enter Account Number: ").strip().upper()

        if acc_no not in self.__accounts:
            print(" Account not found!")
            return False

        pin = input("Enter PIN: ").strip()
        if not pin.isdigit():
            print(" PIN must be numeric!")
            return False

        account = self.__accounts[acc_no]
        if not account.verify_pin(int(pin)):
            print(" Incorrect PIN!")
            return False

        self.__current_account = account
        print(f"\n Login successful! Welcome, {account.owner} 👋")
        return True

    def __show_menu(self):
        acc = self.__current_account
        print(f"\n── MENU ({acc.account_type}) ──")
        print("  1. Check Balance")
        print("  2. Deposit")
        print("  3. Withdraw")
        print("  4. Transaction History")
        print("  5. Change PIN")
        if isinstance(acc, SavingsAccount):
            print("  6. Add Interest")
        print("  0. Logout")
        print("-"*30)

    def __check_balance(self):
        acc = self.__current_account
        print(f"\n Account Balance")
        print(f"   Holder : {acc.owner}")
        print(f"   Acc No : {acc.get_account_number()}")
        print(f"   Balance: ₹{acc.get_balance()}")

    def __deposit(self):
        print("\n── DEPOSIT ──")
        try:
            amount = float(input("Enter amount to deposit: ₹"))
            self.__current_account.deposit(amount)
        except ValueError:
            print(" Invalid input! Enter a numeric value.")

    def __withdraw(self):
        print("\n── WITHDRAW ──")
        try:
            amount = float(input("Enter amount to withdraw: ₹"))
            self.__current_account.withdraw(amount)
        except ValueError:
            print(" Invalid input! Enter a numeric value.")

    def __show_history(self):
        transactions = self.__current_account.get_transactions()
        print("\n── TRANSACTION HISTORY ──")
        if not transactions:
            print("   No transactions yet.")
            return
        print(f"  {'#':<4} {'Type':<12} {'Amount':>10} {'Balance':>10}  {'Time'}")
        print("  " + "-"*60)
        for i, t in enumerate(transactions, 1):
            print(f"  {i:<4} {t['type']:<12} ₹{t['amount']:>8.2f} ₹{t['balance']:>8.2f}  {t['time']}")

    def __change_pin(self):
        print("\n── CHANGE PIN ──")
        try:
            old_pin = int(input("Enter current PIN: "))
            new_pin = int(input("Enter new 4-digit PIN: "))
            self.__current_account.change_pin(old_pin, new_pin)
        except ValueError:
            print(" PIN must be numeric!")

    def __logout(self):
        print(f"\n Thank you, {self.__current_account.owner}! Have a great day!")
        self.__current_account = None

    def run(self):
        self.__display_header()
        print("\n📌 Demo Accounts:")
        print("   ACC001 | PIN: 1234 | Savings Account")
        print("   ACC002 | PIN: 5678 | Current Account")

        while True:
            if self.__current_account is None:
                print("\n── MAIN MENU ──")
                print("  1. Login")
                print("  0. Exit")
                choice = input("Choose: ").strip()

                if choice == "1":
                    self.__login()
                elif choice == "0":
                    print("\n Thank you for using PY-BANK ATM. Goodbye!\n")
                    break
                else:
                    print(" Invalid choice!")
            else:
                self.__show_menu()
                choice = input("Choose: ").strip()

                if choice == "1":
                    self.__check_balance()
                elif choice == "2":
                    self.__deposit()
                elif choice == "3":
                    self.__withdraw()
                elif choice == "4":
                    self.__show_history()
                elif choice == "5":
                    self.__change_pin()
                elif choice == "6" and isinstance(self.__current_account, SavingsAccount):
                    self.__current_account.add_interest()
                elif choice == "0":
                    self.__logout()
                else:
                    print(" Invalid choice!")


# ── Run the ATM ──
if __name__ == "__main__":
    atm = ATM()
    atm.run()