import os

import lights_controller as lc
from dotenv import load_dotenv
from nextcord import Intents, Interaction
from nextcord.ext import commands

from color_utils import format_color, parse_color

print("Loading Bot")
bot = commands.Bot(intents=Intents.default())


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.slash_command(
    name="ping",
    description="Replies with the bot's ping to the server",
)
async def slash_command_ping(interaction: Interaction):
    await interaction.response.send_message(f"Ping: `{round(bot.latency * 1000)} ms`")


@bot.slash_command(
    name="off",
    description="Turns the lights off",
)
async def slash_command_off(interaction: Interaction):
    lc.lights[:] = 0
    lc.lights.update()
    await interaction.response.send_message("Turned the lights off")


@bot.slash_command(
    name="set",
    description="Sets all lights in the slice to the specified color",
)
async def slash_command_set(
    interaction: Interaction,
    color: str,
    start: int = 0,
    stop: int = len(lc.lights),
    step: int = 1,
):
    try:
        parsed_color = parse_color(color)
    except ValueError as err:
        await interaction.response.send_message(str(err))
    else:
        try:
            lc.lights[start:stop:step] = parsed_color
        except ValueError:
            await interaction.response.send_message(
                f"`{start}` to `{stop}` with step size `{step}` is an invalid slice"
            )
        else:
            lc.lights.update()
            await interaction.response.send_message(
                f"Set lights `{start}` to `{stop}` with step size `{step}` to `{color}`"
            )


@bot.slash_command(
    name="brightness",
    description="Sets the brightness of the lights",
)
async def slash_command_brightness(
    interaction: Interaction,
    brightness: str = "0xFF",
):
    try:
        if "%" in brightness:
            parsed_brightness = int(float(brightness[:-1]) / 100 * 0xFF)
        elif "." in brightness:
            parsed_brightness = int(float(brightness) * 0xFF)
        else:
            try:
                parsed_brightness = int(brightness, 0)
            except ValueError:
                parsed_brightness = int(brightness, 16)
    except ValueError:
        await interaction.response.send_message(f"`{brightness}` is an invalid brightness")
    else:
        lc.lights.brightness(parsed_brightness)
        lc.lights.update()
        await interaction.response.send_message(f"Set brightness to `{brightness}`")


@bot.slash_command(
    name="savecolor",
    description="Saves the specified color",
)
async def slash_command_savecolor(interaction: Interaction, name: str, color: str):
    name = name.lower()
    try:
        parsed_color = parse_color(color)
    except ValueError as err:
        await interaction.response.send_message(str(err))
    else:
        lc.save_color(name, format_color(parsed_color))
        await interaction.response.send_message(f"Saved color `{color}` as `{name}`")


@bot.slash_command(
    name="save",
    description="Saves the current pattern",
)
async def slash_command_save(interaction: Interaction, name: str):
    name = name.lower()
    lc.save_pattern(name, [format_color(x) for x in lc.lights[:]])
    await interaction.response.send_message(f"Saved current pattern as `{name}`")


@bot.slash_command(
    name="load",
    description="Loads a saved pattern",
)
async def slash_command_load(interaction: Interaction, name: str):
    name = name.lower()
    try:
        pattern = lc.load_pattern(name)
    except KeyError:
        await interaction.response.send_message(f"Pattern `{name}` not found")
    else:
        lc.lights[:] = [int(x, 16) for x in pattern]
        lc.lights.update()
        await interaction.response.send_message(f"Loaded pattern `{name}`")


load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))
