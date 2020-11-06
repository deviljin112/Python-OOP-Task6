import json
import random


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
        return self.__balance

    @balance.setter
    def balance(self, amount):
        self.__balance += amount

    def deposit(self, amount):
        data = self.get_data()
        data[self.account_number]["Balance"] += amount
        self.constructor(data)

    def withdraw(self, amount):
        amount = amount * -1
        data = self.get_data()
        data[self.account_number]["Balance"] += amount
        self.constructor(data)

    def bank_fees(self):
        data = self.get_data()
        fee = data[self.account_number]["Balance"] * 0.05
        data[self.account_number]["Balance"] -= fee
        self.constructor(data)

    def display(self):
        data = self.get_data()
        my_account = data[self.account_number]

        for k, v in my_account:
            print(f"{k} : {v}")

    def get_data(self):
        with open("account_details.json", "r") as details:
            data = json.load(details)
        return data

    def constructor(self, new_data):
        with open("account_details.json", "w") as details:
            json.dump(new_data, details, indent=4, sort_keys=True)


class ManageAccount(MyAccount):
    def __init__(self, name, address, age, balance):
        self.new_account_num = self.create_account(name, address, age, balance)
        super().__init__(self.new_account_num, balance, name, address, age)

    def create_account(self, name, address, age, balance):
        available = False
        while not available:
            account_number = random.randint(111111, 999999)
            data = self.get_data()

            if account_number not in data.keys():
                available = True
                data[account_number] = {
                    "Name": name,
                    "Address": address,
                    "Age": age,
                    "Balance": balance,
                }

                self.constructor(data)
                print(
                    f"Your new account number is: {account_number}.\nUse it to login!"
                )
                return account_number


class Login(MyAccount):
    def __init__(self, account_number):
        self.login_number = account_number
        self.user_data = self.check_login(self.login_number)
        super().__init__(
            self.login_number,
            self.user_data["Balance"],
            self.user_data["Name"],
            self.user_data["Address"],
            self.user_data["Age"],
        )

    def check_login(self, account_number):
        data = self.get_data()
        if account_number in data.keys():
            return data[account_number]
        else:
            raise Exception("Sorry, Your Account was Not Found!")


# To create a new account we use the following class and syntax
test = ManageAccount("Hubert", "Random Road", 23, 100)
print(test.balance)

number = test.account_number

# To login to our account we just use
test2 = Login(271264)
print(test2.balance)
