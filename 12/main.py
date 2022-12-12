alphabet = "abcdefghijklmnopqrstuvwxyz"
heights = {char: idx for idx, char in enumerate(alphabet)}
heights['S'] = 0
heights['E'] = 25
max_distance = 1_000_000


class Node:
    def __init__(self, char, position, grid):
        self.height = heights[char]
        self.position = position
        self.distance = max_distance
        self.grid = grid

    def get_neighbors(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbors = []
        for dx, dy in directions:
            sx, sy = self.position
            tx = sx + dx
            ty = sy + dy
            t = (tx, ty)
            if t in self.grid:
                neighbors.append(self.grid[t])
        return neighbors


def get_fresh_grid():
    grid = {}
    start = None
    end = None
    with open("input") as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                grid[(x, y)] = Node(char, (x, y), grid)
                if char == 'S':
                    start = grid[(x, y)]
                elif char == 'E':
                    end = grid[(x, y)]

    return grid, start, end


def djykstra(end, grid):
    unvisited = set(grid.values())
    while end in unvisited:
        cur_node = min(unvisited, key=lambda node: node.distance)
        unvisited.remove(cur_node)
        for neighbor in cur_node.get_neighbors():
            if neighbor.height <= cur_node.height + 1:
                neighbor.distance = min(neighbor.distance, cur_node.distance + 1)

    print(end.distance)


def part1():
    grid, start, end = get_fresh_grid()
    start.distance = 0
    djykstra(end, grid)


def part2():
    grid, start, end = get_fresh_grid()
    potential_starts = [node for node in grid.values() if node.height == 0]
    for node in potential_starts:
        node.distance = 0

    djykstra(end, grid)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
