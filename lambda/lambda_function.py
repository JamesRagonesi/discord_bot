import xml.etree.ElementTree as ET
import discord
from discord.ext import commands
import os
import asyncio

videos = set()
client = discord.Client()

TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_ENABLED = os.getenv('DISCORD_ENABLED', default=False)

async def postNewTrashTalkVideo():
    await client.wait_until_ready()

    #id for general channel
    channel = client.get_channel(id=1015401006575652980)

    for video in videos:
        await channel.send(f"New trash talk uploaded! {video}")
        print(f"New trash talk uploaded! {video}")

    await client.close()

def lambda_handler(event, context):
    print(event)

    if(event.get('headers', {}).get('from', '') == 'googlebot(at)googlebot.com'):
        # need this to refresh subscription every so often
        if(event.get('queryStringParameters', {}).get('hub.challenge', False)):
            challengeCode = event.get('queryStringParameters').get('hub.challenge');
            print(f"found hub.challenge {challengeCode}")
            return challengeCode


        elif('body' in event):
            try:
                ns = {'Atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
                root = ET.fromstring(event['body'])

                print("parsing video url from xml doc")
                for entry in root.findall('Atom:entry', ns):
                    videos.add(entry.find('Atom:link', ns).attrib['href'])

                if(len(videos) > 0):
                    if(DISCORD_ENABLED):
                        client.loop.create_task(postNewTrashTalkVideo())
                        client.run(TOKEN)
                    else:
                        print("New trash talk but discord is disabled")
                else:
                    print("no new videos found :(")
            except:
                print("unsupported body")
        else:
            print("unsupported googlebot event")
    else:
        print("unknown and unsupported event")

    return "200"
