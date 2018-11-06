import gzip
import os
import pickle
import sqlite3
from datetime import timedelta, datetime
from io import BytesIO

import pandas as pd
import pandas_datareader.data as web
import requests

from SlippStockCrawler import SlippStockCrawler

crawler = SlippStockCrawler()

if __name__ == "__main__":
    with open("top10_buy_list.txt", 'rt') as f:
        top10_buy_list = f.readlines()
        print(top10_buy_list)

        end = datetime.today()
        start = end - timedelta(days=3)


        # buy list
        for row_data in top10_buy_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]

            stock = crawler.get_available_stock(code, start, end, 0)

            print(stock)


