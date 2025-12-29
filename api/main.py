import requests
import json
import discord
import os
from index import keep_alive
from discord import app_commands

# Create client with minimal intents (no privileged intents needed)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("bot online")
    # Sync slash commands with Discord
    await tree.sync()
    print("slash commands synced")


@tree.command(name="metar", description="Get METAR data for an airport")
@app_commands.describe(icao="4-letter ICAO airport code (e.g., KJFK)")
async def metar(interaction: discord.Interaction, icao: str):
    # Defer the response since API call might take a moment
    await interaction.response.defer()

    # Validate ICAO code length
    airport = icao.strip()[:4]

    hdr = {"X-API-Key": os.environ['checkWXkey']}
    req = requests.get(f"https://api.checkwx.com/metar/{airport}",
                       headers=hdr)

    try:
        req.raise_for_status()
        resp = json.loads(req.text)
        output = json.dumps(resp, indent=1)

    except requests.exceptions.HTTPError as e:
        print(e)
        await interaction.followup.send(
            f"Error retrieving METAR data for '{airport.upper()}'. Please try again later."
        )
        return

    cleanedOutput = output[31:-6]
    if len(cleanedOutput) > 0:
        await interaction.followup.send(
            f"Here's the METAR for {airport.upper()}: \n{cleanedOutput}")
    else:
        await interaction.followup.send(
            f"I'm sorry but '{airport.upper()}' is not a valid airfield. Please provide a valid 4-letter ICAO code."
        )


keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
