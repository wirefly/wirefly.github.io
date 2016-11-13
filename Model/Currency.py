import json
import sys

class Currency:

    rateDict = dict()

    with open('rates.json') as json_data:
        d = json.load(json_data)
        rateDict = json.JSONDecoder().decode(d)


    """Creates currency with sender receiver and amount"""
    def __init__ (self, country):
        self.country = country

    def getExchangeRate(self, currency):
        return self.rateDict[self.country][currency.country]
