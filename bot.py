# bot.py
import os
import fantasy_api

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
    print(f'received message {message.content}')

    # don't let the bot go crazy and talk to itself
    if message.author == client.user:
        return
    elif message.content is not None and '@1015369557701050478' not in message.content:
        return

    if 'sup' in message.content.lower():
        await message.channel.send('nmhjc')

    if 'power rankings' in message.content.lower():
        print(f'calculating power rankings')
        powerRankings = fantasy_api.getPowerRankings()
        await message.channel.send(powerRankings)

    if message.content is not None and 'league' in message.content:
        league_info = fantasy_api.get_league()
        await message.channel.send(league_info)
    else:
        pass

client.run(TOKEN)
