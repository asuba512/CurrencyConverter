# -*- coding: utf-8 -*-

# Server script providing web API for currency converter.
# Adam Šuba
# Kiwi Currency converter task

from flask import Flask, request, abort, jsonify
from converter import Converter, UnknownCurrencyError, RatesUnavailableError

PORT = 50000

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
converter = Converter()


@app.route('/currency_converter', methods=['GET'])
def currency_converter():
    amount = request.args.get('amount', type=float)
    input_currency = request.args.get('input_currency')
    output_currency = request.args.get('output_currency')
    if amount is None or input_currency is None:
        abort(400)  # bad request
    try:
        base, conversion = converter.convert(amount, input_currency, output_currency)
        result = {'input': {'amount': amount, 'currency': base}, 'output': conversion}
        return jsonify(result)
    except UnknownCurrencyError:
        abort(400)  # bad request
    except RatesUnavailableError:
        abort(503)  # service unavailable


if __name__ == '__main__':
    app.run(port=PORT)
