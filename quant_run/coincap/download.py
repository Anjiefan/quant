import json
import requests
import time
import datetime
import time
import datetime
from typing import List, Optional
from app.data_manager import ManagerEngine
from event import EventEngine
from trader.constant import Exchange, Interval
from trader.database.database_sql import SqlManager, init
from trader.engine import MainEngine
from trader.object import BarData, TickData
class Download:
    api='https://api.coincap.io/v2/candles'
    exchange='bitfinex'
    interval='m1'
    baseId='bitcoin'
    quoteId='united-states-dollar'
    symbol='BTCUSDT'
    exchange='BINANCE'
    start=1356969600000
    end=1356969600000
    def __init__(self,interval='m5',baseId='bitcoin',start=1356969600000,exchange='BINANCE',symbol='BTCUSDT'):
        self.interval=interval
        self.baseId=baseId
        self.start=start
        self.save()
    def save(self):
        self.end = round((datetime.datetime.fromtimestamp(self.start / 1000) + datetime.timedelta(days=1)).timestamp()*1000)
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
            self.end = round((datetime.datetime.fromtimestamp(self.start / 1000) + datetime.timedelta(days=1)).timestamp()*1000)
            response_data=json.loads(response.text)
            print(response_data)
            event_engine = EventEngine()
            main_engine = MainEngine(event_engine)
            data: List[BarData] = []
            for item in response_data:
                bar = BarData(
                    symbol=self.symbol,
                    exchange=self.exchange,
                    interval=self.interval,
                    datetime=datetime.datetime.fromtimestamp(item['period']/1000),
                    open_price=float(item["open"]),
                    high_price=float(item["high"]),
                    low_price=float(item["low"]),
                    close_price=float(item["close"]),
                    volume=float(item["volume"]),
                    open_interest=0,
                    gateway_name="RQ"
                )
                data.append(bar)
            from vnpy.trader.setting import get_settings

            settings = get_settings("database.")
            database_manager: "BaseDatabaseManager" = init(settings=settings)
            database_manager.save_bar_data(data)


if __name__ == '__main__':
    Download()
