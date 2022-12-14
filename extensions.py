import json
import requests



class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str, keys: dict):
        if quote == base:
            raise APIException(f'Вы указали одну и туже валюту "{base}".')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Вы указали неправильную валюту "{quote}".')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Вы указали неправильную валюту "{base}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Вы указали неправильное колличество "{amount}".')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(json.loads(r.content)[keys[base]] * amount, 2)

        return total_base