import os

from dotenv import load_dotenv
from lights_controller import lights, load_color, load_pattern, save_color, save_pattern
from nextcord import Intents, Interaction
from nextcord.ext import commands

from color_utils import parse_color

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
    lights[:] = 0
    lights.update()
    await interaction.response.send_message("Turned the lights off")


@bot.slash_command(
    name="set",
    description="Sets all lights in the slice to the specified color",
)
async def slash_command_set(
    interaction: Interaction,
    color: str,
    start: int = 0,
    stop: int = len(lights),
    step: int = 1,
):
    try:
        parsed_color = parse_color(color)
    except ValueError as err:
        await interaction.response.send_message(str(err))
    else:
        try:
            lights[start:stop:step] = parsed_color
        except ValueError:
            await interaction.response.send_message(
                f"`{start}` to `{stop}` with step size `{step}` is an invalid slice"
            )
        else:
            lights.update()
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
            parsed_brightness = int(brightness, 0)
    except ValueError:
        await interaction.response.send_message(f"`{brightness}` is an invalid brightness")
    else:
        lights.brightness(parsed_brightness)
        lights.update()
        await interaction.response.send_message(f"Set brightness to `{brightness}`")


@bot.slash_command(
    name="save",
    description="Saves the current pattern",
)
async def slash_command_save(interaction: Interaction, name: str):
    save_pattern(name, [hex(x)[2:].zfill(6) for x in lights[:]])
    await interaction.response.send_message(f"Saved current pattern as `{name}`")

@bot.slash_command(name="load", description="Loads a saved pattern",)
async def slash_command_load(interaction: Interaction, name: str):
    try:
        pattern = load_pattern(name)
    except KeyError:
        await interaction.response.send_message(f"Pattern `{name}` not found")
    else:
        lights[:] = [int(x, 16) for x in pattern]
        lights.update()
        await interaction.response.send_message(f"Loaded pattern `{name}`")

load_dotenv()
bot.run(os.getenv("BOT_TOKEN"))
