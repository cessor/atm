'''Provides functions that receive and validate user input'''
from decimal import Decimal
import getpass
import re

_PROMPT_INDICATOR = '> '
_FOUR_DIGITS = re.compile(r'^\d{4}$')


def weasel(test, gen):
    text = ''
    while test(text):
        text = gen()
    return text


def _ask_for_input(message):
    print(message)
    return input(_PROMPT_INDICATOR)


def _prevent_empty_response(response_function):
    '''Asks for input as long as the input is empty'''
    return weasel(
        lambda text: not text,
        lambda: response_function().strip()
    )


def prompt(message):
    '''Asks the user for input'''
    return _prevent_empty_response(
        lambda: _ask_for_input(message)
    )


def secret(message):
    '''Asks the user for input and covers their entries'''
    print(message)
    return getpass.getpass(_PROMPT_INDICATOR)


def select(message, choices):
    '''Asks the user for input within an allowed domain of choices'''
    return weasel(
        lambda text: text not in list(choices),
        lambda: prompt(message).lower()
    )


def pin(message, try_again_message, validate):
    '''Ask for four digits, concealing their entry'''
    pin = ''
    # _ is idiomatic for "I don't care about this value"
    for _ in range(3):
        pin = secret(message)
        if _FOUR_DIGITS.match(pin) and validate(pin):
            return True
        print(try_again_message)
    return False


class DecimalFrom(object):
    '''Parses a positive decimal number from input text'''
    def __init__(self, text):
        self.text = text

    def _decimal_separator(self):
        '''Both . and , are recognized as comma values.'''
        self.text = self.text.replace(',', '.')

    def _enforce_positive(self):
        # Accept positive decimal numbers by removing sign
        self.text = self.text.replace('-', '')

    def value(self):
        try:
            self._enforce_positive()
            self._decimal_separator()
            return Decimal(self.text)
        except:
            return Decimal(0)


def amount(message):
    '''Prompts user to input a positive amount decimal number'''
    return weasel(
        lambda value: not isinstance(value, Decimal),
        lambda: DecimalFrom(prompt(message)).value()
    )