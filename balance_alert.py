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
ADDR = os.getenv('ADDR')

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
                r = requests.get(f'https://kmd.explorer.dexstats.info/insight-api-komodo/addr/{ADDR}')
                resp = r.json()
                bal = resp['balance']
                if bal > 1000:
                    await channel.send(f"KMD address [{ADDR}] balance: {bal}")                
            except Exception as e:
                await channel.send(f"Balances endpoint not responding!\n{e}")
            # await asyncio.sleep(60*60*4) # task runs every 4 hrs
            await self.close() # or run once and cron


client = MyClient()
client.run(TOKEN)
