import unittest
from functools import cmp_to_key
from pathlib import Path
from typing import Tuple, List, Dict, Set


def parse(input: str) -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    rules: Dict[int, Set[int]] = {}
    updates: List[List[int]] = []
    parse_updates = False
    for line in input.splitlines():
        if line == "":
            parse_updates = True
            continue

        if parse_updates:
            updates.append(list(map(int, line.split(","))))
        else:
            page, before = tuple(map(int, line.split("|")))
            rules.setdefault(page, set()).add(before)

    return rules, updates


def part1(input: str) -> int:
    rules, updates = parse(input)
    result = 0

    for update in updates:
        valid = True

        for i, page in enumerate(update):
            if page not in rules:
                continue

            # 47|53 = 47 MUST be before 53 = 53 MUST be after 47
            # 47: 1, 2, 3 = 47 MUST be before 1 and 2 and 3 = 1 and 2 and 3 MUST be after 47
            pages_that_must_be_after_this_one = rules[page]
            pages_before_this_one = set(update[:i])

            # .difference = all elements that are in this set but not the others
            if pages_before_this_one.difference(pages_that_must_be_after_this_one) != pages_before_this_one:
                valid = False
                break

        if valid:
            result += update[len(update) // 2]

    return result


def part2(input: str) -> int:
    rules, updates = parse(input)
    result = 0

    for update in updates:
        for i, page in enumerate(update):
            if page not in rules:
                continue

            # 47|53 = 47 MUST be before 53 = 53 MUST be after 47
            # 47: 1, 2, 3 = 47 MUST be before 1 and 2 and 3 = 1 and 2 and 3 MUST be after 47
            pages_that_must_be_after_this_one = rules[page]
            pages_before_this_one = set(update[:i])

            # .difference = all elements that are in this set but not the others
            if pages_before_this_one.difference(pages_that_must_be_after_this_one) != pages_before_this_one:
                valid_update = sorted(update,
                                      # if b is in rules[a] then b MUST be after A
                                      key=cmp_to_key(lambda a, b: 0 if a not in rules else -1 if b in rules[a] else 0))

                result += valid_update[len(valid_update) // 2]
                break

    return result


class Test(unittest.TestCase):
    example1 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
    """.strip()

    def test_part_1(self):
        self.assertEqual(143, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(123, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
