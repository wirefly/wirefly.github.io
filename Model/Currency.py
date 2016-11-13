import numpy as np
import json
import sys

class Currency:

    rateDict = dict()

    """Creates currency with sender receiver and amount"""
    def __init__ (self, country):
        self.fee = np.random.uniform(0.1, 0.2)
        self.country = country

    def get_fee_rate(self, currency):
        return self.fee

    def getExchangeRate(self, currency):
        with open('rates.json') as json_data:
            d = json.load(json_data)
            self.rateDict = d
        if self.country in self.rateDict:
            if currency.country in self.rateDict:
                return self.rateDict[self.country][currency.country]
            else:
                return .69
        return .69
