

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

class AverageStrategy(CtaTemplate):
    author = "Van"
    fast_window = 10
    slow_window = 20
    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0
    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

        def on_init(self):
            self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        self.write_log("策略停止")

        self.put_event()

    def on_tick(self, tick: TickData):
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        am = self.am
        # 更新K线到时间序列容器中
        am.update_bar(bar)
        # 若缓存的K线数量尚不够计算技术指标，则直接返回
        if not am.inited:
            return
        # 计算快速均线
        fast_ma = am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]  # T时刻数值
        self.fast_ma1 = fast_ma[-2]  # T-1时刻数值
        # 计算慢速均线
        slow_ma = am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]
        # 判断是否金叉
        cross_over = (self.fast_ma0 > self.slow_ma0 and
                      self.fast_ma1 < self.slow_ma1)
        # 判断是否死叉
        cross_below = (self.fast_ma0 < self.slow_ma0 and
                       self.fast_ma1 > self.slow_ma1)
        # 如果发生了金叉
        if cross_over:
            # 为了保证成交，在K线收盘价上加5发出限价单
            price = bar.close_price + 5
            # 当前无仓位，则直接开多
            if self.pos == 0:
                self.buy(price, 1)
            elif self.pos < 0:
                self.cover(price, 1)
                self.buy(price, 1)
        elif cross_below:
            price = bar.close_price - 5
            if self.pos == 0:
                self.short(price, 1)
            elif self.pos > 0:
                self.sell(price, 1)
                self.short(price, 1)
        self.put_event()

    def on_order(self, order: OrderData):
        pass

    def on_trade(self, trade: TradeData):
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        pass
