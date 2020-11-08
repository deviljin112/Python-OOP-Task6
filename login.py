from account_management import MyAccount


# See README for full breakdown #


# New class extends "MyAccount"
class Login(MyAccount):
    # Class initialised with only 2 variables, the login and password
    def __init__(self, account_number, password):
        # First variable checks whether the login and password is correct
        # Return value is a dictionary
        self.user_data = self.check_login(account_number, password)
        # If the data is correct then inheritance occurs
        super().__init__(
            account_number,
            self.user_data["Balance"],
            self.user_data["Name"],
            self.user_data["Address"],
            self.user_data["Age"],
        )

    # Main function for checking login and password
    def check_login(self, account_number, password):
        # Gets all the current passwords
        data = self.get_data("passwords.json")
        # Checks if the account number exists
        if account_number in data.keys():
            # Stores the actual account's password in the variable
            stored_pass = data[account_number]
            # Calls a function that performs the password check
            matches = self.checkhash(stored_pass, password)

            # If they do match, then allow acces
            if matches:
                # Returns only the account specific data as a dictionary
                return self.get_data("account_details.json")[account_number]
            else:
                # Since we cannot `break` from class generation instead we need to raise a controlled error
                raise Exception()
        else:
            raise Exception()