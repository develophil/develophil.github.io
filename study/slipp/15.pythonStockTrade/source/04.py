import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
from pandas import DataFrame
import datetime
import sqlite3
import os
import pandas_datareader.data as web

MARKET_KOSPI   = 0
MARKET_KOSDAQ  = 10
TR_REQ_TIME_INTERVAL = 0.3

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(TR_REQ_TIME_INTERVAL)

        df = DataFrame(self.kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'],
                       index=self.kiwoom.ohlcv['date'])
        return df

    @staticmethod
    def get_ohicv_web(code):
        time.sleep(TR_REQ_TIME_INTERVAL)
        data = web.DataReader(code + ".KS", "yahoo")

        return data


    def saveAllStockPrice(self, codes):
        num = len(codes)

        # sqlite db 연결
        con = sqlite3.connect(os.getcwd() + "/stock.db")

        for i, code in enumerate(codes):
            print(i, '/', num, ':', code)
            df = self.get_ohlcv_web(code)
            print(df)
            # df.to_sql(code, con, if_exists='replace')

    def run(self):

        # kospi
        self.saveAllStockPrice(self.kospi_codes)
        # kosdaq
        self.saveAllStockPrice(self.kosdaq_codes)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()