from account_management import MyAccount


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