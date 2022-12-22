import re
import unittest

ex_instr = "10R5L5R10L4R5L5"
inp_instr = "38R8R43L19L6R32L6L5R31R4R34R11L43R44L37R42L15L45L47L42R2L14L43R9R6R31L35L30R23R25R3L18R47R20R13R47R6R3R36L39R17R22R20L26R33L41R2R28L24R25R13L26L1R19L4L16L13R30R1L15R21L50R1R28R36R33R45L35L19L3L11L42L25L4R49R36L25R43R41R41R18L39L46L12L40L39R8L41L27R38L41R1L9L38R7L15L42L27L24L15L10R36L7R30L23L1L50R25L12R16R17L49R49L17R14R1R38L13R25R22R21L11R8L9L6R3R24L46L28L24R2L23R13L45R9L14L29R41R10R3R18L44R27L34L25R10R18L8R47R9L39L19L39L16R46L18L10R24L10R11L16R44L8R16R35L45R5L13L31L44L16L24L23R23R27R12L46R1R10R27L4R15L8R40L17L43L33R41L29L34L17L46R34R26L22R48L12R23L50L32R7R44L2R18R1R4R22R11L6R32L19L17L49L41L31L25L10R41L37L9L30R33R31R23L25R12R8R10L33L42L42L4L11L23R11L31L21R9L22R23L12L42L42R50L4L35L22R40L35R1L34R22R37L47L34L2L15R41R12L29R24R16L2R46R28L11R23R30L10L6L47L3R9R21R49L17R13R10L10R41L31L19L42R8R10R18R22R38L2L3R17R39L49R42R26L22R28R47L41R26R29R44R12L40L20R17L48R47R48L36R38L45L22L6L10R1R22R40L36R15L48L15R23R1L16R50L48L21R45R48L39R45R13R3R12R43L48R21R9L44R24R40L33R13R48R22L31R22L6L21R12R26L38R49L24L46R4L6L8R2R14R1L29L28L18L8R25L29L41R1R13R31R28L23L35R1L13L15L2R32L9R46R37R27L2L30L8R27R45R42L42L42R19R5R32R35L37R2R25R36L21L50R47L6L10L38L39L14R32R27R15L42L14L11L17L2L50R41L18R34L20L29L31L9L3R36L18R8R28R33L9L35R20L8L24L18L39R31L49L34L9L11R44L36R22R19L12L34R16R44R19R17L27L36R10L33L46L18L5L7R45R6L38R18R39R31L11L45R17L39L48R4L10L9L4L10R46R28R32R46L18R11L40L33L44R28L39R2R49R8R21L50R49L42L35R40R6R33L19R43R11R14L26L23L8R43R18L16L19R27L43L1R27L24R11L39L22R44L47L17L35L47R31R18L11R3L2R23R6L37L5R3L41L41R20R4L39L22R50R31R10L14R40L12L3R24L33R14R27R29L22L1L8L17L23L21L47L34L46R32L24R37R39R22R36R37R24R3L21L10L49R21L12R39L27R23R41R41L41L32R4R32R26R35L31R16R7L33R48R5R17R47L41R26L34R36L49L46R49R49R34L48R5L37L32L11R13R42R28R18R44R3L48L13R19R45L11R44R30R29R39L29R11R16L6R35L31L16L39R11L11L41L11L5R16R8L50R15R21R45R17L9R22R23L40R15R43L7L48R1L2R45R35R35R32L8R7L34L9R27R8R47R18R10R45R27L21R4L36L44R8R35R5R39R29L43R45L48L21L13R45L44R27R42R22L3L24L31L16R42L46L46R9L35L23L40R9R5R44L10L38L43L47L21R37R20L23L39L20L37R21R47R37R18R11L37R41L18L2R16L37L10R49R50R11L20L49R3L32L3R49R12L20R12R24R4R7L35R47R10R38L31R24L31L25R32R21L48L45R27L9R10L25L4R44R7L27L33L9R8R47L4L12L47L21L29L43L29R36L35L24L21R26R20R14L26L22R14L8L45L5R20R31R33R10L9R31L37R5R12L7R8R43L9R46R11R29R26R1L46L1L42L19L27L7L27R25L44R22R21R50R22R42L10R19R47R39L42R46R31R36R46L37L23L33R8L1R40R6L38R16L37L30R25R11R41R15L46R3L36L18R8R45L23L10L37R32R38R28L27L43L36L16R27L1R27R38R7R19R36R38L2L25L3L18L25L26L29L16L8R29L22R42L17R30R38R3R32L37L10L26L38R31R1R26L17L41L44L27L20R50L27R39R31L40R16L39L7R34R10L43L49L5L6R13L24L3L7L11L34R24L43L44R45R33L32R25L21R32R5L21L27R34L19R23R43L23R28L35R14R10R23L43R43R50L31R50R1L10R37R3R38R32L7R42L29R44R18R3L33R30L26L16R34R50R27R34R4R11L3R13R36R5L50L41L3L15R16L43L36L47R31R10L33R36R3L35L12L14L7L47L36L49R37L9R8L14L5R41R35L20R47R49R46R29R8R7R35L7R41R46R22R20L34R28L25L3R47L6L40L40R11R21L15L32L35L44L16L3R1R46L29R47R16L14R41L1L50R44L12L18R7L18R3R23L36R34R4R3L34R32L40R15R5L6L40R49R38R15L33R38R14R3R32R41R23L4R3R5R33L39L10L33L45R43L36L24L39L4R33L38R4L29L27L44L4R5R2L49L12R37R4R21R20R50L39R39L18L38R16R15L38L16R49R33R1L48L11L15L39L11L1L27L26L47L38R28L44L9R18L28L4R22L24R48R8R5R47L8R23L16L1R26R16R16R8R23L21R44R42L23R17L18L31L12R37L40R14L46R28R28R46L8L37L28L35R25L27R19R24L5R33L42L10L7R37L25L44R16R10L23L10R40R45R48R5R19L5R44L6L16R34R29R11L32L24L9L25R49R1R2L41R46R29R3L31L1R6R30R23L35R45R19L26L6L4R1L6L38R45L13L34R4R38L42R47R14R39R37R45R1R50R47L13R38R5L21L12R6R37R22R23R16L4L34R5R8R12R3L11L8L50L23R19L10R41L26L1R11L1L29R42R6R28R33R8R30L3L8R43R6R45L23R38R42L7L27R47L48L20R49L8L21L38L40R17L49R22R48R45L49L19L44R50R48L19L26L15R12L17R38R46R14L1R18L50R21R21L7L42L14R14R19L16R36R6R41R21L13R44R25L6L18R8L35R39R2R4L1R21L42R2R29R40L40L38R5R17R36L25L49L24R17L34L4L30R6L49R12R27L31L22L27R7L26L5L18R39R31R28R25R11L27R4R43L5L4L36L6L13L11R36L20L50L46R4R44R11R16R45R42L9R1L9L44R15L14R9R4R16L36L42R48R17R19L41R41R16R26R9R37R43L26L5L11L31L23L26R28L5L35R47R45R7L26R41L15R15L38R22R41R14R32R49R15R41R20R14L7L41L21L5R45R11L11L19R39R31R36L32L9R16R30L37R31L27L23L46L18L28L13R16L19R8L25L15L32R35L5L8L28L44L9R22R4L8L41R13R9L29R20L5L29R41R43R2L2L10L34L13L29R9L12R2L38L25L5L46L48R42R6R27R44R7R38L38L28L1R44R5R38L43R9L6L7R22R30R7L1R1L6L26R29R45R41L12R41L18R5R21L1R7R4R25R5L15R14L43R43L1L31L32R41R12L4L18L40R10R11R48L27L45L32R11R45L23R10L1L2R12R20L42L27L39L39L14R41L44L4R48L18R28R27L5R30R47R37R4L18L32L40L3R13R32R2L43L29L6L33R4R37L7R36L46R24L48L29L18L48R27R41L49L19R49L22R27L27L40L21L19R45R38L22L1R15R13R23L18R23L25R29L12R19L45L23L28R40L33R5L6L31R18L48L50R15R21L29R20L39L40R39L45L34R45L10L8L17R30L43R33R19L29R38R49R8L37L47R29L14L42L6R25R17L27R21L3R2R3R11L14R42L33R15L30L4L47R4R17R42R46R44R36L38L5R3L28L46L9R32L33L34L39R33L4L22R13L27R14R39R26R17R5L31R47L33R45L41R46L15R7R33L7L43L31R24R50L14R7R13L4R45L27L6L35R25R13L36L45L14R6R44L29L25L18L36R6L28R3R29R36R41L11L40L47R10L50R47L16L8L11L40L48L39L30L39L29R37R44L21L18L30R41R5L2R11R36R39R9R37L37R37R2R8R48L25L17R45L39L21L10R40L14R46L32L11L26L34R20R40R43R18R38R13R19L4R48L17L41L16R11R6R42L15R30R19L17L25L27R19L47L27R11L9L46L28R50L16L10L47R17R24R14R16R15L32R20L49L3R37R19R36R24R22L33L15L39L19R6L29R41L28L42R14R47L6L41R15R9L4R7L6R28L23L31L41R25L48R25L25L22R19R25R21R25R46L9L12R11R26R7L22R46L6R25L44R35L12R16L41R39R11L38L40L48R43L14L46R22L38L42L4R22L23R9L19R32L14L36L41L44R11R2R30R27R6R17R13R34R23R7R17R28L14L12L31R18R13L15L25R29R30L42L14L46R45R13R45R38L50R40L2R12R9L1R43R4L39R7L30L10R20R11L35R11L2L21L14L41L38R22R31R26R45L17L28R28L5R20L28L8L42R9R22R42R27L8L36L34L29L3R8L15L21R49L13R25L9R4R49R15L22L18R11L14R11R38R12R35R41R20R21R43R27L13L29R2R23R32R13L25L26R9R15R27R29L39L21R27R1L20L4L25L48L9R49R29R33L38R30R6L27R41R28L50L44L33R42R47L44L22R7";
example = False
passable = "."
blocked = "#"

Direction = (int, int)
Position = (int, int)

facings = ((1, 0), (0, 1), (-1, 0), (0, -1))
right = facings[0]
down = facings[1]
left = facings[2]
up = facings[3]

facing_names = {
    right: "right",
    down: "down",
    left: "left",
    up: "up"
}

facing_points = {
    right: 0,
    down: 1,
    left: 2,
    up: 3
}

class Face:
    def __init__(self, name, x_begin, y_begin):
        self.name = name
        self.min_x = x_begin
        self.min_y = y_begin
        self.max_x = x_begin + 49
        self.max_y = y_begin + 49
        self.neighbors = {}
        self.transforms = {}
        self.facing_after = {}

    def contains_position(self, x, y):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def relative_x(self, x):
        return x - self.min_x

    def relative_y(self, y):
        return y - self.min_y


def initialize_cube() -> dict[int, Face]:
    faces = {
        1: Face(1, 101, 1),
        2: Face(2, 51, 1),
        3: Face(3, 51, 51),
        4: Face(4, 51, 101),
        5: Face(5, 1, 101),
        6: Face(6, 1, 151)
    }

    faces[1].neighbors[down] = faces[3]
    faces[1].transforms[down] = lambda cx, cy: (faces[3].max_x, faces[3].min_y + faces[1].relative_x(cx))
    faces[1].facing_after[down] = left

    faces[1].neighbors[right] = faces[4]
    faces[1].transforms[right] = lambda cx, cy: (faces[4].max_x, faces[4].max_y - faces[1].relative_y(cy))
    faces[1].facing_after[right] = left

    faces[1].neighbors[up] = faces[6]
    faces[1].transforms[up] = lambda cx, cy: (faces[6].min_x + faces[1].relative_x(cx), faces[6].max_y)
    faces[1].facing_after[up] = up

    faces[2].neighbors[up] = faces[6]
    faces[2].transforms[up] = lambda cx, cy: (faces[6].min_x, faces[6].min_y + faces[2].relative_x(cx))
    faces[2].facing_after[up] = right

    faces[2].neighbors[left] = faces[5]
    faces[2].transforms[left] = lambda cx, cy: (faces[5].min_x, faces[5].max_y - faces[2].relative_y(cy))
    faces[2].facing_after[left] = right

    faces[3].neighbors[left] = faces[5]
    faces[3].transforms[left] = lambda cx, cy: (faces[5].min_x + faces[3].relative_y(cy), faces[5].min_y)
    faces[3].facing_after[left] = down

    faces[3].neighbors[right] = faces[1]
    faces[3].transforms[right] = lambda cx, cy: (faces[1].min_x + faces[3].relative_y(cy), faces[1].max_y)
    faces[3].facing_after[right] = up

    faces[4].neighbors[right] = faces[1]
    faces[4].transforms[right] = lambda cx, cy: (faces[1].max_x, faces[1].max_y - faces[4].relative_y(cy))
    faces[4].facing_after[right] = left

    faces[4].neighbors[down] = faces[6]
    faces[4].transforms[down] = lambda cx, cy: (faces[6].max_x, faces[6].min_y + faces[4].relative_x(cx))
    faces[4].facing_after[down] = left

    faces[5].neighbors[up] = faces[3]
    faces[5].transforms[up] = lambda cx, cy: (faces[3].min_x, faces[3].min_y + faces[5].relative_x(cx))
    faces[5].facing_after[up] = right

    faces[5].neighbors[left] = faces[2]
    faces[5].transforms[left] = lambda cx, cy: (faces[2].min_x, faces[2].max_y - faces[5].relative_y(cy))
    faces[5].facing_after[left] = right

    faces[6].neighbors[left] = faces[2]
    faces[6].transforms[left] = lambda cx, cy: (faces[2].min_x + faces[6].relative_y(cy), faces[2].min_y)
    faces[6].facing_after[left] = down

    faces[6].neighbors[down] = faces[1]
    faces[6].transforms[down] = lambda cx, cy: (faces[1].min_x + faces[6].relative_x(cx), faces[1].min_y)
    faces[6].facing_after[down] = down

    faces[6].neighbors[right] = faces[4]
    faces[6].transforms[right] = lambda cx, cy: (faces[4].min_x + faces[6].relative_y(cy), faces[4].max_y)
    faces[6].facing_after[right] = up

    return faces


def skip_face(cube: dict[int, Face], cur_x, cur_y, facing) -> (Position, Direction):
    face = [f for f in cube.values() if f.contains_position(cur_x, cur_y)][0]
    new_position = face.transforms[facing](cur_x, cur_y)
    new_direction = face.facing_after[facing]
    return new_position, new_direction


class Grid:
    def __init__(self, tiles: dict[(int, int), str], instructions: list[str]):
        self.tiles = tiles
        self.instructions = instructions
        self.facing_idx = 0
        self.facing = facings[0]
        self.starting_pos = self.min_at_y(1)
        self.current_pos = self.starting_pos

    def run(self, cube=None):
        for instruction in self.instructions:
            if instruction == 'L':
                self.turn_left()
            elif instruction == 'R':
                self.turn_right()
            elif instruction.isnumeric():
                self.go_forward(int(instruction), cube)
            else:
                raise RuntimeError("Impossible turn!")

    def turn_right(self):
        self.facing_idx = (self.facing_idx + 1) % 4
        self.facing = facings[self.facing_idx]

    def turn_left(self):
        self.facing_idx = (self.facing_idx - 1) % 4
        self.facing = facings[self.facing_idx]

    def go_forward(self, count, cube):
        for i in range(count):
            cx, cy = self.current_pos
            dx, dy = self.facing
            target_pos = cx + dx, cy + dy
            target_dir = dx, dy
            if target_pos not in self.tiles:
                if cube:
                    target_pos, target_dir = skip_face(cube, cx, cy, self.facing)
                else:
                    if self.facing == up:
                        target_pos = self.max_at_x(cx)
                    elif self.facing == down:
                        target_pos = self.min_at_x(cx)
                    elif self.facing == left:
                        target_pos = self.max_at_y(cy)
                    elif self.facing == right:
                        target_pos = self.min_at_y(cy)
                    else:
                        raise RuntimeError(f"Impossible facing")

            target_tile = self.tiles[target_pos]
            if target_tile == blocked:
                break
            self.current_pos = target_pos
            self.facing = target_dir
            self.facing_idx = facing_points[target_dir]

    def max_at_x(self, x):
        return max(((tx, ty) for tx, ty in self.tiles.keys() if tx == x), key=lambda pos: pos[1])

    def min_at_x(self, x):
        return min(((tx, ty) for tx, ty in self.tiles.keys() if tx == x), key=lambda pos: pos[1])

    def max_at_y(self, y):
        return max(((tx, ty) for tx, ty in self.tiles.keys() if ty == y), key=lambda pos: pos[0])

    def min_at_y(self, y):
        return min(((tx, ty) for tx, ty in self.tiles.keys() if ty == y), key=lambda pos: pos[0])

    def score(self):
        x, y = self.current_pos
        return 1000 * y + 4 * x + facing_points[self.facing]


def load():
    grid = {}
    filename = "example" if example else "input"
    with open(filename) as file:
        for y, line in enumerate(file, 1):
            for x, char in enumerate(line, 1):
                if char == passable or char == blocked:
                    grid[(x, y)] = char
    instr_p = re.compile(r"\d+|L|R")
    instruction_string = ex_instr if example else inp_instr
    instructions = instr_p.findall(instruction_string)
    return Grid(grid, instructions)


def part1():
    grid = load()
    grid.run()
    print(grid.score())


def part2():
    cube = initialize_cube()
    grid = load()
    grid.run(cube)
    print(grid.score())


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()


class TestCube(unittest.TestCase):
    def setUp(self):
        self.cube = initialize_cube()

    def test_corners(self):
        self.assert_in_square(1, [(101, 1), (150, 1), (101, 50), (150, 50)])
        self.assert_in_square(2, [(51, 1), (100, 1), (51, 50), (100, 50)])
        self.assert_in_square(3, [(51, 51), (100, 51), (51, 100), (100, 100)])
        self.assert_in_square(4, [(51, 101), (100, 101), (51, 150), (100, 150)])
        self.assert_in_square(5, [(1, 101), (50, 101), (1, 150), (50, 150)])
        self.assert_in_square(6, [(1, 151), (50, 151), (1, 200), (50, 200)])

    def assert_in_square(self, square, points):
        for name, face in self.cube.items():
            for x, y in points:
                if name == square:
                    self.assertTrue(face.contains_position(x, y),
                                    f"{name} shouldn contain {(x, y)}")
                else:
                    self.assertFalse(face.contains_position(x, y),
                                     f"{name} shouldn't contain {(x, y)}")
                    
    def test_translate(self):
        # face 1
        self.assert_translation((101, 1), up, (1, 200), up)
        self.assert_translation((150, 1), up, (50, 200), up)
        self.assert_translation((150, 1), right, (100, 150), left)
        self.assert_translation((150, 50), right, (100, 101), left)
        self.assert_translation((101, 50), down, (100, 51), left)

        # face 2
        self.assert_translation((51, 1), up, (1, 151), right)
        self.assert_translation((100, 1), up, (1, 200), right)
        self.assert_translation((51, 1), left, (1, 150), right)
        self.assert_translation((51, 50), left, (1, 101), right)

        # face 3
        self.assert_translation((51, 51), left, (1, 101), down)
        self.assert_translation((51, 100), left, (50, 101), down)
        self.assert_translation((100, 51), right, (101, 50), up)
        self.assert_translation((100, 100), right, (150, 50), up)

        # face 4
        self.assert_translation((100, 101), right, (150, 50), left)
        self.assert_translation((100, 150), right, (150, 1), left)
        self.assert_translation((51, 150), down, (50, 151), left)
        self.assert_translation((100, 150), down, (50, 200), left)

        # face 5
        self.assert_translation((1, 101), up, (51, 51), right)
        self.assert_translation((50, 101), up, (51, 100), right)
        self.assert_translation((1, 101), left, (51, 50), right)
        self.assert_translation((1, 150), left, (51, 1), right)

        # face 6
        self.assert_translation((1, 151), left, (51, 1), down)
        self.assert_translation((1, 200), left, (100, 1), down)
        self.assert_translation((1, 200), down, (101, 1), down)
        self.assert_translation((50, 200), down, (150, 1), down)
        self.assert_translation((50, 200), right, (100, 150), up)
        self.assert_translation((50, 151), right, (51, 150), up)

    def assert_translation(self, from_point, facing, expected_point, expected_facing):
        self.assertEqual(skip_face(self.cube, from_point[0], from_point[1], facing),
                          (expected_point, expected_facing),
                          f"Expected going {facing_names[facing]} from {from_point} to lead to {expected_point} facing {facing_names[expected_facing]}")

