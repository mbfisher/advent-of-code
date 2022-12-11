import unittest
from collections import deque
from math import prod
from pathlib import Path


def parse_monkeys(input):
    monkeys = []

    lines = deque(input.split("\n"))
    monkey = None

    while lines:
        line = lines.popleft().strip()

        if line.startswith("Monkey"):
            if monkey is not None:
                monkeys.append(monkey)

            monkey = {
                "inspections": 0
            }

        if line.startswith("Starting items"):
            monkey["items"] = deque(map(int, line.split(": ")[1].split(", ")))

        if line.startswith("Operation"):
            monkey["operation"] = line.split(": ")[1].split(" = ")[1]

        if line.startswith("Test"):
            monkey["test"] = {
                "divisible": int(line.split(" ")[3]),
                True: int(lines.popleft().strip().split(" ")[5]),
                False: int(lines.popleft().strip().split(" ")[5])
            }

    monkeys.append(monkey)
    return monkeys


def part1(input: str) -> int:
    monkeys = parse_monkeys(input)

    for _ in range(20):
        for monkey in monkeys:
            while monkey["items"]:
                old = monkey["items"].popleft()
                monkey["inspections"] += 1
                worry_level = int(eval(monkey["operation"]))
                worry_level //= 3
                next_monkey = monkey["test"][worry_level % monkey["test"]["divisible"] == 0]
                monkeys[next_monkey]["items"].append(worry_level)

    monkeys.sort(key=lambda m: m["inspections"], reverse=True)

    return monkeys[0]["inspections"] * monkeys[1]["inspections"]


def part2(input: str) -> str:
    monkeys = parse_monkeys(input)

    mod = prod(monkey["test"]["divisible"] for monkey in monkeys)

    for round in range(1, 10001):
        for i, monkey in enumerate(monkeys):
            while monkey["items"]:
                old = monkey["items"].popleft()
                monkey["inspections"] += 1
                worry_level = int(eval(monkey["operation"]))
                worry_level = worry_level % mod
                next_monkey = monkey["test"][worry_level % monkey["test"]["divisible"] == 0]
                monkeys[next_monkey]["items"].append(worry_level)

        # if round in [1, 20] or round % 1000 == 0:
        #     print(round)
        #     print([monkey["inspections"] for monkey in monkeys])

    monkeys.sort(key=lambda m: m["inspections"], reverse=True)

    return monkeys[0]["inspections"] * monkeys[1]["inspections"]


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(10605, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(2713310158, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".strip("\n")