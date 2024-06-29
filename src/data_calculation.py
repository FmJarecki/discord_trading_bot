import pandas as pd
import ta


def ta_rsi(df: pd.DataFrame, window_size: int = 14) -> pd.DataFrame:
    rsi = ta.momentum.RSIIndicator(close=df['c'], window=window_size).rsi()
    rsi = round(rsi, 2)
    df['ta_rsi'] = rsi
    return df


def pandas_rsi(df: pd.DataFrame, window_size: int = 14) -> pd.DataFrame:
    delta = df['c'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    average_gain = gain.rolling(window=window_size).mean()
    average_loss = loss.rolling(window=window_size).mean()

    rs = average_gain / average_loss.abs()
    rsi = 100 - (100 / (1 + rs))
    rsi = round(rsi, 2)
    df['pd_rsi'] = rsi
    return df
