ASTEROID = '#'


def asteroid_positions(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == ASTEROID:
                yield (x, y)


def factors(num):
    if num == 0:
        return
    for i in range(1, int(num/2)+1):
        if num % i == 0:
            yield i
    yield num


def get_common_divisors(a, b):
    a = abs(a)
    b = abs(b)
    low = min(a, b)
    high = max(a, b)
    for i in factors(low):
        if high % i == 0:
            yield i


def get_greatest_common_divisor(a, b):
    return max(get_common_divisors(a, b))


def get_scale_ratios(num, den):
    # Return rational numbers that represent the same fraction as num/den
    try:
        ratio = 1.0 * num/den
        gcd = get_greatest_common_divisor(num, den)
    except Exception:
        # The numbers are relatively prime and cannot be scaled downwards
        return
    base = int(num / gcd)
    for scale in range(base, num, base):
        yield (scale, int(scale/ratio))


def get_rational_intervals(src, dst):
    diffX = dst[0] - src[0]
    diffY = dst[1] - src[1]
    for midX, midY in get_scale_ratios(diffX, diffY):
        yield (src[0] + midX, src[1] + midY)


def visible_asteroids(asteroids, src):
    for dst in asteroids:
        intervals = list(get_rational_intervals(src, dst))
        print(intervals)
        blocking_view = list(point in asteroids for point in intervals)
        print(blocking_view)
        if not any(blocking_view):
            yield dst


assert set(factors(8)) == {1, 2, 4, 8}
assert set(factors(12)) == {1, 2, 3, 4, 6, 12}
assert set(get_scale_ratios(4, 8)) == {(1, 2), (2, 4), (3, 6)}
assert set(get_scale_ratios(6, 4)) == {(3, 2)}
assert set(get_rational_intervals((1, 0), (5, 4))) == {(2, 1), (3, 2), (4, 3)}

with open('data.txt', 'r') as fp:
    asteroids = set(asteroid_positions(fp))

print(list(visible_asteroids(asteroids, (1, 0))))

visible_dict = {
    point: sum(1 for _ in visible_asteroids(asteroids, point))
    for point in asteroids
}
print(visible_dict)
"""
most_visible = max(
    asteroids,
    key=lambda src: )
)

print(most_visible)
"""
