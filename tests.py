import datetime
from atm import Timestamp, History, remember


def test_timestamp():
    now = Timestamp()
    now.date = datetime.datetime(2016, 11, 23, 12, 27, 47, 186375)
    assert str(now) == "2016-11-23, 12:27:47"


def test_history():
    history = History()
    customer = Customer("Johannes", "Johannes", 1234, Decimal(1000), history)


def run_tests():
    '''
    I did not testdrive the app (i.e. I did not create tests first, as expected when you're following TDD principles). Instead, I tested only my expectations about the parts where I was uncertain. This is considered bad practice, by the way.

    Usually I would use a proper testrunner, such as "nose", but I can never remember how to import data into deeply nested tests, and since I have been working on this program on the train I can't look up how to do it, thus I quickly built my own testrunner.
    '''
    import tests
    for object_name in dir(tests):
        if object_name.startswith('test_'):
            test = getattr(tests, object_name)
            test()

if __name__ == '__main__':
    run_tests()