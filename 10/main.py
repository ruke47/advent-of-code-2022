from math import floor


class Comms:
    def __init__(self, cmds):
        self.cmds = cmds;
        self.x = 1
        self.time = 0
        self.history = {}
        self.screen = None
        self.clear_screen()

    def run(self):
        for cmd in self.cmds:
            if cmd:
                self.tick()
                self.tick()
                self.x += cmd
            else:
                self.tick()

    def tick(self):
        self.time += 1
        self.history[self.time] = self.x

        col = (self.time - 1) % 40
        row = floor((self.time - 1)/40) % 6

        if abs(col - self.x) <= 1:
            self.screen[row][col] = '█'
        else:
            self.screen[row][col] = ' '

    def clear_screen(self):
        self.screen = [['X' for x in range(40)] for y in range(6)]

    def print_screen(self):
        print('-' * 44)
        for row in self.screen:
            print(f"- {''.join(row)} -")
        print('-' * 44)


def main():
    instructions = []
    with open("input") as file:
        for line in file:
            if line.strip() == "noop":
                instructions.append(None)
            else:
                instructions.append(int(line.strip().split()[1]))

    comms = Comms(instructions)
    comms.run()

    score = 0
    for time in [20, 60, 100, 140, 180, 220]:
        score += time * comms.history[time]

    print(score)
    comms.print_screen()


if __name__ == '__main__':
    main()
