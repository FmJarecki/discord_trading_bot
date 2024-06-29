import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import datetime as dt
from src.data_fetcher import ByBitFetcher

mock_data = pd.DataFrame({
        't': [1719608400000, 1719612000000, 1719615600000, 1719619200000, 1719622800000,
              1719626400000, 1719630000000, 1719633600000, 1719637200000, 1719640800000,
              1719644400000, 1719648000000, 1719651600000, 1719655200000],
        'c': [100.0, 90.0, 100.0, 90.0, 100.0,
              90.0, 100.0, 90.0, 100.0, 90.0,
              100.0, 90.0, 100.0, 90.0]
    })


@pytest.fixture
def fetcher():
    symbol = 'BTCUSDT'
    interval = '1h'
    return ByBitFetcher(symbol, interval)


@patch.object(ByBitFetcher, '_get_bybit_bars')
def test_get_actual_rsi(mock_get_bybit_bars, fetcher):
    mock_get_bybit_bars.return_value = mock_data

    rsi = fetcher.get_actual_rsi()

    delta = mock_data['c'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    average_gain = gain.rolling(window=14).mean()
    average_loss = loss.rolling(window=14).mean()
    rs = average_gain / average_loss.abs()
    rsi_pd = 100 - (100 / (1 + rs))

    assert abs(rsi - rsi_pd.iloc[-1]) < 10
    mock_get_bybit_bars.assert_called_once()


@patch('src.data_fetcher.requests.get')
def test_get_bybit_bars(mock_get, fetcher):
    mock_response = MagicMock()
    mock_response.text = '{"retCode":0,"retMsg":"OK","result":{"list":[{"t":1719688860000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.89","h":"141.99","l":"141.88","o":"141.96","v":"384.605"},{"t":1719689040000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.79","h":"141.89","l":"141.79","o":"141.89","v":"544.224"},{"t":1719689220000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.62","h":"141.79","l":"141.62","o":"141.79","v":"970.679"},{"t":1719689400000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.33","h":"141.62","l":"141.18","o":"141.62","v":"3407.135"},{"t":1719689580000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.12","h":"141.35","l":"140.88","o":"141.33","v":"3396.145"},{"t":1719689760000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.24","h":"141.24","l":"141.05","o":"141.12","v":"999.951"},{"t":1719689940000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.39","h":"141.47","l":"141.24","o":"141.24","v":"816.599"},{"t":1719690120000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.56","h":"141.57","l":"141.39","o":"141.39","v":"530.308"},{"t":1719690300000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.47","h":"141.56","l":"141.42","o":"141.56","v":"419.454"},{"t":1719690480000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.54","h":"141.59","l":"141.46","o":"141.47","v":"365.28"},{"t":1719690660000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.69","h":"141.73","l":"141.47","o":"141.54","v":"421.624"},{"t":1719690840000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.7","h":"141.79","l":"141.69","o":"141.69","v":"212.563"},{"t":1719691020000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.71","h":"141.75","l":"141.68","o":"141.7","v":"464.672"},{"t":1719691200000,"s":"SOLUSDT","sn":"SOLUSDT","c":"141.57","h":"141.72","l":"141.56","o":"141.71","v":"143.104"}]},"retExtInfo":{},"time":1719691240794}'
    mock_get.return_value = mock_response

    df = fetcher._get_bybit_bars(limit=14, end_time=dt.datetime(2023, 6, 29).timestamp())

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 14
    assert 't' in df.columns and 'c' in df.columns
    assert not df.empty
    assert 't_date' in df.columns
    assert df.iloc[0]['t_date'] == pd.to_datetime(1719688860000 / 1000, unit='s')
    mock_get.assert_called_once()


def test_symbol_property(fetcher):
    assert fetcher.symbol == "BTCUSDT"
    fetcher.symbol = "ETHUSDT"
    assert fetcher.symbol == "ETHUSDT"


def test_interval_property(fetcher):
    assert fetcher.interval == "1h"
    fetcher.interval = "5m"
    assert fetcher.interval == "5m"
