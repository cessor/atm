'''Usually I devide exceptions into Apologies and Complaints. A complaint is a message about an invalid system state that should halt your application. Apologies are states that are best avoided but that you can recover from.'''

class Complaint(Exception):
    pass

class Exit(Exception):
    pass

class LoginFailed(Complaint):
    pass

class InvalidCustomer(Complaint):
    pass