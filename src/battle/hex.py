WIDTH = 1
HEIGHT = WIDTH / 0.8660254
SIZE = 0.5774


def hex_to_pixel(x, y):
    p_x = WIDTH * x + 0.5 * (y & 1) + WIDTH/2
    p_y = HEIGHT * y + HEIGHT/2
    return p_x, p_y


def pixel_to_hex(p_x, p_y):
    y = int(p_y / HEIGHT)
    x = int(p_x / WIDTH - 0.5 * (y & 1))
    return x, y
