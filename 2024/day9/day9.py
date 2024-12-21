import itertools
import unittest
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple


def parse(input: str) -> Tuple[List[str], Dict[str, Tuple[int, int]]]:
    is_file = True
    disk = []
    files = {}

    for i, char in enumerate(input):
        size = int(char)
        if is_file:
            file_id = str(i // 2)
            disk.extend((file_id,) * size)
            files[file_id] = (len(disk) - 1, size)
            is_file = False
        else:
            disk.extend(('.',) * size)
            is_file = True

    return disk, files


def defragment1(disk: List[str]) -> List[str]:
    defragmented = disk.copy()
    i = 0
    j = len(defragmented) - 1
    while i < len(defragmented) and i < j:
        if defragmented[i] == '.':
            defragmented[i] = defragmented[j]
            defragmented[j] = '.'
            while defragmented[j] == '.':
                j -= 1

        i += 1

    return defragmented


def checksum(disk: List[str]) -> int:
    result = 0
    for i, block in enumerate(disk):
        if block == '.':
            continue

        result += i * int(block)

    return result


def part1(input: str) -> int:
    disk, files = parse(input)
    return checksum(defragment1(disk))


def defragment2(disk: List[str], files: Dict[str, Tuple[int, int]]):
    defragmented = disk.copy()

    for file_id in sorted(files.keys(), reverse=True):
        file_end, file_size = files[file_id]
        i = 0

        while i < len(defragmented) and i < file_end - file_size:
            if defragmented[i] == '.':
                # seek forward to find the end of this space
                k = i
                while defragmented[k] == '.':
                    k += 1

                space = k - i

                if file_size <= space:
                    j = file_end
                    while j > file_end - file_size:
                        defragmented[i], defragmented[j] = defragmented[j], defragmented[i]
                        i += 1
                        j -= 1

                    break

            i += 1

    return defragmented


def part2(input: str) -> int:
    block_ranges = []
    is_file = True
    for i, size in enumerate(input):
        if is_file:
            block_ranges.append((i // 2, int(size)))
        else:
            block_ranges.append((None, int(size)))

        is_file = not is_file

    for j in range(len(block_ranges) - 1, -1, -1):
        if block_ranges[j][0] is None:
            continue
        file_id, file_size = block_ranges[j]

        i = 0
        while i < j:
            _, space_size = block_ranges[i]

            if block_ranges[i][0] is not None or file_size > space_size:
                i += 1
                continue

            block_ranges[i] = (file_id, file_size)
            block_ranges[j] = (None, file_size)

            if file_size < space_size:
                block_ranges.insert(i+1, (None, space_size - file_size))

            break

    # print(''.join(str(file_id) * size if file_id is not None else '.' * size for file_id, size in block_ranges))

    checksum = 0
    k = 0
    for file_id, file_size in block_ranges:
        if file_id is None:
            k += file_size
            continue
        for _ in range(file_size):
            checksum += k * file_id
            k += 1

    return checksum



class Test(unittest.TestCase):
    example1 = "12345"
    example2 = "2333133121414131402"

    def test_part_1(self):
        self.assertEqual((list('0..111....22222'), {'0': (0, 1), '1': (5, 3), '2': (14, 5)}), parse(Test.example1))
        self.assertEqual(list('022111222......'), defragment1(parse(Test.example1)[0]))
        self.assertEqual(list('0099811188827773336446555566..............'), defragment1(parse(Test.example2)[0]))
        self.assertEqual(1928, part1(Test.example2))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(2858, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))
