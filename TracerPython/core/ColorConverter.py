def hex_to_rgb(hex):
    hex = hex.lstrip('#')

    if len(hex) == 3:
        hex = ''.join([char*2 for char in hex])

    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)

    return (r, g, b)