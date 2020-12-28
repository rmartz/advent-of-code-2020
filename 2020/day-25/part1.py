from itertools import islice


def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    v = next(islice(iterable, n, None), default)
    return v


def generate_transforms(subject_number):
    number = 1
    while True:
        yield number
        number *= subject_number
        number %= 20201227


def transform(subject_number, loop_size):
    return nth(generate_transforms(subject_number), loop_size)


def find_public_key_loop_size(subject_number, public_key):
    for i, val in enumerate(generate_transforms(subject_number)):
        if val == public_key:
            return i


def find_encryption_key(subject_number, public_keys):
    alice_key, bob_key = public_keys
    alice_loop_size = find_public_key_loop_size(subject_number, alice_key)
    return transform(bob_key, alice_loop_size)


assert transform(7, 11) == 17807724
assert transform(7, 8) == 5764801

assert find_public_key_loop_size(7, 5764801) == 8
assert find_public_key_loop_size(7, 17807724) == 11
assert find_encryption_key(7, [17807724, 5764801]) == 14897079

with open("./data.txt", "r") as fp:
    keys = [int(val) for val in fp]
print(find_encryption_key(7, keys))
