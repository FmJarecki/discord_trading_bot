from discord_handler import DiscordClient

if __name__ == '__main__':
    dsc_client = DiscordClient('SOLUSDT', '1h')
    dsc_client.bot_run()
