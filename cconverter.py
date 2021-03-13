import requests

from typing import Dict, Any

FLOAT_RATES_URL = "http://www.floatrates.com/daily/"


def get_currency_json(url: str, currency: str) -> Dict[str, Any]:
    r = requests.get(f"{url}{currency}.json")
    return r.json()


def converter(amount_to_exchange: float, exchange_rate: float) -> float:
    return round(amount_to_exchange * exchange_rate, 2)


if __name__ == '__main__':
    initial_currency: str = input()
    currency_rates_json: Dict[str, Any] = get_currency_json(FLOAT_RATES_URL, initial_currency)

    cache: Dict = {}

    if "usd" in currency_rates_json.keys():
        cache["usd"] = currency_rates_json["usd"]["rate"]
    if "eur" in currency_rates_json.keys():
        cache["eur"] = currency_rates_json["eur"]["rate"]

    while True:
        wanted_currency: str = input()
        if len(wanted_currency) == 0:
            break
        money: float = float(input())

        print("Checking the cache...")
        if wanted_currency in cache.keys():
            print("Oh! It is in the cache!")
        else:
            print("Sorry, but it is not in the cache!")
            cache[wanted_currency] = currency_rates_json[wanted_currency]["rate"]

        converted_money = converter(money, cache[wanted_currency])
        print(f"You received {converted_money} {wanted_currency.upper()}.")

