class Tree:
    def __init__(self, height, position, grid):
        self.height = height
        self.position = position
        self.grid = grid
        self.is_visible = False
        self.scenicness = 0

    def prop_tallness(self, dx, dy, tallest=-1):
        if self.height > tallest:
            self.is_visible = True
            tallest = self.height
        tx = self.position[0] + dx
        ty = self.position[1] + dy
        if (tx, ty) in self.grid:
            self.grid[(tx, ty)].prop_tallness(dx, dy, tallest)

    def calc_scene(self):
        self.scenicness = self.calc_vis(0, 1) * self.calc_vis(0, -1) * self.calc_vis(1, 0) * self.calc_vis(-1, 0)

    def calc_vis(self, dx, dy):
        vis = 0
        tx = self.position[0] + dx
        ty = self.position[1] + dy
        while (tx, ty) in self.grid:
            vis += 1
            target = self.grid[(tx, ty)]
            if target.height >= self.height:
                break
            else:
                tx += dx
                ty += dy
        return vis


def main():
    grid = {}
    with open("input") as file:
        for x, line in enumerate(file):
            for y, val in enumerate(line.strip()):
                grid[(x, y)] = Tree(int(val), (x, y), grid)

    for x in range(99):
        grid[(x, 0)].prop_tallness(0, 1)
    for x in range(99)[::-1]:
        grid[(x, 98)].prop_tallness(0, -1)
    for y in range(99):
        grid[(0, y)].prop_tallness(1, 0)
    for y in range(99)[::-1]:
        grid[(98, y)].prop_tallness(-1, 0)

    visible = sum(1 for tree in grid.values() if tree.is_visible)
    print(visible)

    for x in range(99):
        for y in range(99):
            grid[(x, y)].calc_scene()

    print(max([tree.scenicness for tree in grid.values()]))


if __name__ == '__main__':
    main()
