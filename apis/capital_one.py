import requests
import json
from Model import Account

apiKey = 'f1eefaa9631867b1e47580406a2dcc83'


def createAccount(first_name, last_name, currency, isBank):
    url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
    # City represents the currency that the user uses
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "address": {
            "state": "TL",
            "zip": "12345",
            "street_number": "string",
            "street_name": isBank,
            "city": currency}

    }
    response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
    )

    if response.status_code == 201:
        print('account created')
    else:
        print("failed bitch ", response.text, response.reason)


def createCustomer(first_name, last_name, currency, isBank):
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
        print('account created')
        customerId = data['objectCreated']['_id']
        return addAccount(first_name, last_name, customerId, currency, isBank)
    else:
        print("failed bitch ", response.text, response.reason)


def addAccount(first_name, last_name, customerId, currency, isBank):
    url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId, apiKey)
    payload = {
        "type": "Savings",
        "nickname": "test",
        "rewards": 10000,
        "balance": 1000000000,
    }
    # Create a Savings Account
    response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
    )
    if response.status_code == 201:
        print('account created')
        accountId = data['objectCreated']['_id']
        name = first_name + " " + last_name
        account = Account(accountId, name, currency, isBank)
        return account
    else:
        print("failed bitch ", response.text, response.reason)
        return None


def getAllCustomers():
    url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
    response = requests.get(url)
    if response.status_code == 201:
        print(response.text)
    else:
        print("failed bitch ", response.text, response.reason)
