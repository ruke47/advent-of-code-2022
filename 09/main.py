dir_offsets = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def normalize(val):
    if val == 0:
        return 0
    return int(val / abs(val))


class Grid:
    def __init__(self, moves, length):
        self.moves = moves
        self.knots = [(0, 0) for i in range(length)]
        self.tail_positions = [(0, 0)]

    def run(self):
        for move in self.moves:
            self.move_head(move)

    def move_head(self, move):
        direction, count = move
        dir_offset = dir_offsets[direction]

        for i in range(count):
            head_x, head_y = self.knots[0]
            self.knots[0] = (head_x + dir_offset[0], head_y + dir_offset[1])

            # for every pair of knots, have the first drag the latter
            for i in range(0, len(self.knots) - 1):
                self.catch_up_tail(i, i + 1)

    # head is the dragger, tail is the dragee (not necessarily the final knot in the rope)
    def catch_up_tail(self, head_pos, tail_pos):
        hx, hy = self.knots[head_pos]
        tx, ty = self.knots[tail_pos]
        offset_x = hx - tx
        offset_y = hy - ty

        if abs(offset_x) < 2 and abs(offset_y) < 2:
            return

        normalized_x = normalize(offset_x)
        normalized_y = normalize(offset_y)

        if offset_x == 0:
            self.knots[tail_pos] = (tx, ty + normalized_y)
        elif offset_y == 0:
            self.knots[tail_pos] = (tx + normalized_x, ty)
        else:
            self.knots[tail_pos] = (tx + normalized_x, ty + normalized_y)

        # if this is the last knot, add its position to the tail positions
        if tail_pos == len(self.knots) - 1:
            self.tail_positions.append(self.knots[tail_pos])


def main():
    head_moves = []
    with open("input") as file:
        for line in file:
            line_parts = line.strip().split()
            head_moves.append((line_parts[0], int(line_parts[1])))

    grid1 = Grid(head_moves, 2)
    grid1.run()
    print(len(set(grid1.tail_positions)))

    grid2 = Grid(head_moves, 10)
    grid2.run()
    print(len(set(grid2.tail_positions)))

if __name__ == '__main__':
    main()
