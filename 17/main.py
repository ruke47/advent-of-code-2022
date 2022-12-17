from itertools import cycle
from collections.abc import Iterable, Iterator
from math import floor
from time import time

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
    def __init__(self, width: int, wind_length):
        self.width = width
        self.wind_length = wind_length
        self.min_y = 0
        self.max_y = -1
        self.min_x = 0
        self.max_x = width - 1
        self.obstructions = set()
        self.column_rel_heights = {}
        self.cycle_id = -1
        self.all_heights = []

    def height(self):
        return self.max_y + 1

    def drop_shape(self, shape_template: Shape, wind: Iterator[str]):
        self.cycle_id += 1
        cur_shape = shape_template.__copy__()
        cur_shape.initialize(self)
        while True:
            cur_shape.move_side(next(wind), self)
            if not cur_shape.move_down(self):
                self.land(cur_shape)
                self.all_heights.append(self.height())
                break

    def land(self, shape: Shape):
        for point in shape.points:
            self.max_y = max(self.max_y, max(y for x, y in shape.points))
            self.obstructions.add(point)

    def check_relative_heights(self):
        highest_point = {x: -1 for x in range(0, self.width)}
        for x, y in self.obstructions:
            highest_point[x] = max(highest_point[x], y)
        normalized_floor = min(highest_point.values())

        if self.cycle_id % self.wind_length == 0:
            normalized_heights = []
            for x in range(0, self.width):
                normalized_heights.append(highest_point[x] - normalized_floor)
            normalized_heights = tuple(normalized_heights)

            if normalized_heights in self.column_rel_heights:
                return self.column_rel_heights[normalized_heights]
            else:
                self.column_rel_heights[normalized_heights] = (self.cycle_id, self.height())
                return None
        elif self.cycle_id % 1000 == 0:
            # discard everything beneath the highest point in each column
            self.obstructions = set((x, y) for x, y in self.obstructions if y >= normalized_floor)
        return None


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


def part1(cutoff: int):
    wind, wind_len = load_wind()
    grid = Grid(7, wind_len)
    for drop_num, shape_template in enumerate(load_shapes()):
        if drop_num == cutoff:
            break
        grid.drop_shape(shape_template, wind)
    return grid


def part2():
    mega_cycles = 1_000_000_000_000
    wind, wind_len = load_wind()
    grid = Grid(7, wind_len)
    for drop_num, shape_template in enumerate(load_shapes()):
        grid.drop_shape(shape_template, wind)
        if drop_num % 1000 != 0 and drop_num % wind_len != 0:
            continue
        loop_state = grid.check_relative_heights()
        if loop_state:
            loop_begin_idx, before_loop_height = loop_state
            loop_height = grid.height() - before_loop_height
            loop_length = drop_num - loop_begin_idx

            cycles_remaining = floor((mega_cycles - drop_num - 1) / loop_length)
            remaining_cycle_height = cycles_remaining * loop_height

            leftover_cycles = (mega_cycles - drop_num - 1) % loop_length
            leftover_cycle_height = grid.all_heights[loop_begin_idx + leftover_cycles] - before_loop_height

            total_height = grid.height() + remaining_cycle_height + leftover_cycle_height
            print(f"Loop on cycles {loop_begin_idx} - {drop_num}. Loop will repeat {cycles_remaining} more times.")
            print(f"\tBefore-loop height: {before_loop_height}")
            print(f"\tLoop-height: {loop_height}")
            print(f"\tLoop-length: {loop_length}")
            print(f"\tLeftover cycles: {leftover_cycles}")
            print(f"\tLeftover Height: {leftover_cycle_height}")
            print(f"Total Height: {total_height}")
            break




def main():
    print(part1(2022).height())
    begin = time()
    part2()
    time_took = time() - begin
    print(f"Took {floor(time_took/60)}m {floor(time_took) % 60}s")


if __name__ == '__main__':
    main()
