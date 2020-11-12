from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,

)
from vnpy.trader.utility import GanManager


class EmaKMzStrategy(CtaTemplate):
    """演示用的简单双均线"""

    # 策略作者
    author = "Smart Trader"

    # 定义参数
    long_ema = 300
    short_ema = 60
    k_length = 60

    # # 定义变量
    # buy_inform = -1
    # sell_inform = -1
    # short_inform = -1
    # cover_inform = -1
    # 添加参数和变量名到对应的列表
    parameters = ["long_ema", "short_ema", "k_length"]
    # variables = ["buy_inform", "sell_inform", "short_inform", "cover_inform"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # K线合成器：从Tick合成分钟K线用
        self.bg = BarGenerator(self.on_bar)

        # 时间序列容器：计算技术指标用
        self.am = GanManager(size=self.long_ema+self.short_ema+1)

    def on_init(self):
        """
        当策略被初始化时调用该函数。
        """
        # 输出个日志信息，下同
        self.write_log("策略初始化")

        # 加载10天的历史数据用于初始化回放
        self.load_bar(40)

    def on_start(self):
        """
        当策略被启动时调用该函数。
        """
        self.write_log("策略启动")

        # 通知图形界面更新（策略最新状态）
        # 不调用该函数则界面不会变化
        self.put_event()

    def on_stop(self):
        """
        当策略被停止时调用该函数。
        """
        self.write_log("策略停止")

        self.put_event()

    def on_tick(self, tick: TickData):
        """
        通过该函数收到Tick推送。
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        通过该函数收到新的1分钟K线推送。
        """
        am = self.am

        # 更新K线到时间序列容器中
        am.update_bar(bar)

        # 若缓存的K线数量尚不够计算技术指标，则直接返回
        if not am.inited:
            return

        # 指标函数

        ##############################################################################
        # 指标信号发送池子
        # 计算快速均线

        inform = am.ema_k(long_ema=self.long_ema, short_ema=self.short_ema, k_length=self.k_length)
        buy_inform = (inform > 0)
        cover_inform = (inform > 0)
        sell_inform = (inform < 0)
        short_inform = (inform < 0)
        # # 交易信号
        # if inform > 0:
        #     buy_inform = True
        #     # sell_inform = -1
        #     # short_inform = -1
        #     cover_inform = True
        # elif inform < 0:
        #     # buy_inform = -1
        #     sell_inform = True
        #     short_inform = True
        #     # cover_inform = -1
        # print(buy_inform,sell_inform,short_inform)
        # 买入信号
        if buy_inform:
            # 为了保证成交，在K线收盘价上加5发出限价单
            price = bar.close_price + 5
            # 当前多头仓位，则直接开多
            if self.pos >= 0:
                self.buy(price, 1)
                print(self.pos, "buy")
                print(bar.datetime)
                print("当前多头仓位，则直接开多")
            # 当前持有空头仓位，则平空
            elif self.pos < 0:
                self.cover(price, 1)
                print(self.pos, "cover")
                print(bar.datetime)
                print("当前持有空头仓位，则平空")
        # 多头平仓
        elif sell_inform:
            price = bar.close_price - 5
            # 当前空头仓位，需平多单，不操作
            if self.pos <= 0:
                pass
                print(bar.datetime)
                print("当前空头仓位，需平多单，不操作")
            # 当前持有多头仓位，直接平多单
            elif self.pos > 0:
                self.sell(price, 1)
                print(self.pos, "sell")
                print(bar.datetime)
                print("当前持有多头仓位，直接平多单")
        # 卖出入信号
        elif short_inform:
            price = bar.close_price - 5
            # 当前空头仓位，则直接开空
            if self.pos <= 0:
                self.short(price, 1)
                print(self.pos,"short")
                print("当前空头仓位，则直接开空")
            # 当前持有多头仓位，则平多
            elif self.pos > 0:
                self.sell(price, 1)
                print(self.pos,"sell")
                print("当前持有多头仓位，则平多")
        # 空单平仓信号
        elif cover_inform == 1:
            price = bar.close_price + 5
            # 当前多头仓位，平空单，不操作
            if self.pos >= 0:
                pass
                print(bar.datetime)
                print("当前多头仓位，不操作")
            # 当前持有空头仓位，则平空
            elif self.pos < 0:
                self.cover(price, 1)
                print(self.pos, "cover")
                print(bar.datetime)
                print("当前持有空头仓位，则平空")

        self.put_event()

    def on_order(self, order: OrderData):
        """
        通过该函数收到委托状态更新推送。
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        通过该函数收到成交推送。
        """
        # 成交后策略逻辑仓位发生变化，需要通知界面更新。
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        通过该函数收到本地停止单推送。
        """
        pass
