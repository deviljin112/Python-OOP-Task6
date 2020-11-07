import json
import hashlib
import os
import binascii
from account_details import AccountHolderDetails


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