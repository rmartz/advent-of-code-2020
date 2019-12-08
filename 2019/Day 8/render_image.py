from itertools import islice

IMAGE_WIDTH=25
IMAGE_HEIGHT=6

PIXEL_BLACK='0'
PIXEL_WHITE='1'
PIXEL_TRANSPARENT='2'

def chunk(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(islice(it, n))
       if not chunk:
           return
       yield chunk


def compress_layers(layers):
    layer_by_pixel = zip(*layers)
    for pixel_vals in layer_by_pixel:
        opaque = filter(lambda val: val != PIXEL_TRANSPARENT, pixel_vals)
        yield next(opaque)


def color_image(image):
    colors = {
        PIXEL_BLACK: ' ',
        PIXEL_WHITE: '#'
    }

    return (colors.get(p) for p in image)

with open('data.txt', 'r') as fp:
    layers = chunk(IMAGE_HEIGHT * IMAGE_WIDTH, fp.read().strip())

    image = compress_layers(layers)
    colored_image = color_image(image)

    rows = chunk(IMAGE_WIDTH, colored_image)
    for row in rows:
        print(''.join(row))

