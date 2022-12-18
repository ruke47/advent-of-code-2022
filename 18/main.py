adjacencies = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def load():
    grid = set()
    with open("input") as file:
        for line in file:
            x, y, z = [int(coord) for coord in line.strip().split(",")]
            grid.add((x, y, z))
    return grid


def part1():
    grid = load()
    exposed_faces = 0
    for (px, py, pz) in grid:
        for dx, dy, dz in adjacencies:
            neighbor = (px + dx, py + dy, pz + dz)
            if neighbor not in grid:
                exposed_faces += 1
    print(exposed_faces)


def build_solid(xb, xe, yb, ye, zb, ze, collector):
    for x in range(xb, xe + 1):
        for y in range(yb, ye + 1):
            for z in range(zb, ze + 1):
                collector.add((x, y, z))


def part2():
    lava = load()

    # figure out the bounding box for our lava
    max_x = max([x for x, y, z in lava])
    max_y = max([y for x, y, z in lava])
    max_z = max([z for x, y, z in lava])
    min_x = min([x for x, y, z in lava])
    min_y = min([y for x, y, z in lava])
    min_z = min([z for x, y, z in lava])

    # build a 1-wide shell around out lava: this is "outside"
    outside = set()
    build_solid(min_x - 1, min_x - 1, min_y - 1, max_y + 1, min_z - 1, max_z + 1, outside)
    build_solid(max_x + 1, max_x + 1, min_y - 1, max_y + 1, min_z - 1, max_z + 1, outside)
    build_solid(min_x - 1, max_x + 1, min_y - 1, min_y - 1, min_z - 1, max_z + 1, outside)
    build_solid(min_x - 1, max_x + 1, max_y + 1, max_y + 1, min_z - 1, max_z + 1, outside)
    build_solid(min_x - 1, max_x + 1, min_y - 1, max_y + 1, min_z - 1, min_z - 1, outside)
    build_solid(min_x - 1, max_x + 1, min_y - 1, max_y + 1, max_z + 1, max_z + 1, outside)

    # every pixel within our bounding block that isn't lava is a void. it may be interior or exterior
    bounding_block = set()
    build_solid(min_x, max_x, min_y, max_y, min_z, max_z, bounding_block)
    voids = bounding_block.difference(lava)

    # if a void is touching the outside, it's outside the solid
    # keep iterating until no new pixels are being moved outside
    while True:
        move_out = set()
        for void in voids:
            vx, vy, vz = void
            for dx, dy, dz in adjacencies:
                neighbor = (vx + dx, vy + dy, vz + dz)
                if neighbor in outside:
                    move_out.add(void)
                    outside.add(void)
        for void in move_out:
            voids.remove(void)
        if not move_out:
            break

    # fill in the interior void and run our original algorithm
    for void in voids:
        lava.add(void)

    exposed_faces = 0
    for (px, py, pz) in lava:
        for dx, dy, dz in adjacencies:
            neighbor = (px + dx, py + dy, pz + dz)
            if neighbor not in lava:
                exposed_faces += 1
    print(exposed_faces)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
