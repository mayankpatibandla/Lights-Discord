import os

from dotenv import load_dotenv
from lights_controller import lights
from nextcord import Intents, Interaction
from nextcord.ext import commands

from color_utils import parse_color

print("Loading Bot")
bot = commands.Bot(intents=Intents.default())


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.slash_command(name="ping", description="Replies with the bot's ping to the server")
async def slash_command_ping(interaction: Interaction):
    await interaction.response.send_message(f"Ping: `{round(bot.latency * 1000)} ms`")


@bot.slash_command(name="off", description="Turns the lights off")
async def slash_command_off(interaction: Interaction):
    lights[:] = 0
    lights.update()
    await interaction.response.send_message("Turned the lights off")


@bot.slash_command(name="set", description="Sets the specified light to the specified color")
async def slash_command_set(interaction: Interaction, index: int = 0, color: str = "0"):
    try:
        parsed_color = parse_color(color)
    except ValueError as err:
        await interaction.response.send_message(str(err))
    else:
        lights[index] = parsed_color
        lights.update()
        await interaction.response.send_message(f"Set light at index `{index}` to `{color}`")


@bot.slash_command(name="setall", description="Sets all the lights to the specified color")
async def slash_command_setall(interaction: Interaction, color: str = "0"):
    try:
        parsed_color = parse_color(color)
    except ValueError as err:
        await interaction.response.send_message(str(err))
    else:
        lights[:] = parsed_color
        lights.update()
        await interaction.response.send_message(f"Set all lights to `{color}`")


@bot.slash_command(
    name="setrange",
    description="Sets all lights in the range to the specified color",
)
async def slash_command_setrange(
    interaction: Interaction,
    start: int = 0,
    stop: int = len(lights),
    color: str = "0",
):
    try:
        parsed_color = parse_color(color)
    except ValueError as err:
        await interaction.response.send_message(str(err))
    else:
        lights[start:stop] = parsed_color
        lights.update()
        await interaction.response.send_message(f"Set lights in range `{start}` to `{stop}` to `{color}`")


@bot.slash_command(
    name="setslice",
    description="Sets all lights in the slice to the specified color",
)
async def slash_command_setslice(
    interaction: Interaction,
    start: int = 0,
    stop: int = len(lights),
    step: int = 1,
    color: str = "0",
):
    try:
        parsed_color = parse_color(color)
    except ValueError as err:
        await interaction.response.send_message(str(err))
    else:
        lights[start:stop:step] = parsed_color
        lights.update()
        await interaction.response.send_message(
            f"Set lights in slice `{start}` to `{stop}` with step size `{step}` to `{color}`"
        )


@bot.slash_command(
    name="brightness",
    description="Sets the brightness of the lights",
)
async def slash_command_brightness(
    interaction: Interaction,
    brightness: int = 255,
):
    lights.set_brightness(brightness)
    lights.update()
    await interaction.response.send_message(f"Set brightness to `{brightness}`")


load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))
