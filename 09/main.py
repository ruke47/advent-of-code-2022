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
    def __init__(self, moves):
        self.moves = moves
        self.head = (0, 0)
        self.tail = (0, 0)
        self.tail_positions = [(0, 0)]

    def run(self):
        for move in self.moves:
            self.move_head(move)

    def move_head(self, move):
        direction, count = move
        dir_offset = dir_offsets[direction]

        for i in range(count):
            self.head = (self.head[0] + dir_offset[0], self.head[1] + dir_offset[1])
            self.catch_up_tail()

    def catch_up_tail(self):
        hx, hy = self.head
        tx, ty = self.tail
        offset_x = hx - tx
        offset_y = hy - ty

        if abs(offset_x) < 2 and abs(offset_y) < 2:
            return

        normalized_x = normalize(offset_x)
        normalized_y = normalize(offset_y)

        if offset_x == 0:
            self.tail = (tx, ty + normalized_y)
        elif offset_y == 0:
            self.tail = (tx + normalized_x, ty)
        else:
            self.tail = (tx + normalized_x, ty + normalized_y)

        self.tail_positions.append(self.tail)


def main():
    head_moves = []
    with open("input") as file:
        for line in file:
            line_parts = line.strip().split()
            head_moves.append((line_parts[0], int(line_parts[1])))

    grid = Grid(head_moves)
    grid.run()
    print(len(set(grid.tail_positions)))


if __name__ == '__main__':
    main()
