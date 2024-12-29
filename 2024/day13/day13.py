import itertools
import operator
import re
import unittest
from pathlib import Path
from typing import Tuple, Optional


def machines(input: str) -> Tuple[Tuple[str, str, str], ...]:
    result = []
    machine = []
    for line in input.splitlines():
        if line == "":
            result.append(tuple(machine))
            machine = []
        else:
            machine.append(line)

    result.append(tuple(machine))

    return tuple(result)


button_pattern = re.compile(r'Button [A-Z]: X([^,]+), Y(.+)$')
prize_pattern = re.compile(r'Prize: X=(\d+), Y=(\d+)$')


def min_tokens(machine: Tuple[str, str, str], offset=0) -> int:
    ax, ay = tuple(map(int, button_pattern.match(machine[0]).groups()))
    bx, by = tuple(map(int, button_pattern.match(machine[1]).groups()))
    px, py = tuple(map(int, prize_pattern.match(machine[2]).groups()))

    px, py = px + offset, py + offset

    j = (py * ax - ay * px) / (by * ax - ay * bx)
    i = (px - bx * j) / ax

    if int(j) == j and int(i) == i:
        return int(i * 3 + j)

    return 0


def part1(input: str) -> int:
    return sum(map(min_tokens, machines(input)))

def part2(input: str) -> int:
    return sum(map(lambda machine: min_tokens(machine, offset=10000000000000), machines(input)))

class Test(unittest.TestCase):
    example1 = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
    """.strip()

    example2 = """

    """.strip()

    def test_part_1(self):
        self.assertEqual(280, min_tokens(machines(self.example1)[0]))
        self.assertEqual(480, part1(self.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(min_tokens(machines(self.example1)[0], offset=10000000000000), 0)
        self.assertGreater(min_tokens(machines(self.example1)[1], offset=10000000000000), 0)
        self.assertEqual(min_tokens(machines(self.example1)[2], offset=10000000000000), 0)
        self.assertGreater(min_tokens(machines(self.example1)[3], offset=10000000000000), 0)

        print(part2(Path('./input.txt').read_text()))
