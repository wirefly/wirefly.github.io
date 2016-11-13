from datetime import timedelta
from flask import Flask, request, send_from_directory, make_response, current_app
from functools import update_wrapper
from optparse import OptionParser
import json
import optimal_flow as of
import simulate
from Model import Currency, Account, Payment, capital_one as co


app = Flask(__name__)
app._static_folder = ''
# app.config.from_object(__name__)

user_list = co.getAllAccounts()

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None:
        headers = ', '.join(x.upper() for x in headers)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/getConversion')
@crossdomain(origin="*")
def retrieve_command():
    from_curr = request.args.get('from_curr')
    to_curr = request.args.get('to_curr')
    _amount = request.values.get('amount')
    try:
        fromCurrency = Currency.Currency(from_curr)
        toCurrency = Currency.Currency(to_curr)
        sender = co.addCustomer("Sender", "Account", from_curr, False)
        receiver = co.addCustomer("Receiver", "Account", to_curr, False)
        co.saveAllAccounts()
        payment = Payment.Payment(sender, receiver, _amount)
        print(type(user_list))
        paymentList = simulate.simulate.simulatePaymets(user_list)
        paymentList.append(payment)
        finalListPayments = of.solve_optimal(paymentList)
        finalRate = -1
        finalValue = -1
        for p in paymentList:
            co.transfer(p.sender, p.receiver, p.amount)
            if p.receiver.uid == receiver.uid:
                print("HERE")
                finalValue = p.amount
                finalRate = p.sender.currency.getExchangeRate(p.receiver.currency)
        to_return = {'finalRate': finalRate, 'finalValue': finalValue}
        return json.dumps(to_return)
    except IndexError:
        return json.dumps({'finalRate': -1, 'finalValue': -1})

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="portnum", help="Enter port number for server", metavar=False)
    options, args = parser.parse_args()
    if options.portnum is None:
        app.run(debug=True)
    else:
        PORT = int(options.portnum)
        app.run(host=None, port=PORT, debug=True)
