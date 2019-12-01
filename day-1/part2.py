f = open("input.txt", "r")
modules = f.read().splitlines()
# print(modules)

def get_fuel_for_mass(mass):
    return int(mass) // 3 - 2

def get_fuel(mass):
    result = get_fuel_for_mass(mass)
    extra = result
    while True:
        extra = get_fuel_for_mass(extra)
        if extra > 0:
            result += extra
        else:
            return result


print(sum(map(get_fuel, modules)))