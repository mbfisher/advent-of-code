import unittest
from collections import deque
from pathlib import Path
from typing import Set


def part1(input: str) -> int:
    cubes = set(map(lambda coords: tuple(map(int, coords.split(","))), input.split("\n")))

    result = 0
    for cube in cubes:
        for neighbour in [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1)
        ]:
            if (cube[0] + neighbour[0], cube[1] + neighbour[1], cube[2] + neighbour[2]) not in cubes:
                result += 1

    return result


def part2_attempt1(input: str) -> int:
    cubes = set(map(lambda coords: tuple(map(int, coords.split(","))), input.split("\n")))

    result = 0
    for cube in cubes:
        for neighbour in [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1)
        ]:
            if (cube[0] + neighbour[0], cube[1] + neighbour[1], cube[2] + neighbour[2]) not in cubes:
                result += 1

    xi, yi, zi = 0, 1, 2
    mn, mx = 0, 1
    containers = {}
    layers = {}
    air = set()

    for cube in cubes:
        layers.setdefault(cube[yi], set()).add(cube)
        container = containers.setdefault(cube[yi], ([float('inf'), 0], None, [float('inf'), 0]))

        for i in [xi, zi]:
            if cube[i] < container[i][mn]:
                container[i][mn] = cube[i]
            if cube[i] > container[i][mx]:
                container[i][mx] = cube[i]

    for y in sorted(layers.keys()):
        layer = layers[y]
        print("layer", y)
        container = containers[y]

        for x in range(container[xi][mn], container[xi][mx] + 1):
            for z in range(container[zi][mn], container[zi][mx] + 1):
                if (x, y, z) in layer:
                    continue

                dfs = deque([(x, y, z)])
                visited = set()

                found_container = False
                while len(dfs):
                    space = dfs.pop()
                    visited.add(space)

                    if space[xi] < container[xi][mn] or space[xi] > container[xi][mx] or \
                            space[zi] < container[zi][mn] or space[zi] > container[zi][mx]:
                        found_container = True
                        break

                    for i, direction in enumerate([(0, None, 1), (1, None, 0), (0, None, -1), (-1, None, 0)]):
                        next_space = (space[xi] + direction[xi], y, space[zi] + direction[zi])

                        if next_space not in layer and next_space not in visited:
                            dfs.append(next_space)

                if not found_container:
                    air.add((x, y, z))

        output = []
        for z in range(container[zi][mn] - 1, container[zi][mx] + 2):
            line = ""
            for x in range(container[xi][mn] - 1, container[xi][mx] + 2):
                if z == container[zi][mn] - 1 or z == container[zi][mx] + 1:
                    line += '_'
                elif x == container[xi][mn] - 1 or x == container[xi][mx] + 1:
                    line += '|'
                elif (x, y, z) in layer:
                    line += 'x'
                elif (x, y, z) in air:
                    line += '.'
                else:
                    line += ' '

            output.append("".join(line))

        print("\n" + "\n".join(reversed(output)))

    for cube in cubes:
        for neighbour in [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1)
        ]:
            if (cube[0] + neighbour[0], cube[1] + neighbour[1], cube[2] + neighbour[2]) in air:
                result -= 1

    return result


def part2(input: str) -> int:
    cubes = set(map(lambda coords: tuple(map(int, coords.split(","))), input.split("\n")))

    xi, yi, zi = 0, 1, 2

    container = tuple([float('inf'), 0] for _ in range(3))
    mn, mx = 0, 1

    for cube in cubes:
        for i in [xi, yi, zi]:
            if cube[i] - 1 < container[i][mn]:
                container[i][mn] = cube[i] - 1
            if cube[i] + 1 > container[i][mx]:
                container[i][mx] = cube[i] + 1

    dfs = deque([(container[xi][mn], container[yi][mn], container[yi][mn])])

    visited = set()
    surfaces = {}

    while len(dfs):
        cube = dfs.pop()

        visited.add(cube)

        for i in [xi, yi, zi]:
            for direction in [-1, 1]:
                next_cube = list(cube)
                next_cube[i] += direction
                next_cube = tuple(next_cube)

                if container[xi][mn] <= next_cube[xi] <= container[xi][mx] and \
                        container[yi][mn] <= next_cube[yi] <= container[yi][mx] and \
                        container[zi][mn] <= next_cube[zi] <= container[zi][mx] and \
                        next_cube not in visited:

                    if next_cube in cubes:
                        surfaces.setdefault(next_cube, set()).add(cube)
                    else:
                        dfs.append(next_cube)

    for y in range(container[yi][mn], container[yi][mx] + 1):
        output = []
        for z in range(container[zi][mn] - 1, container[zi][mx] + 2):
            line = ""
            for x in range(container[xi][mn] - 1, container[xi][mx] + 2):
                if z == container[zi][mn] - 1 or z == container[zi][mx] + 1:
                    line += '_'
                elif x == container[xi][mn] - 1 or x == container[xi][mx] + 1:
                    line += '|'
                elif (x, y, z) in surfaces:
                    line += str(len(surfaces[(x, y, z)])) if len(surfaces[(x, y, z)]) <= 5 else 'E'
                elif (x, y, z) in visited:
                    line += '.'
                else:
                    line += ' '

            output.append("".join(line))

        print("layer", y)
        print("\n" + "\n".join(reversed(output)))

    return sum(map(len, surfaces.values()))


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(10, part1("1,1,1\n2,1,1"))
        self.assertEqual(64, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(58, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip("\n")
