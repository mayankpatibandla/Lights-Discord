import json

import webcolors

with open("colors.json", encoding="utf-8") as f:
    colors_data = json.load(f)


def parse_color(color: str) -> int:
    for hex_prefix in ["0x", "#"]:
        color = color.lower().removeprefix(hex_prefix)

    try:
        return int(color, 16)
    except ValueError:
        try:
            return int(webcolors.name_to_hex(color)[1:], 16)
        except ValueError:
            try:
                return int(colors_data[color], 16)
            except KeyError as err:
                raise ValueError(f"`{color}` is an invalid color") from err
