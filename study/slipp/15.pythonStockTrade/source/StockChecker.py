import sys
from datetime import timedelta, datetime

from SlippStockCrawler import SlippStockCrawler

crawler = SlippStockCrawler()
target_date = datetime(2018, 11, 12, 0, 0, 0, 0)
today = datetime.today()
between_days = (today-target_date).days + 2
print("betweendays : {}".format(between_days))

if __name__ == "__main__":
    # with open("top10_buy_list_org.txt", 'rt') as f:
    with open("top10_buy_list_{}.txt".format(str(target_date.date()).replace("-", "")), 'rt') as f:
        top10_buy_list = f.readlines()

        corp_info = crawler.select_kospi_corp_list()
        stock = crawler.select_stock_price_model(row_limit=between_days)
        # prev_date = target_date - timedelta(days=1)
        # print(target_date, '|', prev_date)

        print('종목코드,종목명,전일종가,예측종가,시가,실 종가')
        # buy list
        for row_data in top10_buy_list:
            split_row_data = row_data.split(';')
            code = split_row_data[1]
            price = float(split_row_data[-1])
            name = corp_info.loc[code]['회사명']

            target_date_df = stock[code][str(target_date):str(target_date)]
            # prev_date_df = stock[code][str(prev_date):str(prev_date)]

            indexes = stock[code].index.values

            prev_date_idx = -1
            if between_days > 2:
                prev_date_idx = list(indexes).index(str(target_date)) - 1

            prev_date_df = stock[code][indexes[prev_date_idx]:indexes[prev_date_idx]]

            try:
                target_open = target_date_df['Open'].values[0]
            except:
                target_open = 0

            try:
                target_close = target_date_df['Adj_Close'].values[0]
            except:
                target_close = 0

            try:
                prev_close = prev_date_df['Adj_Close'].values[0]
            except:
                prev_close = 0

            print('{},{},{},{},{},{}'.format(code, name, int(prev_close), int(price), int(target_open), int(target_close)))

sys.exit()
