import json
import unittest
from collections import deque
from time import time
from itertools import permutations, combinations
from pathlib import Path
from queue import PriorityQueue


class Search:
    def __init__(self, start: str):
        self.path = [start]
        self.open_valves = {
            start: 0
        }
        self.time = 1

    def open_valve(self, valve):
        copy = Search(valve)
        copy.path = list(self.path)
        copy.open_valves = {k: v for k, v in self.open_valves.items()}
        copy.open_valves[valve] = self.time
        copy.time = self.time + 1
        return copy

    def follow_tunnel(self, path):
        copy = Search(path[-1])
        copy.path = self.path + [path[-1]]
        copy.open_valves = {k: v for k, v in self.open_valves.items()}
        copy.time = self.time + len(path)
        return copy

    def __str__(self):
        return f"Search(time={self.time} path={self.path}, open={self.open_valves})"


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

            bfs = deque([(source,)])
            visited = set()
            while len(bfs):
                path = bfs.popleft()
                current = path[-1]

                visited.add(current)

                if current == target:
                    paths[source][target] = path[1:]
                    break

                for next in tunnels[current]:
                    if next in visited:
                        continue
                    bfs.append(path + (next,))

    dfs = deque([Search("AA")])

    result = 0
    while len(dfs):
        search = dfs.pop()

        if search.time >= 30:
            pressure = 0
            for valve, open_minute in search.open_valves.items():
                pressure += (30 - open_minute) * flow_rates[valve]

            if pressure > result:
                result = pressure

            continue

        valve = search.path[-1]

        if valve not in search.open_valves:
            search = search.open_valve(valve)

            if len(search.open_valves) == len(non_zero_flow_rates) + 1:
                search.time = 30
                dfs.append(search)
            else:
                dfs.append(search)

            continue

        for target, path in paths[valve].items():
            if target in search.open_valves.keys():
                continue

            dfs.append(search.follow_tunnel(path))

    return result


class Search2:
    def __init__(self, start: str):
        self.my_path = [start]
        self.my_next_valve = None
        self.elephant_path = [start]
        self.elephant_next_valve = None
        self.open_valves = {
            start: 0
        }

    def copy(self):
        copy = Search2("")
        copy.my_path = list(self.my_path)
        copy.my_next_valve = self.my_next_valve
        copy.elephant_path = list(self.elephant_path)
        copy.elephant_next_valve = self.elephant_next_valve
        copy.open_valves = {k: v for k, v in self.open_valves.items()}
        return copy

    def __hash__(self) -> int:
        key = dict(self.open_valves)
        if self.my_next_valve is not None:
            key[self.my_next_valve[0]] = self.my_next_valve[1]
        if self.elephant_next_valve is not None:
            key[self.elephant_next_valve[0]] = self.elephant_next_valve[1]
        return hash(tuple((k, key[k]) for k in sorted(key.keys())))


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

            bfs = deque([(source,)])
            visited = set()
            while len(bfs):
                path = bfs.popleft()
                current = path[-1]

                visited.add(current)

                if current == target:
                    paths[source][target] = path[1:]
                    break

                for next in tunnels[current]:
                    if next in visited:
                        continue
                    bfs.append(path + (next,))

    searches_by_minute = {
        1: {Search2("AA")}
    }

    visited = set()
    complete_searches = []

    my_order = deque(["JJ", "BB", "CC"])
    elephant_order = deque(["DD", "HH", "EE"])

    for minute in range(1, 27):
        if minute not in searches_by_minute:
            print(minute, 0)
            continue

        searches = searches_by_minute[minute]
        print(minute, len(searches))

        while len(searches):
            search = searches.pop()

            if search.my_next_valve is not None and search.my_next_valve[1] == minute:
                # JJ 3, BB 7, CC 9
                search.my_path.append(search.my_next_valve[0])
                search.open_valves[search.my_path[-1]] = minute
                search.my_next_valve = None

            if search.elephant_next_valve is not None and search.elephant_next_valve[1] == minute:
                # DD 2, HH 7, EE 11
                search.elephant_path.append(search.elephant_next_valve[0])
                search.open_valves[search.elephant_path[-1]] = minute
                search.elephant_next_valve = None

            if len(search.open_valves) == len(non_zero_flow_rates) + 1:
                complete_searches.append(search)
                continue

            def should_open_valve(target):
                return all([
                    target not in search.open_valves,
                    search.my_next_valve is None or search.my_next_valve[0] != target,
                    search.elephant_next_valve is None or search.elephant_next_valve[0] != target,
                ])

            my_tunnels = [path for target, path in paths[search.my_path[-1]].items() if
                          should_open_valve(target)] if search.my_next_valve is None else []
            elephant_tunnels = [path for target, path in paths[search.elephant_path[-1]].items() if
                                should_open_valve(target)] if search.elephant_next_valve is None else []

            # try:
            #     my_tunnels = [paths[search.my_path[-1]][my_order.popleft()]] if search.my_next_valve is None else []
            # except IndexError:
            #     my_tunnels = []
            # try:
            #     elephant_tunnels = [paths[search.elephant_path[-1]][elephant_order.popleft()]] if search.elephant_next_valve is None else []
            # except IndexError:
            #     elephant_tunnels = []

            tunnels = set()

            if len(my_tunnels) == 0 and len(elephant_tunnels) == 0:
                next_minute = min([move[1] if move is not None else float('inf') for move in
                                   [search.my_next_valve, search.elephant_next_valve]])
                if (next_minute, search) not in visited:
                    searches_by_minute.setdefault(next_minute, set()).add(search)
                    visited.add((next_minute, search))
            elif len(elephant_tunnels) == 0 and len(my_tunnels) > 0:
                for my_tunnel in my_tunnels:
                    tunnels.add((my_tunnel, None))
            elif len(my_tunnels) == 0 and len(elephant_tunnels) > 0:
                for elephant_tunnel in elephant_tunnels:
                    tunnels.add((None, elephant_tunnel))
            elif len(my_tunnels) > 0 and len(elephant_tunnels) > 0:
                for my_tunnel in my_tunnels:
                    for elephant_tunnel in elephant_tunnels:
                        if elephant_tunnel[-1] != my_tunnel[-1]:
                            tunnels.add((my_tunnel, elephant_tunnel))

            for my_tunnel, elephant_tunnel in tunnels:
                new_search = search.copy()
                search_key = dict(search.open_valves)

                if my_tunnel is not None:
                    new_search.my_next_valve = (my_tunnel[-1], minute + len(my_tunnel) + (0 if minute == 1 else 1))
                    search_key[new_search.my_next_valve[0]] = new_search.my_next_valve[1]
                if elephant_tunnel is not None:
                    new_search.elephant_next_valve = (
                        elephant_tunnel[-1], minute + len(elephant_tunnel) + (0 if minute == 1 else 1))
                    search_key[new_search.elephant_next_valve[0]] = new_search.elephant_next_valve[1]

                next_minute = min([move[1] if move is not None else float('inf') for move in
                                   [new_search.my_next_valve, new_search.elephant_next_valve]])

                if (next_minute, new_search) not in visited:
                    searches_by_minute.setdefault(next_minute, set()).add(new_search)
                    visited.add((next_minute, new_search))

    # dfs = deque([(Search("AA"), Search("AA"))])
    # result = 0
    # now = time()
    # states = {}
    #
    # while len(dfs):
    #     me, elephant = dfs.pop()
    #
    #     state_key = tuple(
    #         sorted(set(me.open_valves.keys()).union([me.path[-1]], [elephant.path[-1]], elephant.open_valves.keys())))
    #     state_time = max(me.time, elephant.time)
    #     print(state_key, state_time)
    #     if state_key in states and states[state_key] < state_time:
    #         print("SKIP")
    #         continue
    #
    #     states[state_key] = state_time
    #
    #     if time() - 1 > now:
    #         print(len(dfs))
    #         now = time()
    #
    #     if me.time >= 26 or elephant.time >= 26:
    #         pressure = 0
    #         for search in [me, elephant]:
    #             for valve, open_minute in search.open_valves.items():
    #                 pressure += (26 - open_minute) * flow_rates[valve]
    #
    #         if pressure > result:
    #             result = pressure
    #
    #         continue
    #
    #     i_opened_valve = False
    #     my_valve = me.path[-1]
    #
    #     if my_valve not in me.open_valves:
    #         me = me.open_valve(my_valve)
    #         i_opened_valve = True
    #
    #         if len(me.open_valves) + len(elephant.open_valves) == len(non_zero_flow_rates) + 1:
    #             me.time = 30
    #
    #         dfs.append((me, elephant))
    #
    #     elephant_opened_valve = False
    #     elephant_value = elephant.path[-1]
    #
    #     if elephant_value not in elephant.open_valves:
    #         elephant = elephant.open_valve(elephant_value)
    #         elephant_opened_valve = True
    #
    #         if len(elephant.open_valves) + len(me.open_valves) == len(non_zero_flow_rates) + 1:
    #             elephant.time = 30
    #
    #         dfs.append((me, elephant))
    #
    #     tunnels = set()
    #     my_paths = [] if i_opened_valve else paths[me.path[-1]].items()
    #     elephant_paths = [] if elephant_opened_valve else paths[elephant.path[-1]].items()
    #
    #     if len(elephant_paths) == 0 and len(my_paths) == 0:
    #         continue
    #     if len(elephant_paths) == 0:
    #         for my_target, my_tunnel in my_paths:
    #             if my_target not in me.open_valves and my_target not in elephant.open_valves:
    #                 tunnels.add((my_tunnel, None))
    #     elif len(my_paths) == 0:
    #         for elephant_target, elephant_tunnel in elephant_paths:
    #             if elephant_target not in me.open_valves and elephant_target not in elephant.open_valves:
    #                 tunnels.add((None, elephant_tunnel))
    #     else:
    #         for my_target, my_tunnel in my_paths:
    #             for elephant_target, elephant_tunnel in elephant_paths:
    #                 if elephant_target != my_target \
    #                         and my_target not in me.open_valves and my_target not in elephant.open_valves \
    #                         and elephant_target not in me.open_valves and elephant_target not in elephant.open_valves:
    #                     tunnels.add((my_tunnel, elephant_tunnel))
    #
    #     for my_tunnel, elephant_tunnel in list(tunnels):
    #         my_next_search, elephant_next_search = me, elephant
    #         if my_tunnel:
    #             my_next_search = my_next_search.follow_tunnel(my_tunnel)
    #         if elephant_tunnel:
    #             elephant_next_search = elephant_next_search.follow_tunnel(elephant_tunnel)
    #
    #         dfs.append((my_next_search, elephant_next_search))

    print(len(complete_searches))
    result = 0
    for search in complete_searches:
        pressure = 0
        for valve, open_minute in search.open_valves.items():
            pressure += (26 - open_minute) * flow_rates[valve]

        if pressure > result:
            result = pressure

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
        # search.open_valves == {
        #     "DD": 2,
        #     "JJ": 3,
        #     "BB": 7,
        #     "HH": 7,
        #     "CC": 9,
        #     "EE": 11
        # }
        # me JJ BB CC
        # elephant DD HH EE
        self.assertEqual(1707, part2(Test.example))

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
