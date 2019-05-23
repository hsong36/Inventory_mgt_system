# Haena Song, CIS 345, TTH 10:30, Final_Project


# *********************************PRODUCT***********************************************************
class Product:
    """Product class defines common information for all products"""
    def __init__(self, product_id="", description="", qty=0, price=0.00):
        self.pid = product_id
        self.desc = description
        self.qty = qty
        self.price = price

    @property
    def prod_id(self):
        return self.__pid

    @prod_id.setter
    def id(self, product_id):
        self.pid = product_id

    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, description):
        self.__desc = description

    @property
    def qty(self):
        return self.__qty

    @qty.setter
    def qty(self, quantity):
        self.__qty = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, product_price):
        self.__price = product_price

    def __str__(self):
        """Override the string representation of a student"""
        # Use the properties or you are not executing the formatting
        return f'{self.pid} - {self.desc}, {self.qty}, ${self.price}'


# ******************************Attachment********************************************
class Attachment(Product):
    attachments = []
    """Attachment inherits from Product to get productID"""
    def __init__(self, material='', prod_id='', desc='', qty=0, price=0.00):
        """Initialize a GradStudent with first name and thesis"""
        super().__init__(prod_id, desc, qty, price)
        self.material = material

    def __str__(self):
        """Override the string representation of a product"""
        product_info = super().__str__()
        return f'{product_info}, {self.material}'


# *************************************CUSTOMER******************************************
class Customer:
    """Customer Class"""
    def __init__(self, account_number='', name='', balance=0.00, pin=''):
        self.account = account_number
        self.name = name
        self.pin = pin
        self.balance = balance

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, acc_number):
        self.__account = acc_number

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, customer_name):
        self.__name = customer_name

    @property
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, pin_number):
        self.__pin = pin_number

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_balance):
        self.__balance = new_balance

    def __str__(self):
        """Override the string representation of a student"""
        # Use the properties or you are not executing the formatting
        return f'{self.account} - {self.name}, ${self.balance}'
