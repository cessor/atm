from interactions import prompt, secret, select, pin, amount
import os


class Menu(object):
    # The methods in this class are sorted alphabetically
    TITLE = 'Heidelberg Student Bank'

    def __init__(self, system):
        self.system = system

    def _clear(self):
        self.system.clear()

    def _header(self, text):
        self._clear()
        print('*' * len(text))
        print(text)
        print('*' * len(text))

    def _line(self):
        print('-' * 80)

    def _pause(self):
        self.system.pause()

    def balance(self, balance):
        self._line()
        self._header('Balance')
        print('Your account Balance is: ')
        print()
        print(balance)
        self._line()
        print("Note: (C) Credit / (D) Debit")
        self._line()
        self._pause()

    def branding(self):
        self._clear()
        self._header(self.TITLE)

    def choose_action(self):
        menu_items = """
(D) Deposit   (B) Balance
(W) Withdraw  (R) Report

(Q) Quit
"""
        return select(menu_items, choices="dbwrq")

    def customer_number(self):
        return prompt("Customer Number: ")

    def deposit(self):
        self._header("DEPOSIT")
        return amount("Amount to deposit: ")

    def goodbye(self):
        print('Thank you for using %s services' % self.TITLE)

    def report(self, print_history, print_footer):
        self._header('Report')
        print("Listing past transactions")
        print()
        print_history()
        self._line()
        print_footer()
        self._line()
        print("Note: (D) Deposit / (W) Withdraw")
        self._line()
        self._pause()

    def invalid_customer(self):
        print("User Does Not Exist")

    def login(self, validate_pin):
        return pin(
            "PIN (Entry will be hidden): ",
            "Invalid Pin. Please try again.",
            validate_pin
        )

    def login_failed(self):
        print("You failed to authenticate. Aborting.")

    def welcome(self, name):
        print("Logged in as %s" % name)

    def withdraw(self):
        self._header("WITHDRAW")
        return amount("Amount to withdraw: ")