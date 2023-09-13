import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from dotenv import load_dotenv
import os
import lights_controller
import color

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = nextcord.Intents.default()

client = commands.Bot(intents=intents)


@client.event
async def on_ready():
    print("Bot is ready")


@client.slash_command(
    name="ping", description="Replies with the bot's ping to the server"
)
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"Ping: {round(client.latency*1000)}ms")


@client.slash_command(name="off", description="Turns the lights off")
async def off(interaction: Interaction):
    lights_controller.off()
    await interaction.response.send_message("Turned the lights off")


@client.slash_command(
    name="setall", description="Sets all the lights to the specified color"
)
async def setall(interaction: Interaction, color: str):
    lights_controller.setall(int(color))
    await interaction.response.send_message(f"Set all lights to {color}")


client.run(BOT_TOKEN)
