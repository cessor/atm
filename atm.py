import menu
from model import Accounts, History, Table, File
import system


KEEP_RUNNING = True
STOP = False


class ATM(object):
    '''Controls a users's interactions with the ATM.'''
    def __init__(self, menu, accounts, history):
        self.accounts = accounts
        self.history = history
        self.menu = menu

        self.account = None

    def start(self):
        running = KEEP_RUNNING
        while running:
            running = self._session()
        self.menu.goodbye()

    def _session(self):
        self.menu.branding()

        try:
            self._init_account()
            self._handle_user_action()

        except UnknownCustomer:
            self.menu.invalid_account()
            return STOP

        except LoginFailed:
            self.menu.login_failed()
            return STOP

        except Exit:
            return STOP

        except KeyboardInterrupt:
            return STOP

        except:
            print("An unknown error occured. Aborting")
            return STOP

        finally:
            self.history.save()

        return KEEP_RUNNING

    def _init_account(self):
        if not self.account:
            self.account = self.accounts.find(
                self.menu.account_number,
                self._abort_unknown_account
            )
            self.menu.welcome(self.account.name)

    def _handle_user_action(self):
        choice = self.menu.choose_action().lower()

        if choice == 'q':
            raise Exit()

        # Any action other than exit requires a login first
        self.account = self.account.authenticate(
            self.menu.login,
            self._abort_login
        )

        self._act(choice)

    def _abort_unknown_account(self):
        raise UnknownCustomer()

    def _abort_login(self):
        raise LoginFailed()

    def _act(self, choice):
        actions = {
            'b': self._balance,
            'd': self._deposit,
            'r': self._report,
            'w': self._withdraw,
        }
        action = actions.get(choice, lambda: None)
        action()

    def _balance(self):
        self.menu.balance(
            self.history.balance_for(self.account.number)
        )

    def _deposit(self):
        amount = self.menu.deposit()
        self.history.remember_deposit(self.account.number, amount)

    def _withdraw(self):
        amount = self.menu.withdraw()
        self.history.remember_withdraw(self.account.number, amount)

    def _report(self):
        self.menu.report(
            self.history.report_for(self.account.number)
        )


class UnknownCustomer(Exception):
    pass


class LoginFailed(Exception):
    pass


class Exit(Exception):
    pass


def main():
    ATM(
        menu,
        Accounts(
            Table(
                File('accounts.txt')
            )
        ),
        History(
            Table(
                File('transactions.txt')
            )
        )
    ).start()


if __name__ == "__main__":
    main()
