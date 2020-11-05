from trader.setting import get_settings

if __name__ == '__main__':
    from vnpy.app.cta_strategy.backtesting import BacktestingEngine, OptimizationSetting
    from celue.fx.fx_mz_strategy import (
        FxMzStrategy,
    )
    from datetime import datetime

    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol="BTCUSDT.BINANCE",
        interval="d",
        start=datetime(2019, 1, 1),
        end=datetime(2020, 11, 1),
        rate=0.3 / 10000,
        slippage=0.2,
        size=100,
        pricetick=0.2,
        capital=1_000_000,
    )
    engine.add_strategy(FxMzStrategy, {})
    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    engine.calculate_statistics()
    engine.show_chart()