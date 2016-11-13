import json
import sys

class Currency:

    rateDict = dict()

    """Creates currency with sender receiver and amount"""
    def __init__ (self, country):
        self.country = country

    def getExchangeRate(self, currency):
        with open('../rates.json') as json_data:
            d = json.load(json_data)
            rateDict = d
        return self.rateDict[self.country][currency.country]
