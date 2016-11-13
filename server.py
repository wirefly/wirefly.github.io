from flask import Flask, request
from optparse import OptionParser
import optimal_flow as of
import simulate

from Model import Currency, Account, Payment, capital_one as co


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
    sender = addCustomer("Sender","Account" , from_curr, False)
    receiver = addCustomer("Receiver","Account" , to_curr, False)
    payment = Payment(sender, receiver, _amount)

    paymentList = simulatePayments(co.getAllAccounts())
    paymentList.append(payment)
    finalListPayments = solve_optimal(paymentList)
    for p in finalListPayments:
        co.transfer(p.sender, p.receiver, p.amount)


    return 'Internal Cots, External Cost, (Maybe) Money Saved'


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="portnum", help="Enter port number for server", metavar=False)
    options, args = parser.parse_args()
    if options.portnum is None:
        app.run(debug=True)
    else:
        PORT = int(options.portnum)
        app.run(host=None, port=PORT, debug=True)
