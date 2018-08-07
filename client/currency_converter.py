# -*- coding: utf-8 -*-

# Simple CLI for converting currencies using web API
# Adam Šuba
# Kiwi Currency converter task

import argparse
import sys
import requests
import json
from urllib.parse import urlencode

SERVER_ADDR = '127.0.0.1'
SERVER_PORT = 50000

parser = argparse.ArgumentParser(description='Currency converter from specified currency to another currency'
                                             'or to all known currencies if not specified.')
parser.add_argument('--amount', type=float, required=True, help='must be a float number')
parser.add_argument('--input_currency', required=True, help='3 letters name or currency symbol')
parser.add_argument('--output_currency', help='3 letters name or currency symbol, if not specified conversion is '
                                              'performed to all known currencies')

args = vars(parser.parse_args())
params = {arg: val for arg, val in args.items() if val is not None}
try:
    url = 'http://' + SERVER_ADDR + ':' + str(SERVER_PORT) + '/currency_converter'
    response = requests.get(url, params=urlencode(params))
    if response.status_code == 200:
        print(json.dumps(json.loads(response.text), indent=4))
    elif response.status_code == 400:
        # amount as float is secured by argparse, only possible status code 400 error is unknown currency
        print('Unknown currency entered.', file=sys.stderr)
    else:
        response.raise_for_status()
except requests.exceptions.RequestException:
    print('Currency conversion service is unavailable.', file=sys.stderr)
