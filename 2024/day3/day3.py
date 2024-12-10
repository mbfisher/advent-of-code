import re
import unittest
from pathlib import Path


def part1(input: str) -> int:
    result = 0
    for match in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', input):
        result += int(match[0]) * int(match[1])

    return result


def part2(input: str) -> int:
    enabled = True
    dont = 'don\'t()'
    do = 'do()'
    max_mul_instruction_len = len('mul(999,999)')
    mul_pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    i = 0
    result = 0
    while i < len(input):
        if input[i:i+len(dont)] == dont:
            enabled = False
            i += len(dont)
            continue
        if input[i:i+len(do)] == do:
            enabled = True
            i += len(do)
            continue

        if not enabled:
            i += 1
            continue

        match = mul_pattern.match(input[i:i+max_mul_instruction_len])
        if match is not None:
            result += int(match.group(1)) * int(match.group(2))
            i += len(match.group(0))
            continue

        i += 1

    return result


class Test(unittest.TestCase):
    example1 = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'

    example2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    def test_part_1(self):
        self.assertEqual(161, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(48, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))
