'''Usually I devide exceptions into Apologies and Complaints. A complaint is a message about an invalid system state that should halt your application. Apologies are states that are best avoided but that you can recover from.'''

class Complaint(Exception):
    @classmethod
    def complain(self):
        raise self()

class Exit(Exception):
    pass

class UnknownCustomer(Complaint):
    pass

class LoginFailed(Complaint):
    pass

