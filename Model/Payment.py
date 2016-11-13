class Payment():

    """Creates payment with sender receiver and amount"""
    def __init__ (self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = int(amount)
