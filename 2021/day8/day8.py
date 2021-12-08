from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Set


def part1(input: str) -> int:
    result = 0

    num_segments = {2, 3, 4, 7}
    for line in input.splitlines():
        input, output = line.split(" | ")

        for digit in output.split(" "):
            len_digit = len(digit)

            if len_digit in num_segments:
                result += 1

    return result


def solve_board(line: str) -> List[Set[str]]:
    digits: Dict[int, Set[str]] = {}
    input: List[Set[str]] = list(map(set, line.split(" ")))

    for digit in input:
        len_digit = len(digit)

        if len_digit == 2:
            digits[1] = set(digit)
        if len_digit == 3:
            digits[7] = set(digit)
        if len_digit == 4:
            digits[4] = set(digit)
        if len_digit == 7:
            digits[8] = set(digit)

    input.remove(digits[1])
    input.remove(digits[7])
    input.remove(digits[4])
    input.remove(digits[8])

    for digit in input:
        if len(digit) == 5 and digits[7].issubset(digit):
            digits[3] = digit

        if len(digit) == 6 and digits[4].issubset(digit):
            digits[9] = digit

    input.remove(digits[3])
    input.remove(digits[9])

    for digit in input:
        if len(digit) == 6 and digits[1].issubset(digit):
            digits[0] = digit

    input.remove(digits[0])

    for digit in input:
        if len(digit) == 6:
            digits[6] = digit

    input.remove(digits[6])

    for digit in input:
        if len(digit) == 5 and len(digits[6].difference(digit)) == 1:
            digits[5] = digit
        else:
            digits[2] = digit

    return [digits[i] for i in range(0, 10)]


def part2(input: str) -> int:
    result = 0

    for line in input.splitlines():
        input, output = line.split(" | ")

        values: Dict[str, int] = {''.join(sorted(digit)): value for value, digit in enumerate(solve_board(input))}

        try:
            result += int(''.join(map(lambda digit: str(values[digit]), map(lambda digit: ''.join(sorted(digit)), output.split(" ")))))
        except KeyError as e:
            print(e, values, output)
            raise

    return result


if __name__ == '__main__':
    example = '\n'.join([
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
    ])

    input = Path('./input.txt').read_text()

    example_part1 = part1(example)
    assert example_part1 == 26, f"got {example_part1}"
    print(part1(input))

    values = solve_board("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab")
    assert values[0] == set('cagedb'), values[0]
    assert values[1] == set('ab'), values[1]
    assert values[2] == set('gcdfa'), values[2]
    assert values[3] == set('fbcad'), values[3]
    assert values[4] == set('eafb'), values[4]
    assert values[5] == set('cdfbe'), values[5]
    assert values[6] == set('cdfgeb'), values[6]
    assert values[7] == set('dab'), values[7]
    assert values[8] == set('acedgfb'), values[8]
    assert values[9] == set('cefabd'), values[9]

    example_part2a = part2("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    assert example_part2a == 5353, f"got {example_part2a}"
    example_part2 = part2(example)
    assert example_part2 == 61229, f"got {example_part2}"
    print(part2(input))
