import json
import unittest
from collections import deque
from itertools import permutations, combinations
from pathlib import Path
from queue import PriorityQueue


def part1(input: str) -> int:
    flow_rates = {}
    tunnels = {}

    for line in input.split("\n"):
        valve_info, tunnel_info = line.split("; ")
        valve = valve_info[len("Valve "):len("Valve ") + 2]
        flow_rate = int(valve_info.split()[-1].split('=')[1])
        next_tunnels = tunnel_info[len("tunnels lead to valve "):].split(", ")
        flow_rates[valve] = flow_rate
        if valve not in tunnels:
            tunnels[valve] = []
        for tunnel in next_tunnels:
            tunnels[valve].append(tunnel.strip())

    paths = {}
    non_zero_flow_rates = {name: flow_rate for name, flow_rate in flow_rates.items() if flow_rate > 0}
    for target in non_zero_flow_rates.keys():
        for source in flow_rates.keys():
            if source == target:
                continue

            if source not in paths:
                paths[source] = {}

            bfs = deque([((source,), 0)])
            visited = set()
            while len(bfs):
                path, distance = bfs.popleft()
                current = path[-1]

                visited.add(current)

                if current == target:
                    paths[source][target] = path[1:]
                    break

                for next in tunnels[current]:
                    if next in visited:
                        continue
                    bfs.append((path + (next,), distance + 1))

    dfs = deque([{
        "path": ("AA",),
        "open_valves": {
            "AA": 0
        },
        "time": 1
    }])

    result = 0
    combos = 0
    while len(dfs):
        search = dfs.pop()

        if search["time"] >= 30:
            combos += 1
            pressure = 0
            for valve, open_minute in search["open_valves"].items():
                pressure += (30 - open_minute) * flow_rates[valve]

            if pressure > result:
                result = pressure

            continue

        valve = search["path"][-1]

        if valve not in search["open_valves"]:
            search["open_valves"][valve] = search["time"]

            if len(search["open_valves"]) == len(non_zero_flow_rates) + 1:
                dfs.append({
                    "path": search["path"],
                    "open_valves": search["open_valves"],
                    "time": 30
                })
            else:
                dfs.append({
                    "path": search["path"],
                    "open_valves": {k: v for k, v in search["open_valves"].items()},
                    "time": search["time"] + 1
                })

            continue

        for target, path in paths[valve].items():
            if target in search["open_valves"].keys():
                continue

            dfs.append({
                "path": search["path"] + (target,),
                "open_valves": {k: v for k, v in search["open_valves"].items()},
                "time": search["time"] + len(path)
            })

    print(combos)
    return result


def part2(input: str) -> int:
    flow_rates = {}
    tunnels = {}

    for line in input.split("\n"):
        valve_info, tunnel_info = line.split("; ")
        valve = valve_info[len("Valve "):len("Valve ") + 2]
        flow_rate = int(valve_info.split()[-1].split('=')[1])
        next_tunnels = tunnel_info[len("tunnels lead to valve "):].split(", ")
        flow_rates[valve] = flow_rate
        if valve not in tunnels:
            tunnels[valve] = []
        for tunnel in next_tunnels:
            tunnels[valve].append(tunnel.strip())

    paths = {}
    non_zero_flow_rates = {name: flow_rate for name, flow_rate in flow_rates.items() if flow_rate > 0}
    for target in non_zero_flow_rates.keys():
        for source in flow_rates.keys():
            if source == target:
                continue

            if source not in paths:
                paths[source] = {}

            bfs = deque([((source,), 0)])
            visited = set()
            while len(bfs):
                path, distance = bfs.popleft()
                current = path[-1]

                visited.add(current)

                if current == target:
                    paths[source][target] = path[1:]
                    break

                for next in tunnels[current]:
                    if next in visited:
                        continue
                    bfs.append((path + (next,), distance + 1))

    dfs = deque([{
        "my_path": ("AA",),
        "my_time": 0,
        "elephant_path": ("AA",),
        "elephant_time": 0,
        "open_valves": {
            "AA": 0
        }
    }])

    # dfs = deque([{
    #     "my_path": ("AA", "JJ"),
    #     "my_time": 4,
    #     "elephant_path": ("AA", "DD"),
    #     "elephant_time": 3,
    #     "open_valves": {
    #         "AA": 0,
    #         "DD": 2,
    #         "JJ": 3
    #     }
    # }])

    result = 0
    combos = 0
    while len(dfs):
        search = dfs.pop()

        if len(search["my_path"]) == 2 and search["my_path"] == ("AA", "JJ") and search["elephant_path"] == ("AA", "DD"):
            print("break")

        if len(search["my_path"]) == 3 and search["my_path"] == ("AA", "JJ", "BB") and search["elephant_path"] == ("AA", "DD", "HH"):
            print("break")

        if len(search["my_path"]) == 4 and search["my_path"] == ("AA", "JJ", "BB", "CC") and search["elephant_path"] == ("AA", "DD", "HH", "EE"):
            print("break")

        if search["my_time"] >= 26 or search["elephant_time"] >= 26:
            combos += 1
            pressure = 0
            for valve, open_minute in search["open_valves"].items():
                pressure += (26 - open_minute) * flow_rates[valve]

            if pressure > result:
                result = pressure

            continue

        if search["my_path"][-1] not in search["open_valves"] \
                or search["elephant_path"][-1] not in search["open_valves"]:

            if search["my_path"][-1] not in search["open_valves"]:
                search["open_valves"][search["my_path"][-1]] = search["my_time"]
                search["my_time"] += 1

            if search["elephant_path"][-1] not in search["open_valves"]:
                search["open_valves"][search["elephant_path"][-1]] = search["elephant_time"]
                search["elephant_time"] += 1

            if len(search["open_valves"]) == len(non_zero_flow_rates) + 1:
                dfs.append({
                    "my_path": search["my_path"],
                    "my_time": 26,
                    "elephant_path": search["elephant_path"],
                    "elephant_time": 26,
                    "open_valves": search["open_valves"],
                })
            else:
                dfs.append({
                    "my_path": search["my_path"],
                    "my_time": search["my_time"],
                    "elephant_path": search["elephant_path"],
                    "elephant_time": search["elephant_time"],
                    "open_valves": {k: v for k, v in search["open_valves"].items()}
                })

            continue

        my_next = [path for target, path in paths[search["my_path"][-1]].items() if
                   target not in search["open_valves"]]
        elephant_next = [path for target, path in paths[search["elephant_path"][-1]].items() if
                         target not in search["open_valves"]]

        next_paths = []
        if not len(my_next):
            for elephant_next_path in elephant_next:
                next_paths.append((None, elephant_next_path))
        elif not len(elephant_next):
            for my_next_path in my_next:
                next_paths.append((my_next_path, None))
        else:
            pairs = set()
            for my_next_path in my_next:
                for elephant_next_path in elephant_next:
                    if my_next_path[-1] == elephant_next_path[-1]:
                        continue

                    key = tuple(sorted((my_next_path[-1], elephant_next_path[-1])))
                    if key in pairs:
                        continue

                    pairs.add(key)
                    next_paths.append((my_next_path, elephant_next_path))

        for my_next_path, elephant_next_path in next_paths:
            next_search = {
                "my_path": tuple(search["my_path"]),
                "my_time": search["my_time"],
                "elephant_path": tuple(search["elephant_path"]),
                "elephant_time": search["elephant_time"],
                "open_valves": {k: v for k, v in search["open_valves"].items()}
            }

            if my_next_path:
                next_search["my_path"] = search["my_path"] + (my_next_path[-1],)
                next_search["my_time"] = search["my_time"] + len(my_next_path)

            if elephant_next_path:
                next_search["elephant_path"] = search["elephant_path"] + (elephant_next_path[-1],)
                next_search["elephant_time"] = search["elephant_time"] + len(elephant_next_path)

            dfs.append(next_search)

    print(combos)
    return result


class Test(unittest.TestCase):

    def test_part_1(self):
        # search["path"] == ("AA", "DD", "BB", "JJ", "HH", "EE", "CC")
        # search["open_valves"] == {
        #     "AA": 0,
        #     "DD": 2,
        #     "BB": 5,
        #     "JJ": 9,
        #     "HH": 17,
        #     "EE": 21,
        #     "CC": 24
        # }
        self.assertEqual(1651, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        # search["open_valves"] == {
        #     "DD": 2,
        #     "JJ": 3,
        #     "BB": 7,
        #     "HH": 7,
        #     "CC": 9,
        #     "EE": 11
        # }
        # ("AA", "JJ", "BB", "CC") ("AA", "DD", "HH", "EE")
        # self.assertEqual(1707, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip("\n")
