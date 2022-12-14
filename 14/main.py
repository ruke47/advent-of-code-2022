
rock = "█"
sand = "o"

class Grid:
    def __init__(self):
        self.obstructions = {}
        self.kill_plane = 0
        self.held_sand = 0
        self.floor = 0

    def run(self, has_floor):
        self.floor = self.kill_plane + 1
        while self.drop_sand(has_floor):
            pass
        return self.held_sand

    def drop_sand(self, has_floor):
        sx, sy = 500, 0
        while True:
            if has_floor:
                if sy == self.floor:
                    self.obstructions[(sx, sy)] = sand
                    self.held_sand += 1
                    return True
            else:
                if sy > self.kill_plane:
                    return False

            down = sx, sy + 1
            downl = sx - 1, sy + 1
            downr = sx + 1, sy + 1
            if down not in self.obstructions:
                sx, sy = down
            elif downl not in self.obstructions:
                sx, sy = downl
            elif downr not in self.obstructions:
                sx, sy = downr
            else:
                break
        self.obstructions[(sx, sy)] = sand
        self.held_sand += 1
        if (sx, sy) == (500, 0):
            return False
        else:
            return True

    def load_line(self, begin, end):
        bx, by = begin
        ex, ey = end
        if bx == ex:
            self.load_horizontal_line(bx, by, ey)
        elif by == ey:
            self.load_vertical_line(by, bx, ex)
        else:
            raise f"Line from {begin} -> {end} is neither horizontal nor vertical"

        self.kill_plane = max(self.kill_plane, by, ey)

    def load_horizontal_line(self, x, by, ey):
        if by < ey:
            ly, hy = by, ey
        else:
            ly, hy = ey, by

        for y in range(ly, hy + 1):
            self.obstructions[(x, y)] = rock

    def load_vertical_line(self, y, bx, ex):
        if bx < ex:
            lx, hx = bx, ex
        else:
            lx, hx = ex, bx
        for x in range(lx, hx + 1):
            self.obstructions[(x, y)] = rock


def parse_point(point_str):
    return [int(number) for number in point_str.split(",")]


def load_grid():
    grid = Grid()
    with open("input") as file:
        for line in file:
            points = line.strip().split(" -> ")
            for idx in range(len(points) - 1):
                begin = parse_point(points[idx])
                end = parse_point(points[idx + 1])
                grid.load_line(begin, end)
    return grid


def part1():
    grid = load_grid()
    print(grid.run(False))


def part2():
    grid = load_grid()
    print(grid.run(True))


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
