from collections.abc import Iterable

example = False
verbose = False

north = (0, -1)
east = (1, 0)
south = (0, 1)
west = (-1, 0)
considerations = {
    north: ( (0, -1), (1, -1), (-1, -1) ),
    east: ( (1, 0), (1, -1), (1, 1) ),
    south: ( (0, 1), (-1, 1), (1, 1) ),
    west: ( (-1, 0), (-1, -1), (-1, 1) )
}
consideration_order = (north, south, west, east)

Position = (int, int)
Direction = (int, int)


def consideration_with_offset(offset: int) -> Iterable[Direction]:
    csdr = []
    for i in range(len(consideration_order)):
        index = (i + offset) % len(consideration_order)
        csdr.append(consideration_order[index])
    return csdr


class Elf:
    next_name = 0

    def __init__(self, initial_position: Position):
        self.name = Elf.next_name
        Elf.next_name += 1
        self.initial_position = initial_position
        self.current_position = initial_position

    def __str__(self):
        return f"{self.current_position}"

    def __repr__(self):
        return self.__str__()

    def has_no_neighbors(self, all_positions):
        sx, sy = self.current_position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == dy == 0:
                    continue
                if (sx + dx, sy + dy) in all_positions:
                    return False
        return True


class Game:
    def __init__(self, elves: set[Elf]):
        self.elves = elves
        self.round = 0

    def run(self, rounds):
        for i in range(rounds):
            if verbose:
                print(f"\n--- Round {i} --- \n")
                (tx, ty), (bx, by) = self.get_bounding_box()
                current_positions = {elf.current_position: elf for elf in self.elves}
                for y in range (ty, by + 1):
                    for x in range(tx, bx + 1):
                        if (x, y) in current_positions:
                            print(current_positions[(x, y)].name, end='')
                        else:
                            print('.', end='')
                    print()
            if not self.step():
                print(f"No one moved on {self.round}")
                break
            else:
                if self.round % 10_000 == 0:
                    print(f"\t - {self.round}")


    def step(self):
        current_positions = set(elf.current_position for elf in self.elves)
        # location -> elf
        planned_moves = {}
        for elf in self.elves:
            if elf.has_no_neighbors(current_positions):
                continue
            ex, ey = elf.current_position
            for direction in consideration_with_offset(self.round):
                checks = considerations[direction]
                can_move = True
                for dx, dy in checks:
                    target = ex + dx, ey + dy
                    if target in current_positions:
                        can_move = False
                        break
                if can_move:
                    dx, dy = direction
                    target = ex + dx, ey + dy
                    if target in planned_moves:
                        planned_moves[target].append(elf)
                    else:
                        planned_moves[target] = [elf]
                    break

        any_moved = False
        for target_location, elf_list in planned_moves.items():
            if len(elf_list) == 1:
                elf_list[0].current_position = target_location
                any_moved = True

        self.round += 1
        return any_moved

    def get_bounding_box(self):
        min_x = min(elf.current_position[0] for elf in self.elves)
        min_y = min(elf.current_position[1] for elf in self.elves)
        max_x = max(elf.current_position[0] for elf in self.elves)
        max_y = max(elf.current_position[1] for elf in self.elves)

        return (min_x, min_y), (max_x, max_y)


def size_of_box(top_left, bottom_right):
    min_x, min_y = top_left
    max_x, max_y = bottom_right
    height = max_y - min_y + 1
    width = max_x - min_x + 1
    return height * width


def load():
    filename = "example" if example else "input"
    elves = set()
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    elves.add(Elf((x, y)))
    return elves


def part1():
    game = Game(load())
    game.run(10)
    tl, br = game.get_bounding_box()
    empty = size_of_box(tl, br) - len(game.elves)
    print(empty)


def part2():
    game = Game(load())
    game.run(900_000_000_000)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()