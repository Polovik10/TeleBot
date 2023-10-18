import requests
import json
from config import keys 

class ConvertionException(Exception):
    pass


class ExchangeRates:
    @staticmethod
    def convert(values):
        quote, base, amount = values
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            amount=float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
            
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

    @staticmethod
    def get_price(values):
        base, quote, amount = values
        total_base = ExchangeRates(values)
        text = f'{base} {quote} = {total_base}\n'

        return text