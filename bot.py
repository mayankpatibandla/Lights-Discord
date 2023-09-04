import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from dotenv import load_dotenv
import os

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


client.run(BOT_TOKEN)
