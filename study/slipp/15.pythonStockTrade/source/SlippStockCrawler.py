import enum
import sqlite3
from datetime import timedelta, datetime
from io import BytesIO

import pandas as pd
import pandas_datareader.data as web
import requests


def calc_available_days(moving_average_days):
    # 장이 열리지 않는 날은 제외되므로 이동평균을 구할 수 있는 일 수를 계산한다.
    max_ma_days = max(moving_average_days)
    weekend_days = int(max_ma_days / 5 * (2 + 1))
    holidays = int(max_ma_days * 0.1)

    total_days = max_ma_days + weekend_days + holidays
    print('total_days : {}'.format(total_days))

    return total_days


class MarketType(enum.Enum):
    KOSPI = 'stockMkt'
    KOSDAQ = ''


class SlippStockCrawler:

    # properties
    db_name = 'slipp_stocks'
    corp_list_tbl_name = 'corporation'
    stock_price_tbl_prefix = 'stock_'
    moving_average_days = [5, 20, 60]
    ma_caculatable_days = calc_available_days(moving_average_days)
    # ==================================

    def __init__(self):
        print("init")

    # sqlite IO
    # db connection 맺기.
    def get_sqlite_connection(self):
        return sqlite3.connect("{}.db".format(self.db_name))

    # dataframe 저장하기
    def insert_dataframe(self, df=None, tbl_name='tbl_exam', exist_policy='replace', con=None):
        if con is None:
            with self.get_sqlite_connection() as conn:
                df.to_sql(tbl_name, conn, if_exists=exist_policy)
        else:
            df.to_sql(tbl_name, con, if_exists=exist_policy)

    # sql 조회하기
    # return dataframe
    def select_dataframe(self, sql='select 1', index_col_name=None, con=None):
        if con is None:
            with self.get_sqlite_connection() as conn:
                return pd.read_sql(sql, conn, index_col=index_col_name)
        else:
            return pd.read_sql(sql, con, index_col=index_col_name)


    # kospi 법인 목록 크롤링
    def crawling_kospi_corp_list(self, market_type):

        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
        # 파싱할 데이터, 소스에서 확인
        data = {
            'method': 'download',
            'orderMode': '3',
            'orderStat': 'A',
            'searchType': '13',
            'marketType': market_type.value,   # stockMkt
            'fiscalYearEnd': 'all',
            'location': 'all'
        }
        dataframe = pd.read_html(BytesIO(requests.post(url, data=data).content), header=0, parse_dates=['상장일'])[0]
        dataframe['종목코드'] = dataframe['종목코드'].map('{:06d}'.format)  #6자리 0으로 시작할 수 있는 코드로 세팅
        dataframe['시장구분'] = market_type.name
        dataframe = dataframe.set_index('종목코드')
        dataframe = dataframe.loc[:, ['시장구분', '회사명', '상장일']]
        # dataframe['상장일'] = pd.to_datetime(dataframe['상장일']).apply(lambda x: x.date())   # timestamp -> date 로 변경

        return dataframe

    # kospi 법인 목록 sqlite 조회하기
    def select_kospi_corp_list(self, limit=None):

        limit_phrases = ''

        # 테스트용으로 길이 제한이 필요한 경우.
        if limit is not None:
            limit_phrases = ' limit ' + str(limit)

        return self.select_dataframe("SELECT 종목코드, 회사명, 상장일 FROM {}{}".format(self.corp_list_tbl_name, limit_phrases), '종목코드')


    # yahoo 데이터 사용
    def crawling_stock_price(self, code, start=None, end=None):

        # 종목 선택
        df = web.DataReader(code + ".KS", "yahoo", start, end)

        df.rename(columns={
            'Adj Close': 'Adj_Close'
        }, inplace=True)

        # 주말에는 장이 열리지 않으므로 제거
        df = df[df['Volume'] != 0]

        return df

    # 이동평균 데이터 추가
    def append_moving_averages(self, df):

        # if len(df) < max(self.moving_average_days):
        #     print('데이터가 충분하지 않음. : {}'.format(len(df)))
        #     return df

        for day in self.moving_average_days:
            df = self.append_moving_average(df, day)

        # ma_col_name = 'MA'+str(max(self.moving_average_days))
        # return df[df[ma_col_name] == df[ma_col_name]]   #

        return df

    # 데이터 세팅
    # setup_type ( init : 초기 데이터 세팅, daily : 일별 데이터 추가 )
    def setup_data(self, setup_type):
        # 코스피 법인 목록 크롤링
        kospi_corp_info = self.crawling_kospi_corp_list(MarketType.KOSPI)

        # 법인 목록 sqlite 저장
        self.insert_dataframe(kospi_corp_info, self.corp_list_tbl_name)

        total = len(kospi_corp_info)
        insert_error_code_list = []
        with self.get_sqlite_connection() as con:
            for i, code in enumerate(kospi_corp_info.index.values):
                # test
                # if code in ('005450','006490','009970','152550','145210','300720','293940','010400','293480','306200'):
                try:
                    self.insert_stock_price_model(code, con, setup_type)
                    print('{} / {} : {}'.format(i, total, code))
                except:
                    print('{} / {} : {} - 주가 모델 저장 불가'.format(i, total, code))
                    insert_error_code_list.append(code)

        return insert_error_code_list

    def insert_stock_price_model(self, code, con, setup_type):

        start = '2000-01-01'
        exist_policy = ''

        if setup_type is 'init':
            exist_policy = 'replace'

        elif setup_type is 'daily':
            start = datetime.today() - timedelta(days=self.ma_caculatable_days)
            exist_policy = 'append'

        price_df = self.crawling_stock_price(code, start)
        price_df = self.append_moving_averages(price_df)

        if setup_type is 'daily':
            price_df = price_df[datetime.today().date():]  # 이동평균 계산 후 오늘 날짜의 데이터만 남김

        self.insert_dataframe(price_df, self.stock_price_tbl_prefix + code, exist_policy, con)

    # 종목별 주가 dataframe sqlite 조회하기
    def select_stock_price_model(self, corp_limit=None, row_limit=None):

        model = {}
        kospi_corp_info = self.select_kospi_corp_list(corp_limit)

        limit_phrases = ''
        if row_limit is not None:
            limit_phrases = ' limit ' + str(row_limit)

        with self.get_sqlite_connection() as con:
            for code in kospi_corp_info.index.values:
                try:
                    model[code] = self.select_dataframe(
                        "SELECT * FROM (SELECT * FROM {} ORDER BY Date DESC {}) ORDER BY Date ASC"
                            .format(self.stock_price_tbl_prefix + code, limit_phrases)
                        , 'Date', con)
                except:
                    print('조회 불가 : {}'.format(code))

        return model

    # 예측일 주가 예측을 위한 dataframe sqlite 조회하기
    def select_stock_price_model_for_predict(self, corp_limit=None, predict_date=(datetime.today().date()+timedelta(days=1))):

        model = {}
        kospi_corp_info = self.select_kospi_corp_list(corp_limit)

        with self.get_sqlite_connection() as con:
            for code in kospi_corp_info.index.values:
                try:
                    model[code] = self.select_dataframe(
                        "SELECT * FROM (SELECT * FROM {} WHERE Date < '{}' ORDER BY Date DESC limit { }) ORDER BY Date ASC"
                            .format(self.stock_price_tbl_prefix + code, max(self.moving_average_days))
                        , 'Date',predict_date , con)
                except:
                    print('조회 불가 : {}'.format(code))

        return model

    def init_crawling(self):
        print("error_code_list : {}".format(self.setup_data('init')))

    def daily_crawling(self):
        print("error_code_list : {}".format(self.setup_data('daily')))

    @staticmethod
    def append_moving_average(df, days, target_col_name='Adj_Close', round_num=0):
        col_name = "MA" + str(days)
        ma = df[target_col_name].rolling(window=days).mean().round(round_num)
        df.insert(len(df.columns), col_name, ma)

        return df


if __name__ == "__main__":
    SlippStockCrawler().daily_crawling()
