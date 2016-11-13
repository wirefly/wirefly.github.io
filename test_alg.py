from optimal_flow import *
import numpy as np
from Model.Account import Account
from Model.Currency import Currency
from Model.Payment import Payment


def simple_test():
    u1 = Account(1, 'Connor', Currency('US'), False)
    u2 = Account(2, 'Tarun', Currency('Hungary'), False)
    u3 = Account(3, 'Gus', Currency('US'), False)
    u4 = Account(4, 'Cody', Currency('GB'), False)

    payments = []
    payments.append(Payment(u1, u2, 200))
    payments.append(Payment(u3, u4, 100))

    print(solve_optimal(payments))

simple_test()
