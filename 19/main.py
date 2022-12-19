import re

bp_pattern = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
ore_bot = "ore_bot"
clay_bot = "clay_bot"
obs_bot = "obs_bot"
geo_bot = "geo_bot"
do_nothing = "   "


action_keys = {
    'r': ore_bot,
    'c': clay_bot,
    'o': obs_bot,
    'g': geo_bot,
    'n': do_nothing
}

class Blueprint:
    def __init__(self, id, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geo_ore_cost, geo_obs_cost):
        self.id = id
        self.costs = {
            ore_bot: (int(ore_cost), 0, 0),
            clay_bot: (int(clay_cost), 0, 0),
            obs_bot: (int(obs_ore_cost), int(obs_clay_cost), 0),
            geo_bot: (int(geo_ore_cost), 0, int(geo_obs_cost)),
            do_nothing: (0, 0, 0)
        }

    def print_costs(self):
        print(f"Costs:")
        for name, costs in self.costs.items():
            if name == do_nothing:
                continue
            self.print_cost(name, costs)
        print()

    @staticmethod
    def print_cost(name, costs):
        ore, clay, obs = costs
        print(f"{name: >10} {ore: >3} {clay: >3} {obs: >3}")

class Game:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.ore_bot = 1
        self.clay_bot = 0
        self.obs_bot = 0
        self.geo_bot = 0
        self.states = {1: GameState(self.blueprint, 1, 0, 0, 0, 0, {ore_bot: 1, clay_bot: 0, obs_bot: 0, geo_bot: 0})}
        self.simulate_after(1)

    def simulate_after(self, from_minute):
        for b in range(1, from_minute):
            self.states[b].last_modified = False
        self.states[from_minute].last_modified = True
        for m in range(from_minute + 1, 26):
            action = self.states[m].action if m in self.states else do_nothing
            self.states[m] = self.states[m - 1].next_state(action)

    def play(self):
        while self.play_round():
            pass
        return self.blueprint.id * self.states[24].geo

    def play_round(self):
        print("\n" * 5)
        self.blueprint.print_costs()
        for i, state in self.states.items():
            stated.print()
        day, action = self.get_input()
        if not action:
            return False
        self.states[day].set_action(action)
        self.simulate_after(day)
        return True

    def get_input(self):
        while True:
            action = input("Action: ").strip().split(" ")
            if action == ["d"]:
                return None, None
            if len(action) < 2:
                print(f"Use: <day> <action-key> (oRe, Clay, Obs, Geo, Nothing) {action}")
                continue
            day, action_key = action
            if not day.isnumeric():
                print(f"Invalid date {action}")
                continue
            day = int(day)
            if 1 < day > 25:
                print(f"Invalid date {action}")
                continue
            if action_key not in action_keys:
                print(f"Invalid action {action}")
                continue
            return day, action_keys[action_key]



class GameState:
    def __init__(self, blueprint: Blueprint, minute, ore, clay, obs, geo, bots, action=do_nothing):
        self.blueprint = blueprint
        self.minute = minute
        self.ore = ore
        self.clay = clay
        self.obs = obs
        self.geo = geo
        self.bots = bots
        self.action = action
        self.action_illegal = None
        self.set_action(action)
        self.last_modified = False

    def set_action(self, action):
        self.action = action
        (ore_cost, clay_cost, obs_cost) = self.blueprint.costs[action]
        self.action_illegal = ore_cost > self.ore or clay_cost > self.clay or obs_cost > self.obs
        return self.action_illegal

    def next_state(self, next_state_action=do_nothing):
        (ore_cost, clay_cost, obs_cost) = self.blueprint.costs[self.action]
        next_ore = self.ore - ore_cost + self.bots[ore_bot]
        next_clay = self.clay - clay_cost + self.bots[clay_bot]
        next_obs = self.obs - obs_cost + self.bots[obs_bot]
        next_geo = self.geo + self.bots[geo_bot]
        next_bots = self.bots.copy()
        if self.action != do_nothing:
            next_bots[self.action] += 1
        return GameState(self.blueprint, self.minute + 1, next_ore, next_clay, next_obs, next_geo, next_bots,
                         next_state_action)

    def print(self):
        marker = ">" if self.last_modified else " "
        print(f"{marker} {self.minute: >2}: RES: {self.ore: >3} {self.clay: >3} {self.obs: >3} {self.geo: >3}   "
              f"BOTS: {self.bots[ore_bot]: >2} {self.bots[clay_bot]: >2} {self.bots[obs_bot]: >2} {self.bots[geo_bot]: >2}   "
              f"ACTION: {self.action}",
              end="")
        if self.action_illegal:
            print("  <-- ILLEGAL", end="")
        print()


def load():
    bps = []
    with open("example") as file:
        for line in file:
            m = bp_pattern.fullmatch(line.strip())
            if not m:
                raise RuntimeError(f"line did not match: {line.strip()}")
            bps.append(Blueprint(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7)))
    return bps


def part1():
    bps = load()
    scores = []
    for bp in bps:
        game = Game(bp)
        scores.append(game.play())


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
