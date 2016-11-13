import requests
import random
import json
from Account import Account

apiKey = 'f1eefaa9631867b1e47580406a2dcc83'
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
    payload = {
        "type": "Savings",
        "nickname": currency,
        "rewards": 10000,
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

def getAllCustomers():
    url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        print(response.text)
    else:
        print("failed bitch ", response.text, response.reason)

def generateCustomers():
    customers = []
    for x in range(0, 200):#Change the second argument to specify how many customers we want
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
def getAllAccounts(): #returns a list of all accounts in Account objects
    url = 'http://api.reimaginebanking.com/accounts/?key={}'.format(apiKey)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        print(response.text)
    else:
        print("failed bitch ", response.text, response.reason)
    data = response.json()
    acctList = []
    for x in range(0, len(data)):
        url_acct = 'http://api.reimaginebanking.com/customers/{}/?key={}'.format(data[x]['customer_id'], apiKey)
        response_acct = requests.get(url_acct)
        #print(response_acct.status_code)
        if response_acct.status_code == 200:
            print(response_acct.text)
        else:
            print("failed bitch ", response_acct.text, response_acct.reason)
        data_acct = response_acct.json()
        uid = data[x]['_id']
        name = data_acct['first_name'] + " " + data_acct['last_name']
        currency = data[x]['nickname']
        isBank = data_acct['address']['street_name']
        balance = data[x]['balance']
        acctList.append(Account(uid, name, currency, isBank, balance))
    return acctList
def transfer(payer_id, payee_id, amount):
    url = 'http://api.reimaginebanking.com/accounts/{}/transfers/?key={}'.format(payer_id, apiKey)
    payload = {
      "medium": "balance",
      "payee_id": payee_id,
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


