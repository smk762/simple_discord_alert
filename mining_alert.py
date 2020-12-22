import discord
import asyncio
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL = int(os.getenv('CHANNEL'))
TOKEN = os.getenv('TOKEN')

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
                r = requests.get('http://116.203.120.91:8762/api/nn_mined_4hrs_count/')
                resp = r.json()
                nn_list = resp.keys()
                no_mine_list = []
                for nn in nn_list:
                    if resp[nn] == 0:
                        no_mine_list.append(nn)
                await channel.send(f"In the last 4 hours, {no_mine_list} have not mined any blocks!")
            except Exception as e:
                await channel.send(f"Mining endpoint not responding!\n{e}")
            # await asyncio.sleep(60*60*4) # task runs every 4 hrs
            await self.close() # or run once and cron


client = MyClient()
client.run(TOKEN)
