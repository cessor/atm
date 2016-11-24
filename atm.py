from complaint import Exit, LoginFailed, InvalidCustomer
from menu import Menu
from model import Customers
import system


class ATM(object):
    '''Controls a users's interactions with the ATM.'''

    def __init__(self, menu, customers):
        self.customers = customers
        self.menu = menu
        self.customer = None

    def start(self):
        running = True
        while running:
            running = self._session()
        self.menu.goodbye()

    def _session(self):
        self.menu.branding()

        try:
            self._init_customer()
            self._handle_user_action()

        except InvalidCustomer:
            self.menu.invalid_customer()
            return False

        except LoginFailed:
            self.menu.login_failed()
            return False

        except Exit:
            return False

        except KeyboardInterrupt:
            return False

        #except:
        #    print("An unknown error occured. Aborting")
        #    return False

        finally:
            self.customers.save(self.customer)

        return True # Keep running

    def _init_customer(self):
        if not self.customer:
            number = self.menu.customer_number()
            self.customer = self.customers[number]
            self.menu.welcome(self.customer.name)

    def _handle_user_action(self):
        action = self.menu.choose_action().lower()

        if action == 'q':
            raise Exit()

        # Any action other than exit requires a login first
        self.customer = self.customer.authenticate(
            self.menu.login,
            self._abort_login
        )

        self._act(action)

    def _abort_login(self):
        raise LoginFailed()

    def _act(self, action):
        if action == 'b':
            self._balance()
        if action == 'd':
            self._deposit()
        if action == 'r':
            self._report()
        if action == 'w':
            self._withdraw()

    def _balance(self):
        self.menu.balance(self.customer.balance)

    def _deposit(self):
        amount = self.menu.deposit()
        self.customer.deposit(amount)

    def _withdraw(self):
        amount = self.menu.withdraw()
        self.customer.withdraw(amount)

    def _report(self):
        body = self.customer.history.body
        footer = self.customer.history.footer
        self.menu.report(body, footer)


def main():
    ATM(
        Menu(system.current()),
        Customers()
    ).start()


if __name__ == "__main__":
    main()
