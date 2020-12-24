#!/usr/bin/env python3
import discord
import asyncio
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL = int(os.getenv('CHANNEL'))
TOKEN = os.getenv('TOKEN')
AUD_ALERT_PRICE = float(os.getenv('AUD_ALERT_PRICE'))
BTC_ALERT_PRICE = float(os.getenv('BTC_ALERT_PRICE'))

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(CHANNEL) # channel ID goes here
        while not self.is_closed():
            try:
                r = requests.get('https://api.coinpaprika.com/v1/tickers/kmd-komodo?quotes=AUD,BTC')
                resp = r.json()
                quotes = resp['quotes']
                aud_price = resp['quotes']['AUD']['price']
                btc_price = resp['quotes']['BTC']['price']
                if aud_price > AUD_ALERT_PRICE or btc_price > BTC_ALERT_PRICE:
                    await channel.send(f"KMD Price: ${aud_price} | {btc_price} BTC")
            except Exception as e:
                await channel.send(f"Prices endpoint not responding!\n{e}")
            # await asyncio.sleep(60*60*4) # task runs every 4 hrs
            await self.close() # or run once and cron


client = MyClient()
client.run(TOKEN)
