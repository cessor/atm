import datetime

def remember(method):
    '''This is bad.'''
    import functools
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        self_, amount = args
        self_.history_.remember_transaction(amount, method.__name__)
        return method(*args, **kwargs)
    return wrapper


class History(object):
    def __init__(self):
        self.records = []

    def remember_transaction(self, amount, transaction_type):
        self.records.append(Record(amount, transaction_type))

    def body(self):
        if not self.records:
            print("No records available.")
            return

        for record in self.records:
            record.print()

    def footer(self):
        print("%s Records" % len(self.records))


class Record(object):
    DEPOSIT = 'D'
    WITHDRAW = 'W'

    def __init__(self, amount, transaction_type):
        self.created = Timestamp()
        self.amount = amount
        self.type = self._abbreviate(transaction_type)

    def _abbreviate(self, type_):
        if type_ == 'deposit':
            return self.DEPOSIT
        if type_ == 'withdraw':
            return self.WITHDRAW

    def print(self):
        print("%s %.4f \t%s" % (self.created, self.amount, self.type))


class Timestamp(object):
    '''Encapsulated Timestamps in an object oriented fashion'''
    def __init__(self):
        self.date = datetime.datetime.now()

    def __str__(self):
        format_ = '%Y-%m-%d, %H:%M:%S'
        # String Format Time
        return self.date.strftime(format_)