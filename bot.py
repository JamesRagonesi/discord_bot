# bot.py
import os
import shlex
import fantasy_api
import db

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

keywords = {
    "vfl": "Burn the VFL to the ground!",
    "ridder": "My leaguemate Ben, he shows his Ridder to my other leaguemate Phil, and he says, \"You will never get this! You will never get this! La la la la la!\""
}

# ensure db is ready to go
keywords.update(db.init())

print(keywords)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    print(f'received message {message.content}')
    lowercase_message = message.content.lower()

    # don't let the bot go crazy and talk to itself
    if message.author == client.user:
        return

    for key in keywords:
        if key in lowercase_message.replace(" ", ""):
            await message.channel.send(keywords[key])

    if message.content is not None and '@1015369557701050478' not in message.content:
        return

    if 'sup' in lowercase_message:
        await message.channel.send('nmhjc')

    elif 'rankings' in lowercase_message:
        print('calculating power rankings')
        powerRankings = fantasy_api.getPowerRankings()
        await message.channel.send(powerRankings)

    elif 'league' in lowercase_message:
        league_info = fantasy_api.get_league()
        await message.channel.send(league_info)

    else:
        ops = shlex.split(lowercase_message.strip('||'))
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

client.run(TOKEN)
