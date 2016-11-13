from random import randint, choice

class simulate():

    paymentList = []

    def simulatePaymets(self, userBaseList):
        n = 10000
        while n > 0:
            userFrom = userBaseList[(0, len(userBaseList))]
            userTo = userBaseList[randint(0, len(userBaseList))]
            while userFrom.getCurrency() == userTo.getCurrency():
                userTo = userBaseList[randint(0, len(userBaseList))]
