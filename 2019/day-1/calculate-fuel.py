import math

def calculate_fuel(mass):
    return math.floor(mass / 3) - 2

with open('data.txt', 'r') as fp:
    modules_mass = (int(row) for row in fp)
    modules_fuel = (calculate_fuel(mass) for mass in modules_mass)
    total_fuel = sum(modules_fuel)

print(total_fuel)
