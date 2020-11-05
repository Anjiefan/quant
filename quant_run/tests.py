from trader.constant import Interval

if __name__ == '__main__':
    from vnpy.app.cta_strategy.backtesting import BacktestingEngine
    from vnpy.app.cta_strategy.strategies.fx_strategy import FxStrategy
    from vnpy.app.cta_strategy.strategies.average_strategy import AverageStrategy
    from datetime import datetime
    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol="BTCUSDT.BINANCE",
        interval=Interval.HOUR.value,
        start=datetime(2020, 1, 1),
        end=datetime(2020, 11, 1),
        rate=0,
        slippage=0,
        size=100,
        pricetick=0.2,
        capital=1000000,
    )
    engine.add_strategy(FxStrategy, {})
    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    engine.calculate_statistics()
    engine.show_chart()