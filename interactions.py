'''Provides functions that receive and validate user input'''

from decimal import Decimal
import getpass
import re

_PROMPT_INDICATOR = '> '
_FOUR_DIGITS = re.compile(r'^\d{4}$')


def _ask_until_valid(validate, ask):
    '''Prompts for input, until a validatingcondition is met'''
    text = ''
    while validate(text):
        text = ask()
    return text


def _input(message):
    print(message)
    return input(_PROMPT_INDICATOR).strip()


def _parse_decimal_from(text):
    '''Parses a positive decimal number from input text.
    Both . and , are recognized as comma values.'''
    try:
        text = text.replace(',', '.').replace('-', '')
        return Decimal(text)
    except:
        return Decimal(0)


def amount(message):
    '''Prompts the user to input a positive amount decimal number'''
    return _ask_until_valid(
        ask= lambda: _parse_decimal_from(_input(message)),
        validate= lambda value: not isinstance(value, Decimal),
    )


def prompt(message):
    '''Prompts the user to input some text'''
    return _ask_until_valid(
        ask= lambda: _input(message),
        validate= lambda text: not text
    )


def select(message, choices):
    '''Prompts the user to select from a domain of choices'''
    return _ask_until_valid(
        ask= lambda: _input(message).lower(),
        validate= lambda text: text not in list(choices),
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


def secret(message):
    '''Asks the user for input and covers their entries'''
    print(message)
    return getpass.getpass(_PROMPT_INDICATOR)
