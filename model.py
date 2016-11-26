from decimal import Decimal
import datetime


class Accounts(object):
    '''Retrieves and saves customers'''
    def __init__(self, table):
        self.table = table

        self.accounts = {
            account.number: account for account in (
                Unauthenticated.parse(row)
                for row
                in table.rows()
            )
        }

    def find(self, number, failure):
        return self.accounts.get(number()) or failure()


class Account(object):
    def __init__(self, number, name, pin):
        self.name = name
        self.number = number
        self.pin = pin

    def authenticate(self, login_function, invalid_pin):
        # Authenticated customers don't need to login.
        # They already _are_ logged in
        return self


class Unauthenticated(Account):
    def __init__(self, *args):
        super().__init__(*args)

    def _validate_pin(self, entered_pin):
        return self.pin == entered_pin

    def authenticate(self, login, fail):
        if login(self._validate_pin):
            return Account(self.number, self.name, self.pin)
        fail()

    @classmethod
    def parse(self, string):
        return Unauthenticated(*tuple(CommaSeparatedRow.parse(string)))


class History(object):
    '''A history of events in the system. Persists the transactions
    for all customers into a table'''
    def __init__(self, table):
        self.table = table

        self.transactions = [
            Transaction.parse_record(row)
            for row
            in self.table.rows()
        ]

    def save(self):
        rows = (
            transaction.record()
            for transaction
            in self.transactions
        )
        self.table.save(rows)

    def _history_for_(self, customer):
        return (
            transaction
            for transaction
            in self.transactions
            if transaction.customer == customer
        )

    def balance_for(self, customer_number):
        transactions = list(self._history_for_(customer_number))
        balance = Decimal(sum(t.value for t in transactions))
        return Balance(balance).absolute()

    def report_for(self, customer_number):
        transactions = list(self._history_for_(
            customer_number
        ))

        if not transactions:
            return str(Rows(
                'No records available.',
                Line()
            ))

        n_records = '%s Records' % len(transactions)

        rows = Rows(
            Rows(*transactions),
            Line(),
            n_records,
            Line()
        )
        return str(rows)

    def remember_deposit(self, customer, amount):
        self.transactions.append(
            Deposit(customer, Date.now(), amount)
        )

    def remember_withdraw(self, customer, amount):
        self.transactions.append(
            Withdraw(customer, Date.now(), amount)
        )


class Transaction(object):
    COLUMN_WIDTH = 20

    def __init__(self, customer, created, amount):
        self.customer = customer
        self.created = created
        self.amount = amount

    @property
    def value(self):
        return self.amount

    @property
    def type_(self):
        return self.__class__.__name__.lower()

    @classmethod
    def parse_record(self, string):
        customer, date, amount, type_ = tuple(
            CommaSeparatedRow.parse(string)
        )
        date = Date.parse_iso(date)
        amount = Decimal(amount)
        if type_ == 'deposit':
            return Deposit(customer, date, amount)
        if type_ == 'withdraw':
            return Withdraw(customer, date, amount)

    def record(self):
        key = self.customer
        date = self.created.iso()
        amount = "%.4f" % self.amount
        type_ = self.type_
        return str(CommaSeparatedRow(
            key, date, amount, type_
        ))

    def __repr__(self):
        return str(self)

    def __str__(self):
        key = self.customer
        date = self.created.readable()
        amount = ('%.4f' % self.amount).rjust(self.COLUMN_WIDTH, ' ')
        type_ = self.type_
        return str(Row(
            key, date, amount, type_
        ))


class Withdraw(Transaction):
    @property
    def value(self):
        return self.amount * -1


class Deposit(Transaction):
    pass


class Date(object):
    def __init__(self, date):
        self.date = date

    @classmethod
    def now(self):
        return Date(datetime.datetime.now())

    def value(self):
        return self.date

    def readable(self):
        format_ = '%d. %b %Y, %H:%M:%S'
        # String Format Time
        return self.date.strftime(format_)

    def iso(self):
        return self.date.isoformat()

    @classmethod
    def parse_iso(self, string):
        format_ = '%Y-%m-%dT%H:%M:%S.%f'
        return Date(datetime.datetime.strptime(string, format_))


class Balance(object):
    '''The money owned by a customer, without a currency'''
    def __init__(self, value):
        self.value = value

    def absolute(self):
        if self.value < 0:
            return Debit(abs(self.value))
        return Credit(abs(self.value))

    def __str__(self):
        balance = "%.4f %s" % (self.value, self.__class__.__name__)
        return str(Rows(
                balance,
                Line()
        ))


class Credit(Balance):
    '''Buchführung: Haben'''
    pass


class Debit(Balance):
    '''Buchführung: Soll'''
    pass


class File(object):
    '''Saves as reads text'''
    def __init__(self, path):
        self.path = path

    def content(self):
        with open(self.path, 'r') as file_:
            return file_.read()

    def write(self, content):
        content = str(content)
        with open(self.path, 'w') as file_:
            return file_.write(content)


class Table(object):
    '''Interface to read and write rows into a file'''
    def __init__(self, file):
        self.file = file

    def rows(self):
        return Rows.parse(self.file.content())

    def save(self, rows):
        self.file.write(str(Rows(*rows)))


class Line(object):
    '''A horizontal line on the console'''
    def __str__(self):
        return ('-' * 80)


class Concatenation(object):
    '''Concatenates a set of objects with a separator.'''
    SEPARATOR = ''

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return self.SEPARATOR.join((str(arg) for arg in self.args))

    @classmethod
    def parse(self, string):
        '''Splits text elements by a separator and cleans them from
        whitespace '''
        for item in string.split(self.SEPARATOR):
            item = item.strip()
            if item:
                yield item


class Row(Concatenation):
    '''A text row that separates values with spaces'''
    SEPARATOR = ' '


class Rows(Concatenation):
    '''A collection of rows to be displayed in a table'''
    SEPARATOR = '\n'


class CommaSeparatedRow(Concatenation):
    '''A text row that separates values with commas'''
    SEPARATOR = ', '



