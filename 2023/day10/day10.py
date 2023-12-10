import unittest
from inspect import cleandoc
from pathlib import Path
from typing import List, Mapping, Dict, Set, Tuple

from utils.neighbours import neighbours, DIRECTIONS_CARDINAL, Position, Direction

connections = {
    "|": {
        Direction.N: "|7F",
        Direction.S: "|JL"
    },
    "-": {
        Direction.E: "-J7",
        Direction.W: "-FL"
    },
    "F": {
        Direction.E: "-J7",
        Direction.S: "|JL"
    },
    "L": {
        Direction.E: "-J7",
        Direction.N: "|7F"
    },
    "J": {
        Direction.N: "|7F",
        Direction.W: "-FL"
    },
    "7": {
        Direction.S: "|JL",
        Direction.W: "-FL"
    }
}


def part1(input: str) -> int:
    field = tuple(tuple(line) for line in input.split("\n"))

    S = (0, 0)

    for r, row in enumerate(field):
        for c, tile in enumerate(row):
            if tile == 'S':
                S = (r, c)

    loop: List[Position] = [S]

    done = False
    while not done:
        head = loop[-1]
        tile = field[head[0]][head[1]]

        for (r, c), direction in neighbours(head, field, DIRECTIONS_CARDINAL):
            neighbour = field[r][c]

            if len(loop) == 1:
                if any(direction in valid and neighbour in valid[direction] for _, valid in connections.items()):
                    loop.append((r, c))
                    break
                else:
                    continue

            if (r, c) == loop[-2]:
                continue

            if direction in connections[tile]:
                if (r, c) == S:
                    done = True
                    break

                if neighbour in connections[tile][direction]:
                    loop.append((r, c))
                    break

    i = 1
    j = len(loop) - 1

    while loop[i] != loop[j]:
        i += 1
        j -= 1

    return max(i, len(loop) - i)


def part2(input: str) -> int:
    return 0


class Test(unittest.TestCase):
    example1 = cleandoc("""
        -L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF
    """)

    example2 = cleandoc("""
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
    """)

    def test_part_1(self):
        self.assertEqual(4, part1(Test.example1))
        self.assertEqual(8, part1(Test.example2))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(0, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
