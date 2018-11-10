from datetime import timedelta, datetime

from SlippStockCrawler import SlippStockCrawler

crawler = SlippStockCrawler()

if __name__ == "__main__":
    with open("top10_buy_list.txt", 'rt') as f:
        top10_buy_list = f.readlines()

        end = datetime.today()
        start = end - timedelta(days=3)

        corp_info = crawler.select_kospi_corp_list()
        stock = crawler.select_stock_price_model(row_limit=5)

        target_date = datetime(2018, 11, 6, 0, 0, 0, 0)
        prev_date = target_date - timedelta(days=1)

        print(target_date, '|', prev_date)

        print('종목코드|종목명|전일종가|예측종가|시가|실 종가')
        # buy list
        for row_data in top10_buy_list:
            split_row_data = row_data.split(';')
            code = split_row_data[1]
            price = float(split_row_data[-1])
            name = corp_info.loc[code]['회사명']

            target_date_df = stock[code][str(target_date):str(target_date)]
            prev_date_df = stock[code][str(prev_date):str(prev_date)]

            target_open = target_date_df['Open'].values[0]
            target_close = target_date_df['Adj_Close'].values[0]

            prev_close = prev_date_df['Adj_Close'].values[0]

            print('{}|{}|{}|{}|{}|{}'.format(code, name, int(prev_close), int(price), int(target_open), int(target_close)))