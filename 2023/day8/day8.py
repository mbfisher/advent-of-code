import math
import unittest
from collections import deque
from inspect import cleandoc
from pathlib import Path
from typing import Tuple, Dict


def part1(input: str) -> int:
    lines = input.split("\n")

    instructions = lines.pop(0)
    lines.pop(0)

    network: Dict[str, Tuple[str, str]] = {}

    for line in lines:
        node, children = line.split(" = ")
        network[node] = tuple(children[1:-1].split(", "))

    node = "AAA"
    steps = 0
    i = 0

    while node != "ZZZ":
        instruction = 0 if instructions[i] == "L" else 1
        node = network[node][instruction]

        i += 1
        if i == len(instructions):
            i = 0

        steps += 1

    return steps


def part2(input: str) -> int:
    lines = input.split("\n")

    instructions = lines.pop(0)
    lines.pop(0)

    network: Dict[str, Tuple[str, str]] = {}

    paths = []

    for line in lines:
        node, children = line.split(" = ")
        network[node] = tuple(children[1:-1].split(", "))
        if node[-1] == "A":
            paths.append([node])

    steps = 0
    i = 0
    loops = [0 for _ in paths]

    while any(loop == 0 for loop in loops):
        instruction = 0 if instructions[i] == "L" else 1

        for p, path in enumerate(paths):
            node = path[-1]
            node = network[node][instruction]

            if node[-1] == "Z" and node in path and loops[p] == 0:
                loop_start = path.index(node)
                loops[p] = len(path) - loop_start

            path.append(node)

        i += 1
        if i == len(instructions):
            i = 0

        steps += 1

    return math.lcm(*loops)


class Test(unittest.TestCase):
    example1 = cleandoc("""
        RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
    """)

    example2 = cleandoc("""
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
    """)

    def test_part_1(self):
        self.assertEqual(2, part1(Test.example1))
        self.assertEqual(6, part1(Test.example2))

        print(part1(Path('./input.txt').read_text()))

    example3 = cleandoc("""
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
    """)

    def test_part_2(self):
        # self.assertEqual(6, part2(Test.example3))

        print(part2(Path('./input.txt').read_text()))
