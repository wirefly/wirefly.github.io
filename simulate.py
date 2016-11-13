from random import randint, choice
from Model.Payment import Payment

class simulate():

    def simulatePaymets(userBaseList):
        paymentList = []
        n = 10000
        while n > 0:
            userFrom = userBaseList[randint(0, len(userBaseList)) - 1]
            userTo = userBaseList[randint(0, len(userBaseList)) - 1]
            amount = randint(2000, 100000)
            while userFrom.getCurrency() == userTo.getCurrency():
                userTo = userBaseList[randint(0, len(userBaseList)) - 1]
            payment = Payment(userFrom, userTo, amount)
            paymentList.append(payment)
            n -= 1
        return paymentList
