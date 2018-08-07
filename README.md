# Kiwi Currency Converter Task

## Dependencies
* flask
* requests
* requests-cache
* internet connection

## CLI
```
Currency converter from specified currency to another currency or to all known currencies if not specified.

optional arguments:
  -h, --help            show this help message and exit
  --amount AMOUNT       must be a float number
  --input_currency INPUT_CURRENCY
                        3 letters name or currency symbol
  --output_currency OUTPUT_CURRENCY
                        3 letters name or currency symbol, if not specified
                        conversion is performed to all known currencies
```
### Implementation
File: `currency_converter.py`

CLI is very simple: command line arguments are parsed using `argparse` module and API call is performed using requests module. JSON output is pretty-formatted and printed out to standard output. In case of HTTP error from web API, corresponding error message is printed to standard error output.

## Web API
Files: `server.py`, `converter.py`

Running script `server.py` will open server on `127.0.0.1` and port `50000`.
### Implementation
Web API was implemented using Flask module which is configures to receive requests as specified in assignment. It uses single instance of Converter class which is implemented in `converter.py` module using its `convert()` method. Results are sent back to client in JSON format. Possible exceptions raised by Converter class are interpreted as HTTP error status codes.

Converter class uses exchange rates obtained from Rates API (https://ratesapi.io/documentation/), which is free web API based on data from European Central Bank and includes 33 currencies. Rates API is built to be compatible with paid Fixer.io API which includes much more currencies.

Exchange rates are from Rates API obtained again using requests module and data are cached using requests_cache module. Cache is stored in memory with expiry time of 10 minutes.

As some currencies use the same symbol, it wasn't possible to support every currency with its symbol and thus list of currency symbols were reduces with regard to contain important currencies or those included in Rates API list.
