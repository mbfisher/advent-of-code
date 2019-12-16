f = open("input.txt", "r")
modules = f.read().splitlines()
print(modules)

def get_fuel(mass):
    return int(mass) // 3 - 2

print(sum(map(get_fuel, modules)))