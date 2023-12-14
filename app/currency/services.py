from fastapi import HTTPException

import json

import requests

from app.currency.statistics import calculate_eur_usd_and_chf_usd
from app.currency.utils import convert_data_to_list, make_data_to_insert


class CurrencyService:
    def __init__(self):
        self.api_url = "http://api.nbp.pl/api/exchangerates/"

    def get_currencies(self):
        response = requests.get(self.api_url + "tables/a/")
        data = json.loads(response.text)
        return data[0]["rates"]

    def get_rate_dates(self, counter: int = 1):
        response = requests.get(self.api_url + f"rates/a/eur/last/{counter}/")
        data = json.loads(response.text)
        return data["rates"]

    def get_currency_rate(self, currency_code: str, counter):
        response = requests.get(self.api_url + f"rates/a/{currency_code}/last/{counter}/")
        data = json.loads(response.text)
        return data["rates"]

    def get_today_currency_rate(self, currency: str):
        try:
            response = requests.get(self.api_url + f"rates/a/{currency}/today/")
            data = json.loads(response.text)
            return data["rates"][0]
        except IndexError:
            raise HTTPException(status_code=404, detail="Data not found")

    def prepare_currencies_to_db(self):
        eur_pln = convert_data_to_list(self.get_currency_rate("eur", 90))
        usd_pln = convert_data_to_list(self.get_currency_rate("usd", 90))
        chf_pln = convert_data_to_list(self.get_currency_rate("chf", 90))
        rate_dates = convert_data_to_list(self.get_rate_dates(90), "effectiveDate")
        eur_usd, chf_usd = calculate_eur_usd_and_chf_usd(eur_pln, usd_pln, chf_pln)
        data_to_insert = make_data_to_insert(eur_pln, usd_pln, chf_pln, eur_usd, chf_usd, rate_dates)
        return data_to_insert
