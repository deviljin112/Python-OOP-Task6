import random
from account_management import MyAccount


class CreateAccount(MyAccount):
    def __init__(self, name, password, address, age, balance):
        self.new_account_num = self.create_account(
            name, password, address, age, balance
        )
        super().__init__(self.new_account_num, balance, name, address, age)

    def create_account(self, name, password, address, age, balance):
        available = False
        while not available:
            account_number = str(random.randint(111111, 999999))
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