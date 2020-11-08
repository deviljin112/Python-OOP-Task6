# Module random is used for creating random integer values
import random
from account_management import MyAccount


# See README for full breakdown #


# Creates a new class that extends "MyAccount"
class CreateAccount(MyAccount):
    # Initialises the class
    def __init__(self, name, password, address, age, balance):
        # First variable calls the create_account() function which returns a string of account_number
        self.new_account_num = self.create_account(
            name, password, address, age, balance
        )
        # After creating a new account the initalisation then inherits all the data from other classes
        # With the new account number as a variable and the rest of the variables for ease of access
        super().__init__(self.new_account_num, balance, name, address, age)

    # Create account function, used to generate new account numbers and create JSON entries
    def create_account(self, name, password, address, age, balance):
        available = False
        # Loop used to attempt to generate a unique account number
        while not available:
            # Random module used for creating a new account number
            account_number = str(random.randint(111111, 999999))
            # get_data() is used to pull all currently existing data
            data = self.get_data("account_details.json")

            if account_number not in data.keys():
                available = True
                data[account_number] = {
                    "Name": name,
                    "Address": address,
                    "Age": age,
                    "Balance": balance,
                }

                # Adds new data to JSON file
                self.constructor("account_details.json", data)

                # Password Hash Generation
                pwd_data = self.get_data("passwords.json")
                pwd_data[account_number] = self.hashpass(password)
                self.constructor("passwords.json", pwd_data)
                # Returns the unique account number as a string
                return account_number