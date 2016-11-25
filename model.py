from decimal import Decimal
import datetime

class Customers(object):
    '''Retrieves and saves customers'''
    def __init__(self):
        self.customers = {
            'Johannes': UnauthenticatedCustomer(
                "Johannes" ,"Johannes", "1234", Balance(0.0), History())
        }

    def find(self, number, failure):
       return self.customers.get(number()) or failure()

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
        self.history.remember(amount, 'deposit')
        self.balance = self.balance.credit(amount)

    def withdraw(self, amount):
        self.history.remember(amount, 'withdraw')
        self.balance = self.balance.debit(amount)

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
    '''The money owned by a customer, without a currency'''
    def __init__(self, value):
        self.value = Decimal(value)

    def credit(self, amount):
        # To credit: Gutschreiben
        return Balance(self.value + amount).absolute()

    def debit(self, amount):
        # To debit: Belasten
        return Balance(self.value - amount).absolute()

    def absolute(self):
        if self.value < 0:
            return Debit(abs(self.value))
        return Credit(abs(self.value))

    def __str__(self):
        return "%.4f %s" % (self.value, self.__class__.__name__)


class Credit(Balance):
    pass


class Debit(Balance):
    pass


class History(object):
    '''A history of events in the system'''
    def __init__(self, records = []):
        self.records = records

    def remember(self, amount, label):
        self.records.append(Record(amount, label))


class Line(object):
    '''A horizontal line on the console'''
    def __str__(self):
        return ('-' * 80)


class Report(object):
    '''Displays a table of events'''
    def __init__(self, history):
        self.records = history.records

    def __str__(self):
        if not self.records:
            return str(Rows(
                'No records available.',
                Line()
            ))

        n_records = '%s Records' % len(self.records)

        rows = Rows(
            Rows(*self.records),
            Line(),
            n_records,
            Line()
        )

        return str(rows)


class Record(object):
    def __init__(self, amount, transaction_type):
        self.created = Timestamp()
        self.amount = amount
        self.type = transaction_type

    def __str__(self):
        return '%s %.4f \t%s' % (
            self.created, self.amount, self.type)


class Rows(object):
    '''A collection of rows to be displayed in a table'''
    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return '\n'.join([str(arg) for arg in self.args])


class Timestamp(object):
    '''Encapsulated Timestamps in an object oriented fashion'''
    def __init__(self):
        self.date = datetime.datetime.now()

    def __str__(self):
        format_ = '%Y-%m-%d, %H:%M:%S'
        # String Format Time
        return self.date.strftime(format_)
