from app.data_manager import DataManagerApp
from app.data_recorder import DataRecorderApp
from app.excel_rtd import ExcelRtdApp
from app.spread_trading import SpreadTradingApp
from gateway.bitstamp import BitstampGateway
from vnpy.event import EventEngine
from vnpy.gateway.binance import BinanceGateway
from vnpy.gateway.binances import BinancesGateway
from vnpy.gateway.bitmex import BitmexGateway
from vnpy.gateway.huobi import HuobiGateway
from vnpy.gateway.huobif import HuobifGateway
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy.gateway.okex import OkexGateway
from vnpy.app.cta_backtester import CtaBacktesterApp
from vnpy.app.cta_strategy import CtaStrategyApp


def main():
    """Start VN Trader"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(BinanceGateway)
    main_engine.add_gateway(HuobiGateway)
    main_engine.add_gateway(HuobifGateway)
    main_engine.add_gateway(BinancesGateway)
    main_engine.add_gateway(BitmexGateway)
    main_engine.add_gateway(OkexGateway)
    main_engine.add_gateway(BitstampGateway)

    main_engine.add_app(ExcelRtdApp)
    main_engine.add_app(DataRecorderApp)
    main_engine.add_app(DataManagerApp)
    main_engine.add_app(CtaBacktesterApp)
    main_engine.add_app(SpreadTradingApp)
    main_engine.add_app(CtaStrategyApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
