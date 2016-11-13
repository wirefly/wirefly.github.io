from random import randint, choice
from Model.Payment import Payment

class simulate():

    def simulatePaymets(self, userBaseList):
        paymentList = []
        n = 10000
        while n > 0:
            userFrom = userBaseList[(0, len(userBaseList))]
            userTo = userBaseList[randint(0, len(userBaseList))]
            amount = randint(2000, 100000)
            while userFrom.getCurrency() == userTo.getCurrency():
                userTo = userBaseList[randint(0, len(userBaseList))]
            payment = payment(userFrom, userTo, amount)
            paymentList.append(payment)
        return paymentList