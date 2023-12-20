import pandas as pd
from tradingview_screener import Query, Column
from tradingview_screener.constants import COLUMNS

# ==== TradingView ====


def get_all_tradingview_tickers() -> pd.Series:
    total_n, _ = Query().select().limit(1).get_scanner_data()
    _, df = Query().select().limit(total_n).get_scanner_data()
    return df["ticker"]
