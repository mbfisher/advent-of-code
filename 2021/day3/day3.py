from pathlib import Path
from typing import List


def part1(input: str) -> int:
    numbers = input.split("\n")

    bits = [{'0': 0, '1': 0} for _ in range(0, len(numbers[0]))]

    for number in numbers:
        for i, bit in enumerate(number):
            bits[i][bit] += 1

    gamma = ""
    epsilon = ""
    for counts in bits:
        if counts['0'] > counts['1']:
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"

    return int(gamma, 2) * int(epsilon, 2)


def most_common_bit(numbers: "list[str]", position: int) -> str:
    counts = {'0': 0, '1': 0}

    for number in numbers:
        counts[number[position]] += 1

    return '0' if counts['0'] > counts['1'] else '1'


def part2(input: str) -> int:
    numbers = input.split("\n")
    o2 = numbers

    for i in range(0, len(numbers[0])):
        common = most_common_bit(o2, i)
        o2 = [c for c in o2 if c[i] == common]

        if len(o2) == 1:
            break

    co2 = numbers
    for i in range(0, len(numbers[0])):
        common = most_common_bit(co2, i)
        co2 = [c for c in co2 if c[i] != common]

        if len(co2) == 1:
            break

    return int(o2[0], 2) * int(co2[0], 2)


if __name__ == '__main__':
    example = '\n'.join([
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ])

    assert part1(example) == 198
    print(part1(Path('./input.txt').read_text()))

    assert part2(example) == 230
    print(part2(Path('./input.txt').read_text()))
