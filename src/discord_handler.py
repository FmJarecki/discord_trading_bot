from config import DISCORD_TOKEN, DISCORD_CHANNEL_ID
import discord
from data_fetcher import ByBitFetcher
import asyncio


class DiscordClient(discord.Client):
    def __init__(self, symbol: str, interval: str):
        super().__init__(intents=discord.Intents.default())
        self._channel = None
        self._bg_task = None
        self._data_fetcher = ByBitFetcher(symbol, interval)
        self.frequency = self._data_fetcher.interval

    def bot_run(self):
        self.run(DISCORD_TOKEN)

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        self._channel = self.get_channel(DISCORD_CHANNEL_ID)
        self._bg_task = self.loop.create_task(self.send_message_periodically())

    async def send_message_periodically(self):
        while True:
            rsi = self._data_fetcher.get_actual_rsi()
            if rsi > 70.0 or rsi < 30.0:
                await self._channel.send(f'Current RSI value: {rsi}')
            await asyncio.sleep(self._frequency)

    @property
    def frequency(self) -> int:
        return self._frequency

    @frequency.setter
    def frequency(self, value: str):
        interval_data = {
            '1m': 1*60,
            '3m': 3*60,
            '5m': 5*60,
            '15m': 15*60,
            '30m': 30*60,
            '1h': 60*60,
            '2h': 2*60*60,
            '4h': 4*60*60,
            '6h': 6*60*60,
            '12h': 12*60*60,
            '1d': 24*60*60,
            '1w': 7*24*60*60,
            '1M': 30*7*24*60*60
        }
        self._frequency = interval_data[value]
