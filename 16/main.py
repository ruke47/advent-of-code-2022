import re

input_p = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)")


class Valve:
    def __init__(self, name, flow_rate, neighbors):
        self.name = name
        self.flow_rate = flow_rate
        self.neighbors_names = neighbors
        self.neighbors = None

    def find_neighbors(self, valves):
        self.neighbors = [valves[name] for name in self.neighbors_names]

    def __str__(self):
        return f"{self.name}({self.flow_rate}) -> {self.neighbors_names}"

    def __repr__(self):
        return f"{self.name}({self.flow_rate})"


def read_input():
    valves = {}
    with open("example") as file:
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

    return valves


def search(valve, current_path, open_nodes, fully_explored, current_score, time_left):
    if time_left <= 0:
        return []
    all_paths = []
    current_path.append(valve)
    all_paths.append((current_score, current_path))

    if all(n in current_path for n in valve.neighbors):
        fully_explored.add(valve)

    for n in valve.neighbors:
        has_loop = False
        for i in range(0, len(current_path) - 1):
            if (current_path[i], current_path[i+1]) == (valve, n):
                has_loop = True
                break
        if has_loop and n in fully_explored:
            continue
        for path in search(n, current_path.copy(), open_nodes.copy(), fully_explored.copy(), current_score, time_left - 1):
            all_paths.append(path)

    if valve.flow_rate > 0 and valve not in open_nodes:
        time_left -= 1
        current_score += valve.flow_rate * time_left
        open_nodes.add(valve)
        for n in valve.neighbors:
            has_loop = False
            for i in range(0, len(current_path) - 1):
                if (current_path[i], current_path[i + 1]) == (valve, n):
                    has_loop = True
                    break
            if has_loop and n in fully_explored:
                continue
            for path in search(n, current_path.copy(), open_nodes.copy(), fully_explored.copy(), current_score, time_left - 1):
                all_paths.append(path)

    return all_paths


def part1():
    valves = read_input()
    entry = valves['AA']
    all_paths = search(entry, [], set(), set(), 0, 30)
    all_paths.sort(key=lambda path: path[0])
    all_paths.reverse()
    print(all_paths[-1][0])


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
