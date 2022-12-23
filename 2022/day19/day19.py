import re
import unittest
from collections import deque
from itertools import product
from pathlib import Path
from queue import PriorityQueue
from typing import Set

order = ["ore", "clay", "obsidian", "geode"]


def pack(minute, resources=None, robots=None):
    return (minute,) + tuple(map(lambda r: resources[r], order)) + tuple(map(lambda r: robots[r], order))


def unpack(state):
    return state[0], {r: state[i + 1] for i, r in enumerate(order)}, {r: state[i + 5] for i, r in enumerate(order)}


def part1(input: str) -> int:
    blueprints = []
    for line in input.split("\n"):
        blueprint = {
            "ore": {
                "ore": 0
            },
            "clay": {
                "ore": 0
            },
            "obsidian": {
                "ore": 0,
                "clay": 0,
            },
            "geode": {
                "ore": 0,
                "obsidian": 0
            }
        }

        ore_robot_match = re.search(r'Each ore robot costs (\d+) ore', line)
        blueprint["ore"]["ore"] = int(ore_robot_match.group(1))

        clay_robot_match = re.search(r'Each clay robot costs (\d+) ore', line)
        blueprint["clay"]["ore"] = int(clay_robot_match.group(1))

        obs_robot_match = re.search(r'Each obsidian robot costs (\d+) ore and (\d+) clay', line)
        blueprint["obsidian"]["ore"] = int(obs_robot_match.group(1))
        blueprint["obsidian"]["clay"] = int(obs_robot_match.group(2))

        geo_robot_match = re.search(r'Each geode robot costs (\d+) ore and (\d+) obsidian', line)
        blueprint["geode"]["ore"] = int(geo_robot_match.group(1))
        blueprint["geode"]["obsidian"] = int(geo_robot_match.group(2))

        blueprints.append(blueprint)

    geodes = []
    priority = ["geode", "obsidian", "clay", "ore"]
    lookahead = 2
    for blueprint in blueprints:
        state = pack(
            1,
            resources={"ore": 0,
                       "clay": 0,
                       "obsidian": 0,
                       "geode": 0},
            robots={"ore": 1,
                    "clay": 0,
                    "obsidian": 0,
                    "geode": 0}
        )

        # for minute in range(1, 25, lookahead):
        queue = PriorityQueue()
        queue.put((0, state))

        result = None
        score_fn = lambda f: sum(map(lambda i: f[i] * i + f[i + 4] * i**3, range(1, 5)))
        while not queue.empty():
            _, candidate = queue.get()

            minute, resources, robots = unpack(candidate)

            if minute >= 24:
                result = candidate
                break

            options = [{"resources": resources.copy(), "robots": robots.copy()}]
            for robot in ["geode", "obsidian", "clay", "ore"]:
                if all(resources[r] >= cost for r, cost in blueprint[robot].items()):
                    option = {
                        "resources": resources.copy(),
                        "robots": robots.copy(),
                        "new_robot": robot
                    }

                    for resource, cost in blueprint[robot].items():
                        option["resources"][resource] -= cost

                    options.append(option)
                    # break

            for option in options:
                for resource, count in option["robots"].items():
                    option["resources"][resource] += count

                if "new_robot" in option:
                    option["robots"][option.pop("new_robot")] += 1

                next_state = pack(minute, **option)
                queue.put((score_fn(next_state), next_state))

        _, resources, _ = unpack(result)
        geodes.append(resources["geodes"])

    return sum(map(lambda i: (i + 1) * geodes[i], range(len(geodes))))


def part2(input: str) -> int:
    pass


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(33, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(58, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip("\n")
