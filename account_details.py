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