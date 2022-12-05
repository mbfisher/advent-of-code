import unittest
from pathlib import Path


def part1(input: str) -> int:
    result = 0

    for line in input.split("\n"):
        compartments = (line[:len(line) // 2], line[len(line) // 2:])
        types = [set(compartment) for compartment in compartments]
        common_type = types[0].intersection(types[1]).pop()
        common_type_ord = ord(common_type)
        priority = common_type_ord - 64 + 26 if common_type_ord <= 90 else common_type_ord - 96
        result += priority

    return result


def part2(input: str) -> int:
    result = 0
    count = 0
    items = set()

    for line in input.split("\n"):
        items = set(line) if len(items) == 0 else items.intersection(set(line))
        count += 1

        if count == 3:
            common_type = items.pop()
            common_type_ord = ord(common_type)
            priority = common_type_ord - 64 + 26 if common_type_ord <= 90 else common_type_ord - 96
            result += priority

            count = 0
            items = set()

    return result


class Test(unittest.TestCase):
    example = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
    """.strip()

    def test_part_1(self):
        self.assertEqual(157, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        # self.assertEqual(12, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))
