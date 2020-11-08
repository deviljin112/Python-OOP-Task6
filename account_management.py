# Module used for importing and exporing Python Dictionary into a JSON format
import json

# Module used for password hashing
import hashlib

# Module used for random number generation
import os

# Module used for translating binary code into 'ascii' format
import binascii
from account_details import AccountHolderDetails


# New class extends "AccountHolderDetails"
class MyAccount(AccountHolderDetails):
    # Initialises the class with all the variables
    def __init__(self, account_number, balance, name, address, age):
        # Starts with inheritance from the parent class
        super().__init__(name, address, age)
        # Asigns the variables into private variables
        self.__account_number = account_number
        self.__balance = balance

    # Each private variable uses a Getter to lock user acces to the variable
    @property
    def account_number(self):
        return self.__account_number

    @property
    def balance(self):
        return float("{:.2f}".format(self.__balance))

    # Balance uses a setter for manipulation of front end display
    # Even if the user was to change the variable he doesn't manipulate the back-end data
    @balance.setter
    def balance(self, amount):
        # Unlike regular Setter, when invoked the amount set is actually added to current balance instead
        # Example: `balance = 10` is actually translated into `balance = balance + 10`
        self.__balance += amount

    # To keep the code DRY this function acts as a interface for interacting with the balance variable
    def balance_manager(self, action, amount):
        # Function for getting all the current data
        data = self.get_data("account_details.json")

        # If for calling the specific method
        if action == "deposit":
            data = self.deposit(data, amount)
        elif action == "withdraw":
            data = self.withdraw(data, amount)

        # After data manipulation constructor is called to update the JSON file
        self.constructor("account_details.json", data)

    # Deposit simply adds the amount depositted to both the JSON data and Front-end variable
    def deposit(self, data, amount):
        data[self.account_number]["Balance"] += amount
        self.balance = amount
        # Returns the new data
        return data

    # Withdraw amount simply subtracts the amount withdrawn from both JSON data and Front-end variable
    def withdraw(self, data, amount):
        # Triggers the "on-withdraw fee" function
        fee = self.bank_fees(amount)
        # Prints the fee amount to the user
        print(f"Fee: £{fee * -1}")
        # Since we are withdrawing the number needs to be a negative
        amount = amount * -1
        data[self.account_number]["Balance"] += amount + fee
        self.balance = amount + fee
        # Returns the new data
        return data

    # "on-withdraw fee" takes in the withdraw amount and calculates 5%
    def bank_fees(self, amount):
        # Since it needs to be subtracted it has to be negative
        fee = (amount * 0.05) * -1
        # Returns a float
        return fee

    # Display shows all the data stored in the JSON file about an account
    def display(self):
        data = self.get_data("account_details.json")
        my_account = data[self.account_number]

        # For loop that iterates through all key-value pairs
        for k, v in my_account.items():
            print(f"{k} : {v}")

    # Password function acts similarly to a Setter new_password is a string given by the user
    def password(self, new_password):
        # First the password is hashed
        pwd = self.hashpass(new_password)
        # Then password data is called
        data = self.get_data("passwords.json")
        # Old password is replaced with the new hashed password
        data[self.account_number] = pwd
        # Finally constructor is called to update the JSON file
        self.constructor("passwords.json", data)

    # See README for full break down of Hashing a Password
    def hashpass(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwd_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pass_hash = binascii.hexlify(pwd_hash)
        return (salt + pass_hash).decode("ascii")

    # See README for full break down of comparing Hashed Passwords
    def checkhash(self, stored_pwd, given_pwd):
        salt = stored_pwd[:64]
        stored_pwd = stored_pwd[64:]
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha512", given_pwd.encode("utf-8"), salt.encode("ascii"), 100000
        )
        pass_hash = binascii.hexlify(pwd_hash).decode("ascii")

        return pass_hash == stored_pwd

    # Dynamic function for loading any JSON file as a data dictionary
    def get_data(self, file):
        with open(file, "r") as details:
            data = json.load(details)
        return data

    # Dynamic function for saving a python dictionary in a JSON file
    def constructor(self, file, new_data):
        with open(file, "w") as details:
            json.dump(new_data, details, indent=4, sort_keys=True)
