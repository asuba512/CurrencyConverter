# -*- coding: utf-8 -*-

# Class for converting currencies used by web API server.
# Adam Šuba
# Kiwi Currency converter task

import json
import os

import requests
import requests_cache

TTL = 600  # cache TTL in seconds


class Converter:
    def __init__(self):
        requests_cache.install_cache('rates_cache', expire_after=TTL, backend='memory')
        symbols_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'currency_symbols.json')
        with open(symbols_file) as currencies:
            self.symbols = json.load(currencies)

    # returns corresponding code or if not found original symbol as code
    def symbol_to_code(self, symbol):
        if symbol in self.symbols:
            return self.symbols[symbol]
        else:
            return symbol

    def get_current_rates(self, base):
        response = requests.get('https://ratesapi.io/api/latest', params={'base': base})
        data = response.json()
        if response.status_code == 400 and data['error'] == 'Invalid base or symbols':
            raise UnknownCurrencyError
        response.raise_for_status()  # raise other request errors
        return data['rates']

    def convert(self, amount, input_currency, output_currency):
        try:
            input_currency = self.symbol_to_code(input_currency)
            output_currency = self.symbol_to_code(output_currency)
            rates = self.get_current_rates(input_currency)
            if output_currency is None:
                result = {currency: round(amount * rate, 2) for currency, rate in rates.items()}
            elif output_currency == input_currency:  # in case someone would convert same currencies
                result = {output_currency: round(amount, 2)}
            else:
                if output_currency not in rates:
                    raise UnknownCurrencyError
                result = {output_currency: round(amount * rates[output_currency], 2)}
            return input_currency, result
        except requests.exceptions.RequestException:
            raise RatesUnavailableError


class Error(RuntimeError):
    pass


class UnknownCurrencyError(Error):
    pass


class RatesUnavailableError(Error):
    pass
