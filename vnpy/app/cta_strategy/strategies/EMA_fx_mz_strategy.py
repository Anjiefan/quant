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
    EMA = 10
    slow_window = 20
    # 定义变量
    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0
    buy_price = 0.0
    sell_price = 0.0
    # 添加参数和变量名到对应的列表
    parameters = ["slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # K线合成器：从Tick合成分钟K线用
        self.bg = BarGenerator(self.on_bar)

        # 时间序列容器：计算技术指标用
        self.am = GanManager(size=40)

    def on_init(self):
        """
        当策略被初始化时调用该函数。
        """
        # 输出个日志信息，下同
        self.write_log("策略初始化")

        # 加载10天的历史数据用于初始化回放
        self.load_bar(10)

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
        # self.cta_engine.main_engine.get_account('1')
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        通过该函数收到本地停止单推送。
        """
        pass

    def calculate_statistics(self, df: DataFrame = None, output=True):
        """"""
        self.output("开始计算策略统计指标")

        # Check DataFrame input exterior
        if df is None:
            df = self.daily_df

        # Check for init DataFrame
        if df is None:
            # Set all statistics to 0 if no trade.
            start_date = ""
            end_date = ""
            total_days = 0
            profit_days = 0
            loss_days = 0
            end_balance = 0
            max_drawdown = 0
            max_ddpercent = 0
            max_drawdown_duration = 0
            total_net_pnl = 0
            daily_net_pnl = 0
            total_commission = 0
            daily_commission = 0
            total_slippage = 0
            daily_slippage = 0
            total_turnover = 0
            daily_turnover = 0
            total_trade_count = 0
            daily_trade_count = 0
            total_return = 0
            annual_return = 0
            daily_return = 0
            return_std = 0
            sharpe_ratio = 0
            return_drawdown_ratio = 0
        else:
            # Calculate balance related time series data
            df["balance"] = df["net_pnl"].cumsum() + self.capital
            df["return"] = np.log(df["balance"] / df["balance"].shift(1)).fillna(0)
            df["highlevel"] = (
                df["balance"].rolling(
                    min_periods=1, window=len(df), center=False).max()
            )
            df["drawdown"] = df["balance"] - df["highlevel"]
            df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

            # Calculate statistics value
            start_date = df.index[0]
            end_date = df.index[-1]

            total_days = len(df)
            profit_days = len(df[df["net_pnl"] > 0])
            loss_days = len(df[df["net_pnl"] < 0])

            end_balance = df["balance"].iloc[-1]
            max_drawdown = df["drawdown"].min()
            max_ddpercent = df["ddpercent"].min()
            max_drawdown_end = df["drawdown"].idxmin()

            if isinstance(max_drawdown_end, date):
                max_drawdown_start = df["balance"][:max_drawdown_end].idxmax()
                max_drawdown_duration = (max_drawdown_end - max_drawdown_start).days
            else:
                max_drawdown_duration = 0

            total_net_pnl = df["net_pnl"].sum()
            daily_net_pnl = total_net_pnl / total_days

            total_commission = df["commission"].sum()
            daily_commission = total_commission / total_days

            total_slippage = df["slippage"].sum()
            daily_slippage = total_slippage / total_days

            total_turnover = df["turnover"].sum()
            daily_turnover = total_turnover / total_days

            total_trade_count = df["trade_count"].sum()
            daily_trade_count = total_trade_count / total_days

            total_return = (end_balance / self.capital - 1) * 100
            annual_return = total_return / total_days * 240
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            if return_std:
                sharpe_ratio = daily_return / return_std * np.sqrt(240)
            else:
                sharpe_ratio = 0

            return_drawdown_ratio = -total_return / max_ddpercent

        # Output
        if output:
            self.output("-" * 30)
            self.output(f"首个交易日：\t{start_date}")
            self.output(f"最后交易日：\t{end_date}")

            self.output(f"总交易日：\t{total_days}")
            self.output(f"盈利交易日：\t{profit_days}")
            self.output(f"亏损交易日：\t{loss_days}")

            self.output(f"起始资金：\t{self.capital:,.2f}")
            self.output(f"结束资金：\t{end_balance:,.2f}")

            self.output(f"总收益率：\t{total_return:,.2f}%")
            self.output(f"年化收益：\t{annual_return:,.2f}%")
            self.output(f"最大回撤: \t{max_drawdown:,.2f}")
            self.output(f"百分比最大回撤: {max_ddpercent:,.2f}%")
            self.output(f"最长回撤天数: \t{max_drawdown_duration}")

            self.output(f"总盈亏：\t{total_net_pnl:,.2f}")
            self.output(f"总手续费：\t{total_commission:,.2f}")
            self.output(f"总滑点：\t{total_slippage:,.2f}")
            self.output(f"总成交金额：\t{total_turnover:,.2f}")
            self.output(f"总成交笔数：\t{total_trade_count}")

            self.output(f"日均盈亏：\t{daily_net_pnl:,.2f}")
            self.output(f"日均手续费：\t{daily_commission:,.2f}")
            self.output(f"日均滑点：\t{daily_slippage:,.2f}")
            self.output(f"日均成交金额：\t{daily_turnover:,.2f}")
            self.output(f"日均成交笔数：\t{daily_trade_count}")

            self.output(f"日均收益率：\t{daily_return:,.2f}%")
            self.output(f"收益标准差：\t{return_std:,.2f}%")
            self.output(f"Sharpe Ratio：\t{sharpe_ratio:,.2f}")
            self.output(f"收益回撤比：\t{return_drawdown_ratio:,.2f}")

        statistics = {
            "start_date": start_date,
            "end_date": end_date,
            "total_days": total_days,
            "profit_days": profit_days,
            "loss_days": loss_days,
            "capital": self.capital,
            "end_balance": end_balance,
            "max_drawdown": max_drawdown,
            "max_ddpercent": max_ddpercent,
            "max_drawdown_duration": max_drawdown_duration,
            "total_net_pnl": total_net_pnl,
            "daily_net_pnl": daily_net_pnl,
            "total_commission": total_commission,
            "daily_commission": daily_commission,
            "total_slippage": total_slippage,
            "daily_slippage": daily_slippage,
            "total_turnover": total_turnover,
            "daily_turnover": daily_turnover,
            "total_trade_count": total_trade_count,
            "daily_trade_count": daily_trade_count,
            "total_return": total_return,
            "annual_return": annual_return,
            "daily_return": daily_return,
            "return_std": return_std,
            "sharpe_ratio": sharpe_ratio,
            "return_drawdown_ratio": return_drawdown_ratio,
        }

        # Filter potential error infinite value
        for key, value in statistics.items():
            if value in (np.inf, -np.inf):
                value = 0
            statistics[key] = np.nan_to_num(value)

        self.output("策略统计指标计算完成")
        return statistics