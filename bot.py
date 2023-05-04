# bot.py
import os
import shlex
import fantasy_api
import db
import datetime
from pytz import timezone

import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

keywords = {
    "vfl": "Burn the VFL to the ground!",
    "ridder": "My leaguemate Ben, he shows his Ridder to my other leaguemate Phil, and he says, \"You will never get this! You will never get this! La la la la la!\""
}

# ensure db is ready to go
keywords.update(db.init())

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    countdown.start()

@client.event
async def on_message(message):
    print(f'received message {message.content} {message.channel}')
    lowercase_words = message.content.lower().split()

    # don't let the bot go crazy and talk to itself
    if message.author == client.user:
        return

    for key in keywords:
        if key in lowercase_words:
            await message.channel.send(keywords[key])

    if message.content is not None and '@1015369557701050478' not in message.content:
        return

    if 'sup' in lowercase_words:
        await message.channel.send('nmhjc')

    elif 'rankings' in lowercase_words:
        print('calculating power rankings')
        powerRankings = fantasy_api.getPowerRankings()
        await message.channel.send(powerRankings)

    elif 'league' in lowercase_words:
        league_info = fantasy_api.get_league()
        await message.channel.send(league_info)

    else:
        ops = shlex.split(message.content.lower().strip('||'))
        if('add' == ops[1]):
            try:
                key = ops[2].replace(" ", "")

                if key in keywords:
                    await message.channel.send("This trigger word already exists. Let's play nicely.")
                    return

                val = ops[3]
                print(f'adding a new keyword "{key}" to db with value "{val}"')
                db.insert(key, val)
                keywords[key] = val
                print(keywords)
            except:
                await message.channel.send('''
                    USAGE: @Feldkamp-Ragonesi Trophy Bot add "trigger word(s)" "response word(s)"
                ''')

@tasks.loop(time=datetime.time(hour=15, minute=0))
# @tasks.loop(seconds=5.0)
async def countdown():
    message_channel = client.get_channel(954049443299205234)

    today = datetime.date.today()
    future = datetime.date(2023,8,5)
    diff = (future - today).days

    await message_channel.send(f'Only {diff} more day(s) until the DWO draft!!!!')

@countdown.before_loop
async def before_countdown():
    await client.wait_until_ready()
    print('client is ready...')

client.run(TOKEN)
