# Bank

## Table of Contents

- [Bank](#bank)
  - [Table of Contents](#table-of-contents)
  - [Task](#task)
  - [Functionality](#functionality)
  - [Sample Account](#sample-account)
  - [Explanation](#explanation)
  - [Code explanation](#code-explanation)
    - [Persistent data](#persistent-data)
    - [Password Hashing](#password-hashing)
    - [Login and Registration](#login-and-registration)
      - [Register](#register)
      - [Login](#login)
    - [Main Menu](#main-menu)
  - [To Do](#to-do)

## Task

- Create an AccountHolderDetails class with attributes name, address, age
- Inherit Account holder class into MyAccount
- Create a class called MyAccount which represents a bank account, having as attributes: accountNumber (numeric type), balance.
- Create a constructor () with parameters: accountNumber, balance.
- Create a Deposit() method which manages the deposit actions.
- Create a Withdrawal() method which manages withdrawals actions.
- Create an bankFees() method to apply the bank fees with a percentage of 5% of the balance account.
- Create a display() method to display account details.
- Create manageAccount class and import everything from BankAccount class
- Call all methods in manageAccount class that have are available from parent class
- Create a display() method to display account details.

## Functionality

Fully functioning banking system:

- Registration
- Login
- Persistent data
- Deposit
- Withdraw
- User Details
- Hashing passwords using SHA512 for maximum security
- Data saved as JSON can be easily modified for CSV or SQL
- Menu system (for user options)
- Works on both Windows and Unix-based

## Sample Account

To test out the code, feel free to use the sample account already created, or register your own!

```md
account number: 540292
password: sample
```

## Explanation

Persistent data is achieved through the use of JSON files. Although these are easily accesible, and can view all the user details, it is used for proof-of-concept. This should be revised with the use of SQL db for security.
</br>
Hashing. Hashing uses the SHA256 algorithm. This algorithm produces irreversible and unique hashes. This way even though the data is stored inside of a JSON file, the account password is theoretically uncrackable. This way users do not have to worry about security. Hashing is achieved with the use of Python's `hashlib` library, combined with `binascii` used to convert binary values into readble ascii and `os` module which allows us to get a very "random" value that is used for hashing, and therefore making the password even more secure.
</br>
Menu system allows the user to easily select the available options, see their details, change their password, deposit or withdraw money etc.
</br>
Multiplatform. With the help of `os` module we can easily implement functionality that works on all operating systems. As this program only runs in the terminal, the functionality was simply `cls` / `clear` for ease of formatting and clarity.

## Code explanation

### Persistent data

To achieve persistent data with JSON we need to work in a dictionary format. We can use the `with open(<file>, <permission>) as <variable>:` to access our .json file, with either read (`'r'`) or write (`'w'`) permissions. Since we want the data to be persistent we need both a get and save function. We also will have 2 seperate files one with the account data, one with password storage. Because we want to keep our code DRY we will use variables to state which file we want to access and save.
</br>

Get data function.

```python
def get_data(self, file):
    with open(file, "r") as details:
        data = json.load(details)
    return data
```

Save data function.

```python
def constructor(self, file, new_data):
    with open(file, "w") as details:
        json.dump(new_data, details, indent=4, sort_keys=True)
```

To ensure no data is lost. Although not the most efficient, we will be saving our data to json whenever a user alters their data. For example, when a user deposits any amount, we will first use `get_data` to create a `data` dictionary that will be passed to a `deposit()` function which will directly alter the amount of money the person has in their account. After their balance has been altered it will trigger the `constructor()` function to save the data instantly. `json.load(<variable>)` lets us load the json file into a python dictionary. While `json.dump(<new_data>, <variable>, <other_arguments>)` allows us to save the data with specific arguments. In our case, we want the JSON file to be readble, hence why I've used `indent` and `sort_keys` which is self-explanatory.

### Password Hashing

There are two functions involved with password hashing:

- One for encoding given password so it can be saved in a JSON file.
- Second for encoding the password given by the user with the same parameters and checking if the hashes match.

`hashpass(<password>)` is used as the encoder. It doesn't just hash the password with the algorithm, it actually takes multiple other steps in order to maximise the password security.
</br>
Firstly, we create some `salt`. Salt is an additional input, a random data used to increase the security. This salt is used for encrypting the password, and stored with the password as one. This allows for another function to use the same salt to encrypt the user provided password and check whether it matches the stored password. For our `salt` I've used `os.urandom` which generates a highly random set of numbers.
</br>
Secondly, we use `hexdigest()` and `encode("ascii")` to return a hexadecimal characters which are easier to understand, read and interpret compared to a binary result. These characters can only contain 0-9 and A-F.
</br>
Thirdly, we create the actual hashed password with `pbkdf2_hmac()`. Here, we provide the password encoded with `"utf-8"` which could contain ANY character.
</br>
Lastly, `binascii.hexlify()` this function allows us to convert the returned binary data from `pbkdf2_hmac()` and turn it into a digestable string which is combined with our salt and encoded into `'ascii'` as a return of the entire function. This returned string is stored in our JSON file, and allows us to easily access the `salt` later to use when we want to compare hashes in our second function. First 64 characters is our password hash and last 64 characters is our `salt` hash.

```python
def hashpass(self, password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    pwd_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
    pass_hash = binascii.hexlify(pwd_hash)
    return (salt + pass_hash).decode("ascii")
```

Similarly to the previous function we hash the provided password with the same method. Although this time we dont need to create a `salt` hash as that is already available from our stored password. We just need to hash it with the same parameters and `salt` and return either a `True` or `False` statement if the hashes match.

```python
def checkhash(self, stored_pwd, given_pwd):
    salt = stored_pwd[:64]
    stored_pwd = stored_pwd[64:]
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha512", given_pwd.encode("utf-8"), salt.encode("ascii"), 100000
    )
    pass_hash = binascii.hexlify(pwd_hash).decode("ascii")

    return pass_hash == stored_pwd
```

### Login and Registration

#### Register

In order to `Login` we need to have an existing account. To create an account we have a `Register` class. Our `CreateAccount` class extends the `MyAccount` class. `MyAccount` class stores all the account management functionality, such as balance, deposit, withdraw, hashing and opening json files. It's the main file that acts as the manager.
</br>
When we create a new account we first take in all the neccessary data as variables such as:

- Name
- Password
- Address
- Age
- Initial Deposit Amount

This information is first pushed into our `create_account()` method. This function is triggered before we inherit the data from its parent class in order to generate all the neccessary data for acces. We would be unable to create an instance of `MyAccount` without an existing `account_number`. We are still able to inherit the methods and use them however we are unable to use the class variables that have to be initialised with `super()`.

```python
class CreateAccount(MyAccount):
    def __init__(self, name, password, address, age, balance):
        self.new_account_num = self.create_account(
            name, password, address, age, balance
        )
        super().__init__(self.new_account_num, balance, name, address, age)
```

So, our `__init__` first creates a variable that will store our newly generated account number and triggers the method.
</br>
We create an infinite loop that generates a new random account number with `random.randint()`, that newly generated number is checked if it already exists, if not then we can use it for this account. Note: This is not the most optimal way of implementing random number generation as in larger scale problems it may take a while to generate a number that doesnt exist already.
</br>
Once we found a unique account number, we can add this new data to our variable `data` which is just the return from our `get_data()` function explored earlier. After adding new data, we call our `constructor()` and follow the same steps for our password. First getting `data` then creating a hash, and finally calling the `constructor()`. We then return just the `account_number` which is assigned to our `CreateAccount` class' variable called `self.new_account_number`.

```python
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

            pwd_data = self.get_data("passwords.json")
            pwd_data[account_number] = self.hashpass(password)
            self.constructor("passwords.json", pwd_data)
            return account_number
```

After getting a unique account number we can inherit all the data by filling in the variables inside the `super().__init__()` to inherit all the variables with filled in data.

#### Login

`Login` class has similar approach to `Registration`. We inherit the `MyAccount` Class, and create a variable that will store all the `user_data`. This user data is pulled from our JSON file, opposed to adding it to JSON in the case of `Register`. In order to trigger the `get_data()` function, we first need to check if the login and password is correct.
</br>
Because the `account_data.json` and `passwords.json` uses the same keys, we dont need to access both files in order to know whether the account exists. We also dont need to loop through all the data as python has a simple `in` operator that checks if an instance of our object is present in the dataset. It doesnt return anything other than a `True` or `False` statement. But that is all we need since we will be accesing the table with `account_number` as the key.
</br>
We start with `get_data()` function to pull all the data from Json into a dictionary. Followed by an `if` statement to check all the `keys()` in our data. We then take the stored password as `stored_pass` variable, which we will need in our `checkhash()` function. Since our `checkhash()` returns a boolean, we can store it in a variable that will then be used to do our next steps. We also trigger the `checkhash()` with `stored_pass` and provided by user `password` as arguments. If the passwords match, the function will return all the data that matches the provided `account_number` from the `account_details.json`. Because we know that the return of `get_data()` function is going to be a dictionary we can explicitly return only the data with the key of our `account_number`.

```python
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
```

Because this method is initialised in the `__init__` we cannot use `return False` if the details do not match our records as it will still proceed to call the `super().__init__()` function which will only result in a big error. Instead we can use the `raise Exception()` which will automatically stop the program at that point and it will not continue. We can control where the program stops and use `Try: Catch:` in order to continue the program running rather then stop at the error. This is called "Error Handling" and allows us to control our environment and program from stoping execution.
</br>

`check_login()` function:

```python
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
```

`Try: Catch:` error handling:

```python
try:
    user_login = Login(username, password)
except:
    print("Incorrect details provided!\nPlease try again")
```

### Main Menu

The main menu has multiple options that you would expect from a bank interface. Seeing your balance, depositing money or withdrawing money. The `main_menu()` function takes an argument of `user_object` this object is either going to be the `Login` class or the `CreateAccount` class. Since both classes extend `MyAccount` class, they both inherit all the functionality. The main difference is how they inherit the data. Both classes as explored in the previous chapter, first create a variable that calls a function which in turn returns the neccessary information for inheritance to occur.
</br>
Since both classes are theoretically the same, the methods and variables can be called the same way. Ensuring that our data is uniform and the code dynamic. Through this inheritance we have a tree diagram where `MyAccount` is the key class with majority of the logic and variables that control the flow of data and actions. While the `Login` and `CreateAccount` are two seperate branches that based on different conditions, if they fulfilled they clone an instance of `MyAccount` with all the correct data filled.

## To Do

- [ ] Add transfering money between accounts
- [ ] Change personal details
- [ ] Add email address and phone number as required
- [ ] More checks on what data is used for account creation
- [ ] Bug fix negative numbers as inputs
