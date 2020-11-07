import json
import requests
import time
import datetime
import time
import datetime
from typing import List, Optional
from trader.constant import Exchange, Interval
from trader.object import BarData, TickData
from trader.database.initialize import init
from vnpy.trader.setting import get_settings
class BitfinexDownload:
    interval_relate={
        'm1':Interval.MINUTE,
        'm5':Interval.MINUTE_5,
        'm15': Interval.MINUTE_15,
        'm30': Interval.MINUTE_30,
        'h1': Interval.HOUR,
        'h2':  Interval.HOUR_2,
        'h4':  Interval.HOUR_4,
        'h8':  Interval.HOUR_8,
        'h12':  Interval.HOUR_12,
        'd1':  Interval.DAILY,
        'w1':  Interval.WEEKLY,
    }
    api='https://api.coincap.io/v2/candles'
    exchange='bitfinex'
    interval='m1'
    baseId='bitcoin'
    quoteId='united-states-dollar'
    symbol='BTCUSDT'
    start=1356969600000
    end=1356969600000
    day=1
    def __init__(self,interval='m1',baseId='bitcoin',start=1356969600000,symbol='BTCUSDT',day=1):
        self.interval=interval
        self.baseId=baseId
        self.start=start
        self.day=day
        self.save()
    def save(self):
        self.end = round((datetime.datetime.fromtimestamp(self.start / 1000) + datetime.timedelta(days=self.day)).timestamp()*1000)
        while self.end<datetime.datetime.now().timestamp()*1000:
            response=requests.get(url=self.api,params={
                'exchange':self.exchange,
                'interval':self.interval,
                'baseId':self.baseId,
                'quoteId':self.quoteId,
                'start':self.start,
                'end':self.end
            })
            self.start=self.end
            self.end = round((datetime.datetime.fromtimestamp(self.start / 1000) + datetime.timedelta(days=self.day)).timestamp()*1000)
            response_data=json.loads(response.text)
            print(response_data)
            data: List[BarData] = []
            for item in response_data['data']:
                bar = BarData(
                    symbol=self.symbol,
                    exchange=Exchange.BITFINEX,
                    interval=self.interval_relate[self.interval],
                    datetime=datetime.datetime.fromtimestamp(item['period']/1000),
                    open_price=float(item["open"]),
                    high_price=float(item["high"]),
                    low_price=float(item["low"]),
                    close_price=float(item["close"]),
                    volume=float(item["volume"]),
                    open_interest=0,
                    gateway_name=Exchange.BITFINEX.value
                )
                data.append(bar)
            self.save_data(data=data)

    def save_data(self,data):
        settings = get_settings("database.")
        database_manager: "BaseDatabaseManager" = init(settings=settings)
        database_manager.save_bar_data(data)


if __name__ == '__main__':
    BitfinexDownload(day=30,interval='d1')
