from itertools import cycle, repeat
from collections.abc import Iterable, Iterator


class Shape:
    def __init__(self, points: list[(int, int)], read_only=False):
        self.points = points
        self.read_only = read_only

    def __copy__(self):
        return Shape(self.points.copy())

    def __str__(self):
        return f"{self.points}"

    def __repr__(self):
        return self.__str__()

    def initialize(self, grid: "Grid"):
        if self.read_only:
            raise "Don't touch the read_only shapes!"
        self.points = [(x, y + grid.max_y) for x, y in self.points]

    def move_down(self, grid: "Grid"):
        if self.read_only:
            raise "Don't touch the read_only shapes!"
        new_points = [(x, y - 1) for x, y in self.points]
        if any(point in grid.obstructions for point in new_points):
            return False
        if any(y < grid.min_y for x, y in new_points):
            return False
        self.points = new_points
        return True

    def move_side(self, direction: str, grid: "Grid"):
        if self.read_only:
            raise "Don't touch the read_only shapes!"

        if direction == '>':
            new_points = [(x + 1, y) for x, y in self.points]
            if any(x > grid.max_x for x, y in new_points):
                return False
        elif direction == '<':
            new_points = [(x - 1, y) for x, y in self.points]
            if any(x < grid.min_y for x, y in new_points):
                return False
        else:
            raise f"Bad Direction {direction}"

        if any(point in grid.obstructions for point in new_points):
            return False
        self.points = new_points
        return True


class Grid:
    def __init__(self, width: int):
        self.min_y = 0
        self.max_y = -1
        self.min_x = 0
        self.max_x = width - 1
        self.obstructions = set()

    def land(self, shape: Shape):
        for point in shape.points:
            self.max_y = max(self.max_y, max(y for x, y in shape.points))
            self.obstructions.add(point)


def load_shapes() -> Iterable[Shape]:
    return cycle([
        Shape([(2, 4), (3, 4), (4, 4), (5, 4)], read_only=True),
        Shape([(2, 5), (3, 5), (4, 5), (3, 4), (3, 6)], read_only=True),
        Shape([(2, 4), (3, 4), (4, 4), (4, 5), (4, 6)], read_only=True),
        Shape([(2, 4), (2, 5), (2, 6), (2, 7)], read_only=True),
        Shape([(2, 4), (2, 5), (3, 4), (3, 5)], read_only=True)
    ])


def load_wind() -> (Iterator[str], int):
    with open("input") as file:
        wind_loop = file.readline().strip()
        return cycle(wind_loop), len(wind_loop)


def part1():
    grid = Grid(7)
    wind, wind_len = load_wind()
    for drop_num, shape_template in enumerate(load_shapes()):
        if drop_num == 2022:
            break
        cur_shape = shape_template.__copy__()
        cur_shape.initialize(grid)
        while True:
            cur_shape.move_side(next(wind), grid)
            if not cur_shape.move_down(grid):
                grid.land(cur_shape)
                break
    print(grid.max_y + 1)


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
