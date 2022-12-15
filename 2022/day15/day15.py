import json
import unittest
from collections import deque
from itertools import permutations
from pathlib import Path


def attempt1(input: str) -> int:
    sensors = {}

    x = 0
    y = 1
    for line in input.split("\n"):
        sensor = tuple(map(lambda coord: int(coord[2:]), line.split(": ")[0][len("Sensor at "):].split(", ")))
        beacon = tuple(
            map(lambda coord: int(coord[2:]), line.split(": ")[1][len("closest beacon is at "):].split(", ")))
        sensors[sensor] = beacon

    beacons = set(sensors.values())
    no_beacons = set()

    for sensor, beacon in sensors.items():
        dist = abs(beacon[x] - sensor[x]) + abs(beacon[y] - sensor[y])
        rd = 0
        while dist > 0:
            for row in [sensor[y] + rd, sensor[y] - rd]:
                for col in range(sensor[x] - dist, sensor[x] + dist + 1):
                    if (col, row) not in sensors and (col, row) not in beacons:
                        no_beacons.add((col, row))

            dist -= 1
            rd += 1

    return len([(x, y) for (x, y) in no_beacons if y == 10])


def part1(input: str, row_y: int) -> int:
    sensors = {}
    x = 0
    y = 1

    for line in input.split("\n"):
        sensor = tuple(map(lambda coord: int(coord[2:]), line.split(": ")[0][len("Sensor at "):].split(", ")))
        beacon = tuple(
            map(lambda coord: int(coord[2:]), line.split(": ")[1][len("closest beacon is at "):].split(", ")))
        sensors[sensor] = beacon

    beacons = set(sensors.values())

    no_beacons = set()
    for sensor, beacon in sensors.items():
        dist = abs(beacon[x] - sensor[x]) + abs(beacon[y] - sensor[y])
        if sensor[y] + dist >= row_y or sensor[y] - dist <= row_y:
            r = abs(sensor[y] - row_y)
            for rx in range(sensor[x] - dist + r, sensor[x] + dist - r + 1):
                if (rx, row_y) not in beacons:
                    no_beacons.add((rx, row_y))

    return len(no_beacons)


def part2(input: str, search_space=4000000) -> int:
    sensors = {}
    x = 0
    y = 1

    for line in input.split("\n"):
        sensor = tuple(map(lambda coord: int(coord[2:]), line.split(": ")[0][len("Sensor at "):].split(", ")))
        beacon = tuple(
            map(lambda coord: int(coord[2:]), line.split(": ")[1][len("closest beacon is at "):].split(", ")))
        sensors[sensor] = beacon

    rows = {}

    for sensor, beacon in sensors.items():
        dist = abs(beacon[x] - sensor[x]) + abs(beacon[y] - sensor[y])
        # print(sensor, dist)
        dy = 0
        while dist > 0:
            for row in [sensor[y] + dy, sensor[y] - dy]:
                if row not in rows:
                    rows[row] = set()

                rows[row].add((sensor[x] - dist, sensor[x] + dist))

            dist -= 1
            dy += 1

    distress_beacon = None
    progress = 0
    for row, spans in rows.items():
        ordered_spans = list(spans)
        ordered_spans.sort(key=lambda span: span[0])

        span_queue = ordered_spans

        i = 0
        while len(span_queue) > 1 and i < len(span_queue) - 1:
            left = span_queue[i]
            right = span_queue[i + 1]

            # left inside right
            if left[0] >= right[0] and left[1] <= right[1]:
                span_queue = span_queue[:i] + [right] + span_queue[i + 2:]

            # right inside left
            elif left[0] <= right[0] and left[1] >= right[1]:
                span_queue = span_queue[:i] + [left] + span_queue[i + 2:]

            elif left[0] < right[1] and right[0] - left[1] <= 1:
                span_queue = span_queue[:i] + [(left[0], right[1])] + span_queue[i + 2:]

            elif right[0] < left[1] and left[0] - right[1] <= 1:
                span_queue = span_queue[:i] + [(right[0], left[1])] + span_queue[i + 2:]

            else:
                i += 1

        progress += 1
        if progress % 100000 == 0:
            print(progress)

        if len(span_queue) > 1:
            if span_queue[1][0] - span_queue[0][1] == 2:
                mdb = (span_queue[0][1] + 1, row)
                if 0 <= mdb[0] <= search_space and 0 <= mdb[1] <= search_space:
                    distress_beacon = mdb
                    break

    return distress_beacon[0] * 4000000 + distress_beacon[1]


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(26, part1(Test.example, 10))

        print(part1(Path('./input.txt').read_text(), 2000000))

    def test_part_2(self):
        self.assertEqual(56000011, part2(Test.example, search_space=20))

        print(part2(Path('./input.txt').read_text()))

    example = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip("\n")
