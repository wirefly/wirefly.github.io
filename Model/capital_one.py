import requests
import random
import json
# from Model import Account, Currency
from Model.Account import Account
from Model.Currency import Currency

apiKey = 'ab66e2459d00318d1e49fa563a71c34a'
currency_list = ['USD', 'IDR', 'BGN', 'ILS', 'GBP', 'DKK', 'CAD', 'JPY', 'HUF', 'RON', 'MYR', 'SEK', 'SGD', 'HKD', 'AUD', 'CHF', 'KRW', 'CNY', 'TRY', 'HRK', 'NZD', 'THB', 'EUR', 'NOK', 'RUB', 'INR', 'MXN', 'CZK', 'BRL', 'PLN', 'PHP', 'ZAR']
def addCustomer(first_name, last_name, currency, isBank):
    url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)

    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "address": {
            "state": "TL",
            "zip": "12345",
            "street_number": "string",
            "street_name": str(isBank),  # Street name distinguishes whether or not user is a bank
            "city": currency}  # City represents the currency that the user uses

    }
    response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
    )
    data = response.json()
    if response.status_code == 201:
        #print('customer created')
        customerId = data['objectCreated']['_id']
        return addAccount(first_name, last_name, customerId, currency, isBank)
    else:
        print("failed bitch ", response.text, response.reason)
        return None


def addAccount(first_name, last_name, customerId, currency, isBank):
    url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId, apiKey)
    iB = 1 #Replacement for isBank
    if isBank:
        iB = 1
    else:
        iB = 0
    payload = {
        "type": "Savings",
        "nickname": currency,
        "rewards": iB,# fix for customer problems
        "balance": 1000000000
    }
    # Create a Savings Account
    response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
    )
    data = response.json()
    if response.status_code == 201:
        #print('account created')
        accountId = data['objectCreated']['_id']
        name = first_name + " " + last_name
        account = Account(accountId, name, Currency(currency), isBank)
        return account
    else:
        print("failed bitch ", response.text, response.reason)
        return None

def printAllCustomers():
    url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        print(response.text)
    else:
        print("failed bitch ", response.text, response.reason)

def generateCustomers():
    customers = []
    for x in range(0, 100):#Change the second argument to specify how many customers we want
        customers.append(addCustomer("Customer", "Account", random.choice(currency_list), False))
    for c in currency_list:
        customers.append(addCustomer("Bank", "Account", c, True))
    return customers
def printAllAccounts():
    url = 'http://api.reimaginebanking.com/accounts/?key={}'.format(apiKey)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        print(response.text)
    else:
        print("failed bitch ", response.text, response.reason)
def saveAllAccounts(): #returns a list of all accounts in Account objects
    url = 'http://api.reimaginebanking.com/accounts/?key={}'.format(apiKey)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        print(response.text)
    else:
        print("failed bitch ", response.text, response.reason)
    data = response.json()
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
def getAllAccounts():
    acctList = []
    with open('data.txt') as data_file:
        data = json.load(data_file)
    for x in range(0, len(data)):
        uid = data[x]['_id']
        name = "Account"
        currency = data[x]['nickname']
        isBank = True
        if(data[x]['rewards'] == 1):
            isBank = True
        else:
            isBank = False
        balance = data[x]['balance']
        acctList.append(Account(uid, name, currency, isBank, balance))
    return acctList
def transfer(payer_id, payee_id, amount):
    payer_num = payer_id.uid
    payee_num = payee_id.uid
    print(payer_num, payee_num)
    url = 'http://api.reimaginebanking.com/accounts/{}/transfers/?key={}'.format(payer_num, apiKey)
    payload = {
      "medium": "balance",
      "payee_id": payee_num,
      "amount": amount,
      "transaction_date": "2016-11-13",
      "description": "transfer"
    }
    response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
    )
    print(response.status_code)
    if response.status_code == 201:
        print(response.text)
    else:
        print("failed bitch ", response.text, response.reason)
