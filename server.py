from flask import Flask, request
from optparse import OptionParser

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/getConversion', methods=['GET', 'POST'])
def retrieve_command():
    in_currency = request.args.get('from_curr')
    out_currency = request.args.get('to_curr')
    amount = request.values.get('amount')
    # do all the mehtods with this information and then
    # retrun the internal and external cost calculated by that
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
