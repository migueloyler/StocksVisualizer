"""
Grabs stock information
"""

import requests
import csv
import io


def nasdaq_top_100():
    NASDAQ_100 = 'http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx?render=download'
    r = requests.get(NASDAQ_100)
    info = [row for row in csv.reader(io.StringIO(r.text))]
    return [row[0] for row in info[1:] if row[0] != 'XRAY']


def form_url(stock_symbols):
    """
    Returns a URL that grabs symbol(s), market cap(j1), and
    percent change from 50-day moving average (m8) for every symbol
    in 'stock_symbols'

    Args:
        stock_symbols (list of str): a list of individual stock symbols
    """
    # write def here


def main():
    print(requests.get(form_url(nasdaq_top_100())).text, end='')


if __name__ == '__main__':
    main()
