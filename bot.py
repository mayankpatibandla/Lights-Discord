import color_utils
import nextcord
import os
from dotenv import load_dotenv
from lights_controller import lights
from nextcord import Interaction
from nextcord.ext import commands

print("Loading Bot")

bot = commands.Bot(intents=nextcord.Intents.default())


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.slash_command(name="ping", description="Replies with the bot's ping to the server")
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"Ping: `{round(bot.latency * 1000)} ms`")


@bot.slash_command(name="off", description="Turns the lights off")
async def off(interaction: Interaction):
    lights[:] = 0
    lights.update()
    await interaction.response.send_message("Turned the lights off")


@bot.slash_command(
    name="set", description="Sets the specified light to the specified color"
)
async def set(interaction: Interaction, index: int, color: str):
    try:
        parsed_color = color_utils.parse_color(color)
    except ValueError:
        await interaction.response.send_message(f"`{color}` is an invalid input")
    else:
        lights[index] = parsed_color
        lights.update()
        await interaction.response.send_message(
            f"Set light at index `{index}` to `{color}`"
        )


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


@bot.slash_command(
    name="setrange", description="Sets all lights in the range to the specified color"
)
async def setrange(interaction: Interaction, start: int, stop: int, color: str):
    try:
        parsed_color = color_utils.parse_color(color)
    except ValueError:
        await interaction.response.send_message(f"`{color}` is an invalid input")
    else:
        lights[start:stop] = parsed_color
        lights.update()
        await interaction.response.send_message(
            f"Set lights in range `{start}` to `{stop}` to `{color}`"
        )


@bot.slash_command(
    name="setslice", description="Sets all lights in the slice to the specified color"
)
async def setslice(
    interaction: Interaction, start: int, stop: int, step: int, color: str
):
    try:
        parsed_color = color_utils.parse_color(color)
    except ValueError:
        await interaction.response.send_message(f"`{color}` is an invalid input")
    else:
        lights[start:stop:step] = parsed_color
        lights.update()
        await interaction.response.send_message(
            f"Set lights in slice `{start}` to `{stop}` with step size `{step}` to `{color}`"
        )


load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))
