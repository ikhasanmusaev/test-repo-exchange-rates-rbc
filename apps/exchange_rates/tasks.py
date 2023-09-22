import datetime
import django
import os

import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
django.setup()

from exchange_rates.models import Currency, DailyRate

header = {
    'Content-Type': 'application/json'
}
url = 'https://www.cbr-xml-daily.ru/daily_json.js'
url_archive = 'https://www.cbr-xml-daily.ru/archive/{year}/{mm}/{dd}/daily_json.js'
today = datetime.datetime.today()


def get_or_create_currency(currency_code, currency_object):
    currency, _created = Currency.objects.get_or_create(
        num_code=currency_code,
        defaults={
            'id_cbr': currency_object['ID'],
            'char_code': currency_object['CharCode'],
            'name': currency_object['Name'],
        }
    )
    return currency


def add_or_update_rate(date, value, nominal, currency_id):
    DailyRate.objects.update_or_create(
        defaults={
            'value': value,
            'nominal': nominal
        },
        currency_id=currency_id,
        date=date,
    )


def add_today_rates():
    today_rates_list = requests.get(url, ).json()

    if 'Valute' in today_rates_list:

        for currency_code, currency_object in today_rates_list['Valute'].items():
            currency = get_or_create_currency(currency_code, currency_object)
            add_or_update_rate(
                today,
                currency_object['Value'],
                currency_object['Nominal'],
                currency.id,
            )


def add_daily_rates():
    delta = datetime.timedelta(days=1)
    start_date = today - datetime.timedelta(days=30)

    # Check or update latest 30 days rates, without today
    while start_date < today:
        one_rates_day = (url_archive.format(year=start_date.strftime('%Y'),
                                            mm=start_date.strftime('%m'),
                                            dd=start_date.strftime('%d')))
        one_day_rates_list = requests.get(one_rates_day, ).json()
        if 'Valute' in one_day_rates_list:
            for currency_code, currency_object in one_day_rates_list['Valute'].items():
                currency = get_or_create_currency(currency_code, currency_object)
                add_or_update_rate(
                    start_date,
                    currency_object['Value'],
                    currency_object['Nominal'],
                    currency.id,
                )

        start_date += delta


add_today_rates()
add_daily_rates()
