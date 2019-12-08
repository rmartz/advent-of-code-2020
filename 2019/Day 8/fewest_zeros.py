from itertools import islice

IMAGE_WIDTH=25
IMAGE_HEIGHT=6

def chunk(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(islice(it, n))
       if not chunk:
           return
       yield chunk


def count_pixel_val(layer, v):
    return sum(
        1 if pixel == v else 0
        for pixel in layer
    )


with open('data.txt', 'r') as fp:
    layers = chunk(IMAGE_HEIGHT * IMAGE_WIDTH, fp.read().strip())

    least_zeros = min(layers, key=lambda l: count_pixel_val(l, '0'))
    print(
        count_pixel_val(least_zeros, '1') *
        count_pixel_val(least_zeros, '2')
    )

