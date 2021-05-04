WIDTH = 1
HEIGHT = WIDTH / 0.8660254
SIZE = 0.5774


def hex_to_pixel(x, y):
    p_x = WIDTH * x + 0.5 * (y & 1) + WIDTH / 2
    p_y = HEIGHT * y + HEIGHT / 2
    return p_x, p_y


def pixel_to_hex(p_x, p_y):
    y = int(p_y / HEIGHT)
    if p_y % HEIGHT < HEIGHT / 4:
        boundary = (p_x % 0.5) * (HEIGHT / 4 / 0.5)
        if p_x % 1 <= 0.5:
            boundary = (HEIGHT / 4) - boundary
        print(boundary < p_y % HEIGHT)
        y = y if boundary < p_y else y-1
    x = int(p_x / WIDTH - 0.5 * (y & 1))
    #print((x, y), (p_x, p_y))
    return x, y
