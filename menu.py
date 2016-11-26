'''Provides functions that display the state of the application.'''
import os
import system

from interactions import *

_system = system.current()

TITLE = 'Heidelberg Student Bank'


def _clear():
    _system.clear()


def _decoration(text):
    return '*' * len(text)


def _header(text):
    _clear()
    print(_decoration(text))
    print(text)
    print(_decoration(text))


def _pause():
    _system.pause()


def branding():
    _clear()
    _header(TITLE)


def balance(balance):
    _header('Balance')
    print('Your account Balance is: ')
    print()
    print(balance)
    _pause()


def choose_action():
    menu_items = '''
(D) Deposit   (B) Balance
(W) Withdraw  (R) Report

(Q) Quit
'''
    return select(menu_items, choices='dbwrq')


def account_number():
    return prompt('Account Number: ')


def deposit():
    _header('Deposit')
    return amount('Amount to deposit: ')


def goodbye():
    print('Thank you for using %s services' % TITLE)


def report(history):
    _header('Report')
    print('Listing past transactions')
    print()
    print(history)
    _pause()


def invalid_account():
    print('Account Does Not Exist.')


def login(validate_pin):
    return pin(
        'PIN (Entry will be hidden): ',
        'Invalid Pin. Please try again.',
        validate_pin
    )


def login_failed():
    print('You failed to authenticate. ')


def welcome(name):
    print('Logged in as %s' % name)


def withdraw():
    _header('Withdraw')
    return amount('Amount to withdraw: ')
