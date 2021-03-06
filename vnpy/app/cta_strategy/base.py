"""
Defines constants and objects used in CtaStrategy App.
"""
import calendar
import datetime

from dataclasses import dataclass, field
from enum import Enum
from datetime import timedelta

from vnpy.trader.constant import Direction, Offset, Interval

APP_NAME = "CtaStrategy"
STOPORDER_PREFIX = "STOP"


class StopOrderStatus(Enum):
    WAITING = "等待中"
    CANCELLED = "已撤销"
    TRIGGERED = "已触发"


class EngineType(Enum):
    LIVE = "实盘"
    BACKTESTING = "回测"


class BacktestingMode(Enum):
    BAR = 1
    TICK = 2


@dataclass
class StopOrder:
    vt_symbol: str
    direction: Direction
    offset: Offset
    price: float
    volume: float
    stop_orderid: str
    strategy_name: str
    lock: bool = False
    vt_orderids: list = field(default_factory=list)
    status: StopOrderStatus = StopOrderStatus.WAITING


EVENT_CTA_LOG = "eCtaLog"
EVENT_CTA_STRATEGY = "eCtaStrategy"
EVENT_CTA_STOPORDER = "eCtaStopOrder"
now_date = datetime.datetime.now()

INTERVAL_DELTA_MAP = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.MINUTE_3: timedelta(minutes=3),
    Interval.MINUTE_5: timedelta(minutes=5),
    Interval.MINUTE_15: timedelta(minutes=15),
    Interval.MINUTE_30: timedelta(minutes=30),
    Interval.HOUR: timedelta(hours=1),
    Interval.HOUR_2: timedelta(hours=2),
    Interval.HOUR_4: timedelta(hours=4),
    Interval.HOUR_6: timedelta(hours=6),
    Interval.HOUR_8: timedelta(hours=8),
    Interval.HOUR_12: timedelta(hours=12),
    Interval.DAILY: timedelta(days=1),
    Interval.DAILY_3: timedelta(days=3),
    Interval.WEEKLY: timedelta(weeks=1),
    Interval.MONTH: timedelta(days=calendar.monthrange(now_date.year,now_date.month)[1]),
}
