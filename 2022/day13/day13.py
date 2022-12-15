import json
import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    result = 0

    pair = []
    index = 0
    for line in input.split("\n"):
        if line == "":
            continue
        else:
            pair.append(json.loads(line))

        if len(pair) < 2:
            continue

        index += 1
        left_packet = deque(pair[0])
        right_packet = deque(pair[1])

        while True:
            try:
                left = left_packet.popleft()
            except IndexError:
                if len(right_packet):
                    result += index

                break

            try:
                right = right_packet.popleft()
            except IndexError:
                break

            if isinstance(left, int) and isinstance(right, int):
                if left == right:
                    continue

                if left < right:
                    result += index

                break

            if isinstance(left, list) and isinstance(right, list):
                if len(left) > 0 and len(right) > 0:
                    left_packet.appendleft(left[1:])
                    left_packet.appendleft(left[0])

                    right_packet.appendleft(right[1:])
                    right_packet.appendleft(right[0])

                    continue

                if len(left) == 0 and len(right) == 0:
                    continue

                if len(left) < len(right):
                    result += index

                break

            if isinstance(left, int):
                left_packet.appendleft([left])
                right_packet.appendleft(right)
            else:
                right_packet.appendleft([right])
                left_packet.appendleft(left)

        pair = []

    return result


def part2(input: str) -> int:

    packets = []
    for line in input.split("\n"):
        if line == "":
            continue
        else:
            packets.append(json.loads(line))

    divider_packets = [[[2]], [[6]]]
    for packet in divider_packets:
        packets.append(packet)

    def packets_in_order(left_packet, right_packet):
        left_stack = deque(left_packet)
        right_stack = deque(right_packet)

        while True:
            try:
                left = left_stack.popleft()
            except IndexError:
                return len(right_stack) > 0

            try:
                right = right_stack.popleft()
            except IndexError:
                return False

            if isinstance(left, int) and isinstance(right, int):
                if left == right:
                    continue

                return left < right

            if isinstance(left, list) and isinstance(right, list):
                if len(left) > 0 and len(right) > 0:
                    left_stack.appendleft(left[1:])
                    left_stack.appendleft(left[0])

                    right_stack.appendleft(right[1:])
                    right_stack.appendleft(right[0])

                    continue

                if len(left) == 0 and len(right) == 0:
                    continue

                return len(left) < len(right)

            if isinstance(left, int):
                left_stack.appendleft([left])
                right_stack.appendleft(right)
            else:
                right_stack.appendleft([right])
                left_stack.appendleft(left)

    def partition(array, low, high):
        pivot = high
        left = low
        right = pivot - 1

        while left <= right:
            if not packets_in_order(array[left], array[pivot]):
                while not packets_in_order(array[right], array[pivot]) and left <= right:
                    right -= 1

                if right < left:
                    break

                array[left], array[right] = array[right], array[left]

            left += 1

        array[left], array[pivot] = array[pivot], array[left]
        return left

    def quicksort(array, low, high):
        if low < high:
            pivot = partition(array, low, high)
            quicksort(array, low, pivot-1)
            quicksort(array, pivot+1, high)

    quicksort(packets, 0, len(packets)-1)

    result = 1
    for i, packet in enumerate(packets):
        if packet in divider_packets:
            result *= i+1

    return result


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(13, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(140, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".strip("\n")
