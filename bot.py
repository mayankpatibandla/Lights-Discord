import os

import color_utils
import nextcord
from dotenv import load_dotenv
from lights_controller import lights
from nextcord import Interaction
from nextcord.ext import commands

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = nextcord.Intents.default()

bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.slash_command(name="ping", description="Replies with the bot's ping to the server")
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"Ping: {round(bot.latency * 1000)}ms")


@bot.slash_command(name="off", description="Turns the lights off")
async def off(interaction: Interaction):
    lights[:] = 0
    lights.update()
    await interaction.response.send_message("Turned the lights off")


@bot.slash_command(
    name="setall", description="Sets all the lights to the specified color"
)
async def setall(interaction: Interaction, color: str):
    try:
        parsed_color = color_utils.parse_color(color)
    except ValueError:
        await interaction.response.send_message(f"`{color}` is an invalid input")
    else:
        lights[:] = parsed_color
        lights.update()
        await interaction.response.send_message(f"Set all lights to `{color}`")


bot.run(BOT_TOKEN)
