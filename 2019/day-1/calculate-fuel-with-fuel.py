import math

def calculate_fuel(mass):
    return math.floor(mass / 3) - 2

def calculate_fuel_with_fuel(mass):
    fuel_needed = calculate_fuel(mass)

    fuel_for_fuel = calculate_fuel(fuel_needed)
    while fuel_for_fuel > 0:
        fuel_needed += fuel_for_fuel
        fuel_for_fuel = calculate_fuel(fuel_for_fuel)
    return fuel_needed


with open('data.txt', 'r') as fp:
    modules_mass = (int(row) for row in fp)
    modules_fuel = (calculate_fuel_with_fuel(mass) for mass in modules_mass)
    total_fuel = sum(modules_fuel)

print(total_fuel)
