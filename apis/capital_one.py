import requests
import json

apiKey = 'f1eefaa9631867b1e47580406a2dcc83'
def createAccount(first_name, last_name, currency):
	url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
	#City 
	payload = {
	    "first_name": first_name,
	    "last_name": last_name,
	    "address": {
	    	"state": "TL",
	    	"zip": "12345",
	      	"street_number": "string",
	      	"street_name": "string",
	      	"city": currency}
			
		}
	response = requests.post( 
		url, 
		data=json.dumps(payload),
		headers={'content-type':'application/json'},
		)

	if response.status_code == 201:
		print('account created')
	else:
		print("failed bitch ", response.text, response.reason)
def getCustomers():
	url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
	response = requests.get(url)
	print(response.text)
def deleteCustomer(id_thing):

	url = 'http://api.reimaginebanking.com/customers/{}?key={}'.format(id_thing,apiKey)
	response = requests.delete(url)
	print(response.status_code)