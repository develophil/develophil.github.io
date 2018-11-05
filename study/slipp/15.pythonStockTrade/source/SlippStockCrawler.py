import gzip
import os
import pickle
import sqlite3
from datetime import timedelta
from io import BytesIO

import pandas as pd
import pandas_datareader.data as web
import requests


class SlippStockCrawler:
    def __init__(self):
        print("init")

    # 상장법인 목록 얻기
    @staticmethod
    def get_stock_code_list():
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
        # 파싱할 데이터, 소스에서 확인
        data = {
            'method': 'download',
            'orderMode': '3',
            'orderStat': 'D',
            'searchType': '13',
            'marketType': 'stockMkt',   # kospi
            'fiscalYearEnd': 'all',
            'location': 'all'
        }
        dataframe = pd.read_html(BytesIO(requests.post(url, data=data).content), header=0, parse_dates=['상장일'])[0]
        # dataframe['종목코드'] = dataframe['종목코드'].astype(np.str)  # 타입 변환
        # dataframe['종목코드'] = dataframe['종목코드'].str.zfill(6)  # 빈자리 0으로 채움
        dataframe['종목코드'] = dataframe['종목코드'].map('{:06d}'.format)  #6자리 0으로 시작할 수 있는 코드로 세팅

        dataframe = dataframe.loc[:, ['종목코드']]

        dataframe = dataframe[0:10] # 테스트용으로 10개만 자르기

        return dataframe['종목코드']

    @staticmethod
    def get_sqlite_connection():
        # sqlite 현재 폴더 stock.db 연결
        return sqlite3.connect(os.getcwd() + "/stock.db")

    def get_kospi_stock_price(self, start, end, seq_length):
        codes = self.get_stock_code_list()
        num = len(codes)

        stock_data = {}

        min_available_days = 60 + seq_length
        min_search_days = min_available_days + int(min_available_days / 5 * 3)
        print("min_search_days : ", min_search_days)

        for i, code in enumerate(codes):
            try:
                df = self.get_available_stock(code, start, end, min_search_days)
                print(i, '/', num, ':', code, '(', len(df), ')')

                if (len(df) < 60 + seq_length):
                    print('not efficient rows')
                    continue

                df = self.append_moving_average(df, 5)
                df = self.append_moving_average(df, 20)
                df = self.append_moving_average(df, 60)
                # df = self.append_moving_average(df, 120)

                df = df[df['MA60'] == df['MA60']]
                print(df)
                # df.to_sql(code, con, if_exists='replace')
                stock_data[code] = df
            except:
                print('error')

        return stock_data

    def run(self):
        stock_data = self.get_kospi_stock_price()
        self.save_stock_data(stock_data)

    @staticmethod
    def save_stock_data(data):
        with gzip.open('kospi_stock_price.pickle', 'wb') as f:
            pickle.dump(data, f)
            f.close()

    @staticmethod
    def view_pickle():
        with gzip.open('kospi_stock_price.pickle', 'rb') as f:
            data = pickle.load(f)
            print("==================pickle=================")
            print(len(data))
            f.close()

    @staticmethod
    def save_test():
        with gzip.open('test.pickle', 'rb') as f:
            data = pickle.load(f)
        with gzip.open('test.pickle', 'wb') as f:
            data.update({'33': 123, '44': 44444})
            pickle.dump(data, f)
            f.close()

    @staticmethod
    def view_test():
        with gzip.open('test.pickle', 'rb') as f:
            data = pickle.load(f)
            print("==================pickle=================")
            print(data)
            f.close()

    @staticmethod
    def get_available_stock(code, start, end, min_search_days):

        if(start is not None):
            start = start - timedelta(days=min_search_days)

        # 종목 선택
        gs = web.DataReader(code + ".KS", "yahoo", start, end)
        gs[["High", "Low", "Open", "Close", "Volume", "Adj Close"]] = gs[
            ["High", "Low", "Open", "Close", "Volume", "Adj Close"]].round()
        # print(gs)
        # 주말에는 장이 열리지 않으므로 제거
        return gs[gs['Volume'] != 0]

    @staticmethod
    def append_moving_average(df, days):
        col_name = "MA" + str(days)
        ma = df['Adj Close'].rolling(window=days).mean().round(0)
        df.insert(len(df.columns), col_name, ma)

        return df


if __name__ == "__main__":
    crawler = SlippStockCrawler()
    crawler.run()
    crawler.view_pickle()

    # SlippStockCrawler.save_test()
    # SlippStockCrawler.view_test()
