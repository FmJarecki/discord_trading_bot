# discord_trading_bot
Reading the value from the stock, calculating the RSI and publishing it on the discord channel if value is < 30 or > 70.


# How to use
- Visit the site https://discord.com/developers/applications to create yor bot (you need DISCORD_TOKEN)
- Connect your bot to your discord channel (you need DISCORD_CHANNEL_ID)
- Prepare config.py and fill with data
- In main.py you can write stock pair which you are interested in + time interval
- Build Docker container with "docker build -t image_name ." and then run it with "docker run -d image_name"
- Congrats! Now your app is working in the background. :)
