# Parent class for all children
class AccountHolderDetails:
    # Initialises with the core user details
    def __init__(self, name, address, age):
        # All personal information is hidden
        self.__name = name
        self.__address = address
        self.__age = age

    # User can only view the data with a Getter without the ability to edit
    @property
    def age(self):
        return self.__age

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address