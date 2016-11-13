import numpy as np

class Currency:

    """Creates currency with sender receiver and amount"""
    def __init__ (self, country):
        self.country = country

    def get_fee_rate(self, currency):
        # return np.random.uniform(0.1, 2)
        return 0.1
