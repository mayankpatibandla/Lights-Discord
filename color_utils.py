import webcolors


def parse_color(x: str) -> int:
    x = x.lower()
    hex_prefixes = ["0x", "#"]

    for prefix in hex_prefixes:
        x = x.removeprefix(prefix)

    try:
        return int(x, 16)
    except ValueError:
        return int(webcolors.name_to_hex(x)[1:], 16)
