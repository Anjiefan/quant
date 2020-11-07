import time
import datetime
from typing import List, Optional
from app.data_manager import ManagerEngine
from event import EventEngine
from trader.constant import Exchange, Interval
from trader.database.database_sql import SqlManager, init
from trader.engine import MainEngine
from trader.object import BarData, TickData

if __name__ == '__main__':
    # event_engine = EventEngine()
    # main_engine = MainEngine(event_engine)
    # data: List[BarData] = []
    # bar = BarData(
    #     symbol=symbol,
    #     exchange=exchange,
    #     interval=interval,
    #     datetime=dt,
    #     open_price=row["open"],
    #     high_price=row["high"],
    #     low_price=row["low"],
    #     close_price=row["close"],
    #     volume=row["volume"],
    #     open_interest=0,
    #     gateway_name="RQ"
    # )
    # data.append(bar)
    # from vnpy.trader.setting import get_settings
    #
    # settings = get_settings("database.")
    # database_manager: "BaseDatabaseManager" = init(settings=settings)
    # database_manager.save_bar_data(data)
    end = 1356969600000
    print(datetime.datetime.fromtimestamp(end/1000))
