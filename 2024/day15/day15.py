import re
import unittest
from functools import reduce
from math import prod
from pathlib import Path
from typing import Tuple

moves = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}

def part1(input: str, print_moves=False, print_finished=False) -> int:
    warehouse, instructions = input.split("\n\n")
    warehouse = list(map(list, warehouse.splitlines()))
    instructions = reduce(lambda result, line: result + list(line), instructions.splitlines(), [])

    robot = None
    for y, row in enumerate(warehouse):
        try:
            robot = (y, row.index('@'))
            break
        except ValueError:
            continue

    if print_moves:
        print("\n".join("".join(row) for row in warehouse), "\n")

    y, x = robot
    for instruction in instructions:
        dy, dx = moves[instruction]
        y1, x1 = y + dy, x + dx

        if warehouse[y1][x1] == '.':
            warehouse[y][x], warehouse[y1][x1] = warehouse[y1][x1], warehouse[y][x]
            y, x = y1, x1
        elif warehouse[y1][x1] != '#':
            while warehouse[y1][x1] == 'O':
                y1, x1 = y1 + dy, x1 + dx

            if warehouse[y1][x1] == '#':
                continue

            while y1 != y or x1 != x:
                warehouse[y1 - dy][x1 - dx], warehouse[y1][x1] = warehouse[y1][x1], warehouse[y1 - dy][x1 - dx]
                y1, x1 = y1 - dy, x1 - dx

            y, x = y + dy, x + dx

        if print_moves:
            print(instruction)
            print("\n".join("".join(row) for row in warehouse), "\n")

    if print_finished:
        print("\n".join("".join(row) for row in warehouse), "\n")

    result = 0

    for y in range(len(warehouse)):
        for x in range(len(warehouse[y])):
            if warehouse[y][x] == 'O':
                result += 100 * y + x

    return result

def part2(input: str, print_wider_warehouse=False, print_moves=False, print_finished=False) -> int:
    warehouse, instructions = input.split("\n\n")
    warehouse = warehouse.splitlines()
    instructions = reduce(lambda result, line: result + list(line), instructions.splitlines(), [])

    walls = set()
    boxes = set()
    robot = (0, 0)

    for y, row in enumerate(warehouse):
        x = 0
        for char in row:
            if char == '#':
                walls.add((y, x))
                walls.add((y, x + 1))
            if char == 'O':
                boxes.add((y, x))
            if char == '@':
                robot = (y, x)

            x += 2

    if print_wider_warehouse:
        print(
            "\n".join("".join(
                '##' if (y, x) in walls else
                '[]' if (y, x) in boxes else
                '@.' if (y, x) == robot else
                '..' for x in range(0, len(warehouse[y]) * 2, 2)
            ) for y in range(len(warehouse))),
            "\n"
        )

    y, x = robot

    for instruction in instructions:
        dy, dx = moves[instruction]
        y1, x1 = y + dy, x + dx

        if (y1, x1) not in walls and (y1, x1) not in boxes and (y1, x1 - 1) not in boxes:
            y, x = y1, x1
        elif (y1, x1) not in walls:
            if instruction == '>':
                while (y1, x1) in boxes:
                    boxes.remove((y1, x1))
                    y1, x1 = y1 + dy * 2, x1 + dx * 2
                    boxes.add((y1, x1))
                    y, x = y1, x1

            if instruction == '<':
                while (y1, x1 - 1) in boxes:
                    boxes.remove((y1, x1 - 1))
                    y1, x1 = y1 + dy * 2, x1 + dx * 2
                    boxes.add((y1, x1))
                    y, x = y1, x1





    result = 0


    return result


class Test(unittest.TestCase):
    example1 = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
    """.strip()

    example2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    """.strip()

    example3 = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
    """.strip()

    def test_part_1(self):
        self.assertEqual(2028, part1(self.example1))
        self.assertEqual(10092, part1(self.example2, print_finished=True))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        part2(self.example3, print_wider_warehouse=True)
        # print(part2(Path('./input.txt').read_text()))
