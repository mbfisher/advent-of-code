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





def part2(input: str) -> int:
    return 0


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

    # assert part2(example) == 900
    # print(part2(Path('./input.txt').read_text()))
