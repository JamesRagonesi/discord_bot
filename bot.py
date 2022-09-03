# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    # don't let the bot go crazy and talk to itself
    if message.author == client.user:
        return

    if message.content == 'sup':
        await message.channel.send('nmhjc')

client.run(TOKEN)
