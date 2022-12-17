import re
from collections.abc import Iterable

input_p = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)")
tap = "🚰"

class Valve:
    next_valve_id = 1

    def __init__(self, name: str, flow_rate: int, neighbors: list[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors_names = neighbors
        self.neighbors = None
        self.distance_to = {}
        self.valve_id = 0
        if flow_rate > 0:
            self.valve_id = Valve.next_valve_id
            Valve.next_valve_id *= 2

    def find_neighbors(self, valves: dict[str, "Valve"]):
        self.neighbors = [valves[name] for name in self.neighbors_names]

    def find_distance_to_others(self, valves: Iterable["Valve"]):
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
    def __init__(self, valve: Valve):
        self.valve = valve
        self.distance = 100

    def __str__(self):
        return f"{self.valve.name}: {self.distance}"

    def __repr__(self):
        self.__str__()


def find_distance(start: Valve, end: Valve, all_valves: Iterable[Valve]):
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


class GameState:
    def __init__(self, position: Valve, valves_enabled: int, time_left: int, score: int, history=[], is_move_action=True):
        self.position = position
        self.valves_enabled = valves_enabled
        self.time_left = time_left
        self.score = score
        self.history = history.copy()
        if is_move_action:
            self.history.append(position.name)
        else:
            self.history.append(tap)

    def __str__(self):
        return f"[{self.position.name}]({self.time_left} - {self.valves_enabled}]: {self.score}";

    def __repr__(self):
        return self.__str__()

    def is_better_than(self, other: "GameState"):
        i_have_equal_valves = self.valves_enabled & other.valves_enabled == other.valves_enabled
        # i_have_equal_vales = self.valves_enabled == other.valves_enabled
        if i_have_equal_valves and self.time_left >= other.time_left and self.score >= other.score:
            return True
        return False

    def already_opened_valve(self):
        if self.position.flow_rate == 0:
            return True
        if self.position.valve_id & self.valves_enabled == self.position.valve_id:
            return True
        return False

    def state_with_valve_open(self):
        new_enabled = self.valves_enabled | self.position.valve_id
        new_time_left = self.time_left - 1
        new_score = new_time_left * self.position.flow_rate + self.score
        if new_time_left > 0:
            return GameState(self.position, new_enabled, new_time_left, new_score, self.history, is_move_action=False)
        else:
            return None

    def state_with_move_to(self, neighbor: Valve):
        if neighbor not in self.position.neighbors:
            raise f"Cannot move from {self.position} to {neighbor}"
        if self.valves_enabled == Valve.next_valve_id - 1:
            # if all valves are open, stop running around
            return None
        if self.time_left > 1:
            return GameState(neighbor, self.valves_enabled, self.time_left - 1, self.score, self.history)
        else:
            return None


def no_better_positions(new_state: GameState, good_position_map: dict[str, list[GameState]]):
    good_positions = good_position_map[new_state.position.name]
    if any(other.is_better_than(new_state) for other in good_positions):
        return False
    else:
        not_worse_positions = [position for position in good_positions if not new_state.is_better_than(position)]
        not_worse_positions.append(new_state)
        good_position_map[new_state.position.name] = not_worse_positions
        return True


def explore_map(start_node: Valve, valve_map: dict[str, Valve], time: int):
    seen_positions = {valve.name: [] for valve in valve_map.values()}
    initial_state = GameState(start_node, 0, time, 0)
    seen_positions[start_node.name].append(initial_state)
    to_explore = [initial_state]
    comparisons = 0
    while to_explore:
        comparisons += 1
        cur_state = to_explore.pop()
        for neighbor_position in cur_state.position.neighbors:
            new_state = cur_state.state_with_move_to(neighbor_position)
            if new_state and no_better_positions(new_state, seen_positions):
                to_explore.append(new_state)
        if not cur_state.already_opened_valve():
            new_state = cur_state.state_with_valve_open()
            if new_state and no_better_positions(new_state, seen_positions):
                to_explore.append(new_state)
    best_position = initial_state
    for position_list in seen_positions.values():
        for position in position_list:
            best_position = max(best_position, position, key=lambda state: state.score)

    return best_position.score


def part1():
    valves = read_input()
    # TODO: start with a stack of [(starting_position, enabled_faucets)]
    # pop a reached-state off of the stack, and for each neighbor, consider whether you've been
    # in that (location, enabled-faucets|potential-points) before, but had more time left. Only if you have not,
    # push that next-state onto the stack.
    entry = valves['AA']
    score = explore_map(entry, valves, 30)
    print(score)


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
