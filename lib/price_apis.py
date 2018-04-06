import sys, os
sys.path.append(os.path.dirname(__file__))

import requests
import json
import time

import pandas as pd

import constants as C


def query(url):
    """Generic GET query returned as a dictionary"""
    return json.loads(requests.get(url).text)


def dict_to_df(price_dict, price_type):
    """Converts a price dictionary to a dataframe"""
    price_rows = [
        { C.SYMBOL: s, C.TYPE: price_type, C.PRICE: p, }
        for s, p in price_dict.items()
    ]

    return pd.DataFrame(price_rows)


def key_error_display(e, data):
    print('KeyError: {}'.format(e))
    print(data)
    time.sleep(C.HTTP_SLEEP)


def query_fail_display(service, symbols, url):
    print(
        'Failed to query {}.\n'.format(service) + \
        'Symbol(s):\n' +\
        ' {}\n'.format(symbols) +\
        'Query:\n' +\
        '{}\n'.format(url)
    )


def crypto_compare(syms, price_type):
    """For querying real-time crypto prices"""
    print('Querying CryptoCompare\n')

    prices = {}

    for s in list(set(syms)):
        print('Requesting symbol\n{}\n'.format(s))

        url =\
            'https://min-api.cryptocompare.com/data/price' +\
                '?fsym={}&tsyms=USD'\
                    .format(s)

        for idx in range(C.HTTP_RETRIES):
            data = query(url)

            try:
                prices[s] = data['USD']
                break

            except KeyError as e:
                key_error_display(e, data)

        else:
            query_fail_display('CryptoCompare', s, url)

    return dict_to_df(prices, price_type)


def alpha_vantage(syms, price_type):
    """For querying real-time stocks and ETFs"""

    print('Querying AlphaVantage\n')

    prices = {}

    # Has a 100 symbol limit on the batch query
    syms_100 = []
    for idx, s in enumerate(list(set(syms))):
        if not (idx % 100):
            syms_100.append([])

        syms_100[-1].append(s)

    for s_100 in syms_100:
        # AV recommends limiting to ~1 query per second
        time.sleep(C.AV_SLEEP)

        slist = ','.join(s_100)
        print('Requesting symbols\n{}\n'.format(slist))

        url = \
            'https://www.alphavantage.co/query' + \
                '?function=BATCH_STOCK_QUOTES&symbols={}&apikey={}'\
                    .format(slist, C.AV_KEY)

        for idx in range(C.HTTP_RETRIES):
            data = query(url)

            try:
                for q in data['Stock Quotes']:
                    p = float(q['2. price'])
                    if p:
                        prices[q['1. symbol']] = p

                break

            except KeyError as e:
                key_error_display(e, data)

        else:
            query_fail_display('AlphaVantage', slist, url)

    return dict_to_df(prices, price_type)

