import itertools
import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    total_calibration_result = 0

    for line in input.splitlines():
        equation_test_value, equation_numbers = line.split(': ')
        equation_test_value = int(equation_test_value)
        equation_numbers = tuple(map(int, equation_numbers.split(' ')))

        for operators in map(deque, itertools.product('+*', repeat=len(equation_numbers) - 1)):
            numbers = deque(equation_numbers)
            result = numbers.popleft()

            while len(numbers) > 0:
                number = numbers.popleft()
                operator = operators.popleft()
                if operator == '+':
                    result += number
                else:
                    result *= number

            if result == equation_test_value:
                total_calibration_result += result
                break

    return total_calibration_result


def part2(input: str, debug=False) -> int:
    total_calibration_result = 0

    for line in input.splitlines():
        equation_test_value, equation_numbers = line.split(': ')
        equation_test_value = int(equation_test_value)
        equation_numbers = tuple(map(int, equation_numbers.split(' ')))

        for operators in map(deque, itertools.product('+*|', repeat=len(equation_numbers) - 1)):
            numbers = deque(equation_numbers)
            result = numbers.popleft()

            while len(numbers) > 0:
                number = numbers.popleft()
                operator = operators.popleft()
                if operator == '|':
                    result = int(str(result) + str(number))
                elif operator == '+':
                    result += number
                else:
                    result *= number

            if result == equation_test_value:
                total_calibration_result += result
                break

    return total_calibration_result


class Test(unittest.TestCase):
    example1 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
    """.strip()

    def test_part_1(self):
        self.assertEqual(3749, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(11387, part2(Test.example1, debug=True))

        print(part2(Path('./input.txt').read_text()))
