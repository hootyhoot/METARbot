import requests
import json
import discord
import os
import discord.ext
from keep_alive import keep_alive
from discord.ext import commands

client = discord.Client(
    intents=discord.Intents(messages=True, message_content=True))


async def on_ready():
    print("bot online")  #will print bot online when booted up


@client.event
async def on_message(message):
    ##next change for nearest airport if airfield is valid but no available METAR
    channel = message.channel
    if message.content.startswith("*metar"):
        airport = message.content[7:11]
        hdr = {"X-API-Key": os.environ['checkWXkey']}
        req = requests.get(f"https://api.checkwx.com/metar/{airport}",
                           headers=hdr)

        try:
            req.raise_for_status()
            resp = json.loads(req.text)
            output = json.dumps(resp, indent=1)

        except requests.exceptions.HTTPError as e:
            print(e)

        cleanedOutput = output[31:-6]
        if len(cleanedOutput) > 0:
            await channel.send(
                f"Here's the METAR for {airport.upper()}: \n{cleanedOutput}")
        else:
            await channel.send(
                f"I'm sorry but '{airport.upper()}' is not a valid airfield. Please try again in this format '*metar (4 digit ICAO code)'"
            )


keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
