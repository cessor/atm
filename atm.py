import menu
from model import Customers, Report
import system

KEEP_RUNNING = True
STOP = False


class ATM(object):
    '''Controls a users's interactions with the ATM.'''
    def __init__(self, menu, customers):
        self.customers = customers
        self.menu = menu

        # NewCustomer()
        self.customer = None

    def start(self):
        running = KEEP_RUNNING
        while running:
            running = self._session()
        self.menu.goodbye()

    def _session(self):
        self.menu.branding()

        try:
            self._init_customer()
            self._handle_user_action()

        except UnknownCustomer:
            self.menu.invalid_customer()
            return STOP

        except LoginFailed:
            self.menu.login_failed()
            return STOP

        except Exit:
            return STOP

        except KeyboardInterrupt:
            return STOP

        # except:
        #     print("An unknown error occured. Aborting")
        #     return STOP

        finally:
            self.customers.save(self.customer)

        # Keep running
        return KEEP_RUNNING

    def _init_customer(self):
        if not self.customer:
            self.customer = self.customers.find(
                self.menu.customer_number,
                self._abort_unknown_customer
            )
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

    def _abort_unknown_customer(self):
        raise UnknownCustomer()

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
        self.menu.report(Report(self.customer.history))


class UnknownCustomer(Exception):
    pass


class LoginFailed(Exception):
    pass


class Exit(Exception):
    pass


def main():
    ATM(
        menu,
        Customers()
    ).start()


if __name__ == "__main__":
    main()
