# bot.py
import os
import fantasy_api

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

keywords = {
    "vfl": "Burn the VFL to the ground!",
    "armtalent": "Trevor Lawrence is the greatest quarterback of all time",
    "mikewhite": "Mike White. Mike White. Mike White. https://pbs.twimg.com/media/FimZOxHWYAAxShx.jpg",
    "jamaal": "He's a touchdown machine!!",
    "williams": "Williams? Jamaal Williams is a touchdown machine!!",
    "ridder": "My leaguemate Ben, he shows his Ridder to my other leaguemate Phil, and he says, \"You will never get this! You will never get this! La la la la la!\""
}

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    print(f'received message {message.content}')

    # don't let the bot go crazy and talk to itself
    if message.author == client.user:
        return

    for key in keywords:
        if key in message.content.lower().replace(" ", ""):
            await message.channel.send(keywords[key])
            return

    if message.content is not None and '@1015369557701050478' not in message.content:
        return

    if 'sup' in message.content.lower():
        await message.channel.send('nmhjc')

    if 'rankings' in message.content.lower():
        print(f'calculating power rankings')
        powerRankings = fantasy_api.getPowerRankings()
        await message.channel.send(powerRankings)

    if message.content is not None and 'league' in message.content:
        league_info = fantasy_api.get_league()
        await message.channel.send(league_info)
    else:
        pass

client.run(TOKEN)
