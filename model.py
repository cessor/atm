'''This module contains all model classes, that define the domain. '''
from decimal import Decimal
from history import History, remember
from complaint import InvalidCustomer


class Customers(object):
    '''Retrieves ans saves customers'''
    def exists(self, number):
        return number == "Johannes"

    def __getitem__(self, number):
        if not self.exists(number):
            raise InvalidCustomer()
        return UnauthenticatedCustomer(
            number, number, "1234", Balance(0.0), History())

    def save(self, customer):
        pass


class Customer(object):
    def __init__(self, number, name, pin, balance, history):
        self.name = name
        self.number = number
        self.pin = pin
        self.balance = balance
        self.history = history

    def deposit(self, amount):
        self.history.remember_transaction(amount, 'deposit')
        self.balance.credit(amount)

    def withdraw(self, amount):
        self.history.remember_transaction(amount, 'withdraw')
        self.balance.debit(amount)

    def authenticate(self, login_function, invalid_pin):
        # Authenticated customers don't need to login.
        # They already _are_ logged in
        return self


class UnauthenticatedCustomer(Customer):
    def __init__(self, *args):
        super().__init__(*args)

    def _validate_pin(self, entered_pin):
        return self.pin == entered_pin

    def authenticate(self, login, fail):
        if login(self._validate_pin):
            return Customer(self.number, self.name, self.pin, self.balance, self.history)
        fail()


class Balance(object):
    CREDIT = 'C'
    DEBIT = 'D'

    def __init__(self, value):
        self.value = Decimal(value)

    def credit(self, amount):
        # To credit: Gutschreiben
        self.value += amount

    def debit(self, amount):
        # To debit: Belasten
        self.value -= amount

    def _avoid_negative_value(self):
        return self.value * -1 if self.value < 0 else self.value

    def _type(self):
        return self.DEBIT if self.value < 0 else self.CREDIT

    def __str__(self):
        value = self._avoid_negative_value()
        return "%.4f %s" % (value, self._type())
