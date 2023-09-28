import json

import lights_controller as lc
import webcolors

with open("colors.json", encoding="utf-8") as f:
    colors_data = json.load(f)


def parse_color(color: str) -> int:
    color = color.lower()

    try:
        return int(lc.load_color(color), 16)
    except KeyError:
        try:
            return int(color, 0)
        except ValueError:
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


def format_color(color: int) -> str:
    return hex(color)[2:].zfill(6)
