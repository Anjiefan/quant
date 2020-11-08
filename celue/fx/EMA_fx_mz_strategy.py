from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)
from vnpy.trader.utility import GanManager


class EmaFxMzStrategy(CtaTemplate):
    """演示用的简单双均线"""

    # 策略作者
    author = "Smart Trader"

    # 定义参数
    EMA = 15
    slow_window = 20

    # 定义变量
    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0
    buy_price = 0.0
    sell_price = 0.0
    # 添加参数和变量名到对应的列表
    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # K线合成器：从Tick合成分钟K线用
        self.bg = BarGenerator(self.on_bar)

        # 时间序列容器：计算技术指标用
        self.am = GanManager(size=self.EMA)

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
        up_fx = am.up_fx()
        down_fx = am.down_fx()
        up_mz = am.up_mz()
        down_mz = am.down_mz()
        # 卖出入信号
        if up_fx != 0:
            short_inform = True
        else:
            short_inform = False
        # 买入信号
        if down_fx != 0:
            buy_inform = True
            if short_inform:
                buy_inform = False
                short_inform = False
        else:
            buy_inform = False

        # 平仓信号
        if up_mz != 0:
            cover_inform = True
        else:
            cover_inform = False
        if down_mz != 0:
            sell_inform = True
        else:
            sell_inform = False

        ###################################################################
        # 交易池子
        # 多头交易
        if buy_inform:
            # 为了保证成交，在K线收盘价上加5发出限价单
            price = bar.close_price + 5
            # 当前多头仓位，则直接开多
            if self.pos >= 0:
                self.buy(price, 1)
                print(1)
                print(bar.datetime)
                print("当前多头仓位，则直接开多")
            # 当前持有空头仓位，则平空
            elif self.pos < 0:
                self.cover(price, 1)
                print(1)
                print(bar.datetime)
                print("当前持有空头仓位，则平空")
        # 多头平仓
        elif sell_inform:
            price = bar.close_price - 5
            # 当前空头仓位，需平多单，不操作
            if self.pos <= 0:
                pass
                print(2)
                print(bar.datetime)
                print("当前空头仓位，需平多单，不操作")
            # 当前持有多头仓位，直接平多单
            elif self.pos > 0:
                self.sell(price, 1)
                print(2)
                print(bar.datetime)
                print("当前持有多头仓位，直接平多单")
        # 空头开仓交易
        elif short_inform:
            price = bar.close_price - 5
            # 当前空头仓位，则直接开空
            if self.pos <= 0:
                self.short(price, 1)
                print(3)
                print("当前空头仓位，则直接开空")
            # 当前持有多头仓位，则平多
            elif self.pos > 0:
                self.sell(price, 1)
                print(3)
                print("当前持有多头仓位，则平多")

        elif cover_inform:

            price = bar.close_price + 5
            # 当前多头仓位，平空单，不操作
            if self.pos >= 0:
                pass
                print(4)
                print(bar.datetime)
                print("当前多头仓位，不操作")
            # 当前持有空头仓位，则平空
            elif self.pos < 0:
                self.cover(price, 1)
                print(4)
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