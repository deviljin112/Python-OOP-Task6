import json
import random
import hashlib
import os
import binascii
import time


class AccountHolderDetails:
    def __init__(self, name, address, age):
        self.__name = name
        self.__address = address
        self.__age = age

    @property
    def age(self):
        return self.__age

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address


class MyAccount(AccountHolderDetails):
    def __init__(self, account_number, balance, name, address, age):
        super().__init__(name, address, age)
        self.__account_number = account_number
        self.__balance = balance

    @property
    def account_number(self):
        return self.__account_number

    @property
    def balance(self):
        return float("{:.2f}".format(self.__balance))

    @balance.setter
    def balance(self, amount):
        self.__balance += amount

    def balance_manager(self, action, amount):
        data = self.get_data("account_details.json")

        if action == "deposit":
            data = self.deposit(data, amount)
        elif action == "withdraw":
            data = self.withdraw(data, amount)

        self.constructor("account_details.json", data)

    def deposit(self, data, amount):
        data[self.account_number]["Balance"] += amount
        self.balance = amount
        return data

    def withdraw(self, data, amount):
        fee = self.bank_fees(amount)
        print(f"Fee: £{fee * -1}")
        amount = amount * -1
        data[self.account_number]["Balance"] += amount + fee
        self.balance = amount + fee

        return data

    def bank_fees(self, amount):
        fee = (amount * 0.05) * -1
        return fee

    def display(self):
        data = self.get_data("account_details.json")
        my_account = data[self.account_number]

        for k, v in my_account.items():
            print(f"{k} : {v}")

    def password(self, new_password):
        pwd = self.hashpass(new_password)
        data = self.get_data("passwords.json")
        data[self.account_number] = pwd
        self.constructor("passwords.json", data)

    def hashpass(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwd_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pass_hash = binascii.hexlify(pwd_hash)
        return (salt + pass_hash).decode("ascii")

    def checkhash(self, stored_pwd, given_pwd):
        salt = stored_pwd[:64]
        stored_pwd = stored_pwd[64:]
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha512", given_pwd.encode("utf-8"), salt.encode("ascii"), 100000
        )
        pass_hash = binascii.hexlify(pwd_hash).decode("ascii")

        return pass_hash == stored_pwd

    def get_data(self, file):
        with open(file, "r") as details:
            data = json.load(details)
        return data

    def constructor(self, file, new_data):
        with open(file, "w") as details:
            json.dump(new_data, details, indent=4, sort_keys=True)


class CreateAccount(MyAccount):
    def __init__(self, name, password, address, age, balance):
        self.new_account_num = self.create_account(
            name, password, address, age, balance
        )
        super().__init__(self.new_account_num, balance, name, address, age)

    def create_account(self, name, password, address, age, balance):
        available = False
        while not available:
            account_number = random.randint(111111, 999999)
            data = self.get_data("account_details.json")

            if account_number not in data.keys():
                available = True
                data[account_number] = {
                    "Name": name,
                    "Address": address,
                    "Age": age,
                    "Balance": balance,
                }

                self.constructor("account_details.json", data)

                # Password Data
                pwd_data = self.get_data("passwords.json")
                pwd_data[account_number] = self.hashpass(password)
                self.constructor("passwords.json", pwd_data)
                return account_number


class Login(MyAccount):
    def __init__(self, account_number, password):
        self.user_data = self.check_login(account_number, password)
        super().__init__(
            account_number,
            self.user_data["Balance"],
            self.user_data["Name"],
            self.user_data["Address"],
            self.user_data["Age"],
        )

    def check_login(self, account_number, password):
        data = self.get_data("passwords.json")
        if account_number in data.keys():
            stored_pass = data[account_number]
            matches = self.checkhash(stored_pass, password)

            if matches:
                return self.get_data("account_details.json")[account_number]
            else:
                raise Exception()
        else:
            raise Exception()


def main():
    print("Hello user!\nWhat would you like to do?\n'Login' or 'Register'")
    choice = input("=> ")

    if choice.lower() == "register":
        # To create a new account we use the following class and syntax
        register_acc = True
        while register_acc:
            user_name = input("Name: ")
            user_pass = input("Password: ")
            user_addr = input("Address: ")
            user_age = input("Age: ")
            user_balance = input("First Deposit Amount: ")

            if user_age.isdigit() and user_balance.isdigit():
                user_age, user_balance = int(user_age), float(user_balance)

                user_register = CreateAccount(
                    user_name, user_pass, user_addr, user_age, user_balance
                )
                print(
                    f"""
You have successful registed a new account!
Your account number is: {user_register.account_number}.
Use it to login in the future!
Please make note of it of it now.
"""
                )

                while True:
                    confirmation = input(
                        "Please confirm your account number before continuing.\n=> "
                    )

                    if (
                        confirmation.isdigit()
                        and int(confirmation) == user_register.account_number
                    ):
                        print("Account confirmed!\nRedirecting...")
                        time.sleep(5)
                        os.system("cls" if os.name == "nt" else "clear")
                        break
                    else:
                        print("Account number doesn't match.\nPlease try again!")

                main_menu(user_register)

                register_acc = False
            else:
                print("Invalid details.\nPlease try again!")

    elif choice.lower() == "login":
        # To login to our account we just use
        logging_in = True
        while logging_in:
            username = input("Account No: ")
            password = input("Password: ")

            try:
                user_login = Login(username, password)
            except:
                print("Incorrect details provided!\nPlease try again")
            else:
                print("Logging in Successful!\nRedirecting...")
                time.sleep(5)
                os.system("cls" if os.name == "nt" else "clear")
                main_menu(user_login)
                logging_in = False

    else:
        print("That is not a valid option!")


def main_menu(user_object):
    while True:
        print(
            f"""
Bank Menu:

Menu commands are highlighted with 'command'

    - Account Details:
        - 'Account Number'
        - 'Name'
        - 'Age'
        - 'Address'
        - 'Change Password'

    - Balance:
        - 'Balance'
        - 'Deposit'
        - 'Withdraw'

    - 'Display' all details

    - 'Logout'

Bank Fees: Each withdraw applies a fee of 5%

Please note we cannot show you your current password for security reasons."""
        )

        choice = input("=> ")

        if choice.lower() == "account number":
            print(f"Your account number is: {user_object.account_number}.")
        elif choice.lower() == "name":
            print(f"Your name is: {user_object.name}.")
        elif choice.lower() == "age":
            print(f"You are {user_object.age} years old.")
        elif choice.lower() == "address":
            print(f"Your address is: {user_object.address}.")
        elif choice.lower() == "change password":
            print("Please input the new password.")
            new_pwd = input("=> ")

            user_object.password(new_pwd)
            print("Password changed successfully!")
        elif choice.lower() == "balance":
            print(f"You have: £{user_object.balance}.")
        elif choice.lower() == "deposit" or choice.lower() == "withdraw":
            while True:
                print("Please input the amount.")
                amount = input("=> ")

                try:
                    amount = float(amount)
                except:
                    print("Please input a valid number!")
                else:
                    if (
                        amount + (user_object.bank_fees(amount) * -1)
                    ) <= user_object.balance:
                        user_object.balance_manager(choice.lower(), amount)
                        print(f"Successful {choice.lower()} of £{amount}")
                        break
                    else:
                        print("You don't have enough funds.")
                        break

        elif choice.lower() == "display":
            user_object.display()
        elif choice.lower() == "logout":
            user_object = None
            print("Thank you for using our bank.\nGoodbye!")
            break
        else:
            print("This is not a valid option!")

        time.sleep(5)
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("-=BANK=-")
    main()
