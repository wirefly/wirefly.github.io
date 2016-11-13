from flask import Flask, request, send_from_directory
from optparse import OptionParser
import optimal_flow as of
import simulate
from Model import Currency, Account, Payment, capital_one as co


app = Flask(__name__)
app._static_folder = ''
# app.config.from_object(__name__)

user_list = None

@app.route('/getConversion')
def retrieve_command():
    from_curr = request.args.get('from_curr')
    to_curr = request.args.get('to_curr')
    _amount = request.values.get('amount')

    fromCurrency = Currency.Currency(from_curr)
    toCurrency = Currency.Currency(to_curr)
    sender = co.addCustomer("Sender", "Account", from_curr, False)
    receiver = co.addCustomer("Receiver", "Account", to_curr, False)
    co.saveAllAccounts()
    payment = Payment.Payment(sender, receiver, _amount)

    paymentList = simulate.simulate.simulatePaymets(user_list)
    # paymentList.append(payment)
    # finalListPayments = of.solve_optimal(paymentList)
    finalRate = None
    finalValue = None
    for p in paymentList:
        co.transfer(p.sender, p.receiver, p.amount)
        if p.receiver.uid == receiver.uid:
            finalValue = p.amount
            finalRate = p.sender.currency.getExchangeRate(p.receiver.currency)

    return finalValue, finalRate

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="portnum", help="Enter port number for server", metavar=False)
    options, args = parser.parse_args()
    user_list = co.getAllCustomers()
    if options.portnum is None:
        app.run(debug=True)
    else:
        PORT = int(options.portnum)
        app.run(host=None, port=PORT, debug=True)
