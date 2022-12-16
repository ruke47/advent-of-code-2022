import re
from itertools import permutations

input_p = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)")


class Valve:
    def __init__(self, name, flow_rate, neighbors):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors_names = neighbors
        self.neighbors = None
        self.distance_to = {}

    def find_neighbors(self, valves):
        self.neighbors = [valves[name] for name in self.neighbors_names]

    def find_distance_to_others(self, valves):
        for valve in valves:
            if valve == self:
                self.distance_to[self.name] = 0
            elif self.name in valve.distance_to:
                self.distance_to[valve.name] = valve.distance_to[self.name]
            else:
                self.distance_to[valve.name] = find_distance(self, valve, valves)

    def __str__(self):
        return f"{self.name}({self.flow_rate}) -> {self.neighbors_names}"

    def __repr__(self):
        return f"{self.name}({self.flow_rate})"


class Node:
    def __init__(self, valve):
        self.valve = valve
        self.distance = 100

    def __str__(self):
        return f"{self.valve.name}: {self.distance}"

    def __repr__(self):
        self.__str__()


def find_distance(start, end, all_valves):
    nodes = {valve.name: Node(valve) for valve in all_valves}
    nodes[start.name].distance = 0
    unvisited = set(nodes.values())
    while nodes[end.name] in unvisited:
        cur_node = min(unvisited, key=lambda node: node.distance)
        unvisited.remove(cur_node)
        for neighbor in cur_node.valve.neighbors:
            neighbor_node = nodes[neighbor.name]
            neighbor_node.distance = min(neighbor_node.distance, cur_node.distance + 1)

    return nodes[end.name].distance


def read_input():
    valves = {}
    with open("input") as file:
        for line in file:
            match = input_p.fullmatch(line.strip())
            if not match:
                raise f"Line did not match format: {line}"
            name = match.group(1)
            rate = int(match.group(2))
            neighbors = match.group(3).split(", ")
            valves[name] = Valve(name, rate, neighbors)
    for valve in valves.values():
        valve.find_neighbors(valves)
    for valve in valves.values():
        valve.find_distance_to_others(valves.values())

    return valves


def rush_valves(start_node, unopened_valves, time):
    valve_orders = permutations(unopened_valves)
    max_score = 0
    for i, order in enumerate(valve_orders):
        if i % 1_000_000 == 0:
            print(f"\t - {i}")
        score = 0
        cur_node = start_node
        time_left = time
        for valve in order:
            time_cost = cur_node.distance_to[valve.name] + 1
            time_left -= time_cost
            score += valve.flow_rate * time_left
            cur_node = valve
        max_score = max(max_score, score)
    return max_score


def part1():
    valves = read_input()
    entry = valves['AA']
    unopened_valves = set(valve for valve in valves.values() if valve.flow_rate > 0)
    score = rush_valves(entry, unopened_valves, 30)
    print(score)


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
