class Account:

    """Creates account with uid, name, currency, and bank"""
    def __init__(self, uid, name, currency, isBank, balance=1000000000):
        self.uid = uid
        self.name = name
        self.currency = currency
        self.isBank = isBank
        self.balance = balance

    def getCurrency(self):
        return self.currency
    def printAccount(self):
    	print(self.uid + " " + self.name + " " + self.currency + " " + str(self.isBank) + "\n")