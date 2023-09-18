import json
import webcolors


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
            with open("colors.json") as f:
                data = json.load(f)
                try:
                    return int(data[x], 16)
                except KeyError as exc:
                    raise ValueError(f"`{x}` is an invalid input") from exc
