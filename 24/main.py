from collections.abc import Iterable

example = False

Direction = (int, int)
Point = (int, int)
directions = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1)
}
move_options = ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))

class Ghost:
    def __init__(self, x: int, y: int, direction_str: str):
        self.position = (x, y)
        self.direction_str = direction_str
        self.direction = directions[direction_str]

    def __str__(self):
        return f"{self.position} {self.direction_str}"

    def __repr__(self):
        return self.__str__()

    def move(self, board: "Board"):
        gx, gy = self.position
        dx, dy = self.direction
        tx, ty = gx + dx, gy + dy
        if tx < board.min_x:
            tx = board.max_x
        elif tx > board.max_x:
            tx = board.min_x
        if ty < board.min_y:
            ty = board.max_y
        elif ty > board.max_y:
            ty = board.min_y
        return Ghost(tx, ty, self.direction_str)



class Board:
    def __init__(self, width, height, goal_count):
        self.min_x = 0
        self.min_y = 0
        self.max_x = width
        self.max_y = height
        self.begin = (0, -1)
        self.end = (self.max_x, self.max_y + 1)
        if goal_count == 1:
            self.goals = [self.end]
        elif goal_count == 3:
            self.goals = [self.end, self.begin, self.end]

    def __str__(self):
        return f"{self.max_x, self.max_y}"

    def __repr__(self):
        return self.__str__()

    def valid_position(self, x, y):
        if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y:
            return True
        if (x, y) == self.begin or (x, y) == self.end:
            return True
        return False

class Gamestate:
    def __init__(self, board, player_position: Point, turn, history: list[Point], score: int):
        self.board = board
        self.player_position = player_position
        self.turn = turn
        self.history = history.copy()
        self.history.append(player_position)
        self.score = score
        self.point_get = False
        if player_position == board.goals[self.score]:
            self.score += 1
            self.point_get = True

    def __str__(self):
        return f"[{self.turn}]: {self.player_position}"

    def __repr__(self):
        return self.__str__()

    def __key__(self):
        return self.turn, self.player_position, self.score

    def __hash__(self):
        return hash(self.__key__())

    def __eq__(self, other):
        if isinstance(other, Gamestate):
            return self.__key__() == other.__key__()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def valid_next_moves(self, new_ghost_positions: set(Point)) -> Iterable["Gamestate"]:
        px, py = self.player_position
        valid_moves = []
        for dx, dy in move_options:
            tx, ty = px + dx, py + dy
            if not self.board.valid_position(tx, ty):
                continue
            if (tx, ty) in new_ghost_positions:
                continue
            valid_moves.append(Gamestate(self.board, (tx, ty), self.turn + 1, self.history, self.score))
        return valid_moves

    def is_winner(self):
        return self.score == len(self.board.goals)


def load(goal_count):
    filename = "example" if example else "input"
    ghosts = []
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char in '><v^':
                    ghosts.append(Ghost(x, y, char))
    board = Board(x, y, goal_count)
    return ghosts, board


def run(goal_count):
    ghosts, board = load(goal_count)

    state = Gamestate(board, (0, -1), 0, [], 0)
    states = {
        0: [state]
    }
    ghosts = {
        0: ghosts
    }
    for i in range(1, 1_000_000):
        prior_states = states[i - 1]
        if not prior_states:
            print(f"{i}: no valid moves")
            break
        ghosts[i] = [ghost.move(board) for ghost in ghosts[i - 1]]
        ghost_positions = set(ghost.position for ghost in ghosts[i])
        states[i] = set()
        found_winner = False
        for state in prior_states:
            if state.is_winner():
                print(f"Won on turn {state.turn}")
                found_winner = True
                break
            # can't do any better than that
            if state.point_get:
                states[i] = state.valid_next_moves(ghost_positions)
                break
            else:
                for next_state in state.valid_next_moves(ghost_positions):
                    states[i].add(next_state)

        if i % 1000 == 0:
            print(f"\t - {i}")
        if found_winner:
            break


def main():
    run(1)
    run(3)


if __name__ == '__main__':
    main()