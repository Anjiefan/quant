from trader.setting import get_settings

if __name__ == '__main__':
    from vnpy.app.cta_strategy.backtesting import BacktestingEngine, OptimizationSetting
    from celue.fx.ema_k_strategy import (
        EmaKMzStrategy,
    )
    from datetime import datetime

    engine = BacktestingEngine()
    engine.set_parameters(
        vt_symbol="BTCUSDT.BINANCE",
        interval="d",
        start=datetime(2020, 3, 1),
        end=datetime(2020, 4, 30),
        rate=0.3 / 10000,
        slippage=0.2,
        size=300,
        pricetick=0.2,
        capital=1_000_000,
    )
    engine.add_strategy(EmaKMzStrategy, {})
    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    engine.calculate_statistics()
