from datetime import timedelta, datetime

from SlippStockCrawler import SlippStockCrawler

crawler = SlippStockCrawler()

if __name__ == "__main__":
    with open("top10_buy_list.txt", 'rt') as f:
        top10_buy_list = f.readlines()

        end = datetime.today()
        start = end - timedelta(days=3)

        corp_info = crawler.select_kospi_corp_list()
        stock = crawler.select_stock_price_model(row_limit=2)

        # buy list
        for row_data in top10_buy_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]
            name = corp_info.loc[code]['회사명']

            close = stock[code]['Close']
            close = close[:-1]

            print('{}|{}|{}|{}'.format(code, name, price, close.values[0]))