import webcolors

def parse_color(x):
    result = 0

    try:
        result = int(x, 16)
    except ValueError:
        result = int(webcolors.name_to_hex(x)[1:], 16)

    return result
