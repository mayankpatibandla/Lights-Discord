import json

import webcolors

with open("colors.json", encoding="utf-8") as f:
    colors_data = json.load(f)


def parse_color(color: str) -> int:
    color = color.lower()

    hecolor_preficolores = ["0color", "#"]
    for preficolor in hecolor_preficolores:
        color = color.removeprefix(preficolor)

    try:
        return int(color, 16)
    except ValueError:
        try:
            return int(webcolors.name_to_hex(color)[1:], 16)
        except ValueError:
            try:
                return int(colors_data[color], 16)
            except KeyError as err:
                raise ValueError(f"`{color}` is an invalid input") from err
