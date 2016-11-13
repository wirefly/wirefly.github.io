from flask import Flask, request
from optparse import OptionParser
import simulate
import Account
import Currency
import Payment

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/getConversion', methods=['GET', 'POST'])
def retrieve_command():
    in_name = request.args.get('in_account')
    from_curr = request.args.get('from_curr')
    out_name = request.args.get('out_account')
    to_curr = request.args.get('to_curr')
    _amount = request.values.get('amount')

    fromCurrency = Currency(from_curr)
    toCurrency = Currency(to_curr)
    sender = Account(uid, in_account, fromCurrency, isBank)
    receiver = Account(uid, name, toCurrency, isBank)
    payment = Payment(sender, reciever, _amount)

    paymentList.append(payment)

    return 'Internal Cots, External Cost, (Maybe) Money Saved'


if __name__ == "__main__":
    paymentList = simulatePaymets()
    transactionList = mipAlgorithm(paymentList)

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="portnum", help="Enter port number for server", metavar=False)
    options, args = parser.parse_args()
    if options.portnum is None:
        app.run(debug=True)
    else:
        PORT = int(options.portnum)
        app.run(host=None, port=PORT, debug=True)
