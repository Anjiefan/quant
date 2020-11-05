
if __name__ == '__main__':
    from vnpy.app.cta_strategy.backtesting import BacktestingEngine, OptimizationSetting
    from vnpy.app.cta_strategy.strategies.average_strategy import AverageStrategy
    from vnpy.app.cta_strategy.strategies.boll_channel_strategy import BollChannelStrategy
    from datetime import datetime

    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol="BTCUSDT.BINANCE",
        interval="1m",
        start=datetime(2020, 1, 1),
        end=datetime(2020, 11, 1),
        rate=0.3 / 10000,
        slippage=0.2,
        size=100,
        pricetick=0.2,
        capital=1000000,
    )
    engine.add_strategy(AverageStrategy, {})

    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    engine.calculate_statistics()
    engine.show_chart()