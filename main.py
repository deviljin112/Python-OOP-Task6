import time
import os
from create_account import CreateAccount
from login import Login


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
