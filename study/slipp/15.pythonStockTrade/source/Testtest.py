from datetime import datetime, timedelta

from SlippStockCrawler import SlippStockCrawler

crawler = SlippStockCrawler()

# sqlite에서 종목별 주가 데이터 조회.
kospi_corp_info = crawler.select_kospi_corp_list()
# d = datetime.today() - timedelta(days=2)
# sql = "SELECT * FROM stock_000040 where Date >= '{}'".format(d.date())
# print(sql)
# data = SlippStockCrawler().select_dataframe(sql)
# print(data)


today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
# stock = SlippStockCrawler().crawling_stock_price('000040', '2018-11-07')
# print(stock)

# keys = [*data]
# print(keys)


with crawler.get_sqlite_connection() as con:

    print(crawler.crawling_stock_price('000040', datetime.today().date()))

    # total = len(kospi_corp_info)
    # for i, code in enumerate(kospi_corp_info.index.values):
    #     # test
    #     # if code in ('005450','006490','009970','152550','145210','300720','293940','010400','293480','306200'):
    #     print('{} / {} : {}'.format(i, total, code))
    #     price_df = crawler.crawling_stock_price(code, '2018-11-07')
    #     price_df = crawler.append_moving_averages(price_df)
