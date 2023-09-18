import json
import webcolors

with open("colors.json") as f:
    colors_data = json.load(f)


def parse_color(x: str) -> int:
    x = x.lower()

    hex_prefixes = ["0x", "#"]
    for prefix in hex_prefixes:
        x = x.removeprefix(prefix)

    try:
        return int(x, 16)
    except ValueError:
        try:
            return int(webcolors.name_to_hex(x)[1:], 16)
        except ValueError:
            try:
                return int(colors_data[x], 16)
            except KeyError as exc:
                raise ValueError(f"`{x}` is an invalid input") from exc
