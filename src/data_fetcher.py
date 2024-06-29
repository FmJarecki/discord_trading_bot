import requests
import json
import pandas as pd
from data_calculation import ta_rsi, pandas_rsi
import datetime as dt


class ByBitFetcher:
    def __init__(self, symbol: str, interval: str):
        self._url = "https://api.bybit.com/spot/v3/public/quote/kline"
        self.symbol = symbol
        self.interval = interval

    def get_actual_rsi(self) -> float:
        window_size = 14
        df = self._get_bybit_bars(window_size)
        df['c'] = df['c'].astype(float)
        df = ta_rsi(df, window_size)
        df = pandas_rsi(df, window_size)
        rsi = df.iloc[-1]['ta_rsi']
        rsi = float(rsi)
        return rsi

    def _get_bybit_bars(self, limit: int = 1, end_time: dt.datetime = dt.datetime.now().timestamp()) -> pd.DataFrame:
        end_time = int(end_time) * 1000
        req_params = {'symbol': self._symbol, 'interval': self._interval, 'limit': limit, 'endTime': end_time}
        req = requests.get(self._url, params=req_params)
        data = json.loads(req.text)['result']['list']
        df = pd.DataFrame(data)
        df['t_date'] = pd.to_datetime(df['t'] / 1000, unit='s')
        return df

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        self._symbol = value

    @property
    def interval(self) -> str:
        return self._interval

    @interval.setter
    def interval(self, value: str):
        self._interval = value
