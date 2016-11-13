import json
import sys

class Currency:

    with open('rates.json') as json_data:
        d = json.load(json_data)
        rateDict = json.JSONDecoder().decode(d)


    """Creates currency with sender receiver and amount"""
    def __init__ (self, country):
        self.country = country

    def getExchangeRate(self, currency):
        return rateDict[self]
