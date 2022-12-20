import re
from functools import cmp_to_key

bp_pattern = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
ore_bot = "ore_bot"
clay_bot = "clay_bot"
obs_bot = "obs_bot"
geo_bot = "geo_bot"
do_nothing = "   "
bot_types = [ore_bot, clay_bot, obs_bot, geo_bot]

action_keys = {
    'r': ore_bot,
    'c': clay_bot,
    'o': obs_bot,
    'g': geo_bot,
    'n': do_nothing
}


class Blueprint:
    def __init__(self, id, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geo_ore_cost, geo_obs_cost):
        self.id = int(id)
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

    def __str__(self):
        return f"[{self.minute}]: {self.ore} {self.clay} {self.obs} {self.geo} | {self.bots[ore_bot]} " \
               f"{self.bots[clay_bot]} {self.bots[obs_bot]} {self.bots[geo_bot]} | {self.action}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        return self.as_tuple() == other.as_tuple()

    def as_tuple(self):
        return (self.minute, self.ore, self.clay, self.obs, self.geo, self.bots[ore_bot], self.bots[clay_bot],
                self.bots[obs_bot], self.bots[geo_bot], self.action)

    def strictly_worse_than(self, other: "GameState"):
        fewer_bots = all([self.bots[bot_type] <= other.bots[bot_type] for bot_type in bot_types])
        less_cash = self.ore <= other.ore and self.clay <= other.clay and self.obs <= other.obs and self.geo <= other.geo
        return fewer_bots and less_cash

    def set_action(self, action):
        self.action = action
        (ore_cost, clay_cost, obs_cost) = self.blueprint.costs[action]
        self.action_illegal = ore_cost > self.ore or clay_cost > self.clay or obs_cost > self.obs
        return self.action_illegal

    def next_state(self, action=None, next_state_action=do_nothing):
        if action is None:
            action = self.action
        (ore_cost, clay_cost, obs_cost) = self.blueprint.costs[action]
        next_ore = self.ore - ore_cost + self.bots[ore_bot]
        next_clay = self.clay - clay_cost + self.bots[clay_bot]
        next_obs = self.obs - obs_cost + self.bots[obs_bot]
        next_geo = self.geo + self.bots[geo_bot]
        next_bots = self.bots.copy()
        if action != do_nothing:
            next_bots[action] += 1
        return GameState(self.blueprint, self.minute + 1, next_ore, next_clay, next_obs, next_geo, next_bots,
                         next_state_action)

    def get_valid_actions(self):
        valid = []
        for action, (ore, clay, obs) in self.blueprint.costs.items():
            if self.ore >= ore and self.clay >= clay and self.obs >= obs:
                valid.append(action)
        if self.bots[clay_bot] == 0 and self.can_afford(ore_bot) and self.can_afford(clay_bot):
            valid.remove(do_nothing)
        elif self.bots[obs_bot] == 0 and self.can_afford(ore_bot) and self.can_afford(clay_bot) and self.can_afford(obs_bot):
            valid.remove(do_nothing)
        elif len(valid) == 5:
            valid.remove(do_nothing)
        return valid

    def can_afford(self, bot_type):
        (ore, clay, obs) = self.blueprint.costs[bot_type]
        return self.ore >= ore and self.clay >= clay and self.obs >= obs

    def print(self):
        marker = ">" if self.last_modified else " "
        print(f"{marker} {self.minute: >2}: RES: {self.ore: >3} {self.clay: >3} {self.obs: >3} {self.geo: >3}   "
              f"BOTS: {self.bots[ore_bot]: >2} {self.bots[clay_bot]: >2} {self.bots[obs_bot]: >2} {self.bots[geo_bot]: >2}   "
              f"ACTION: {self.action}",
              end="")
        if self.action_illegal:
            print("  <-- ILLEGAL", end="")
        print()


class InteractiveGame:
    def __init__(self, blueprint):
        self.blueprint = blueprint
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
            state.print()
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


class AutoGame:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.states = {i: [] for i in range(1, 26)}
        self.ok_states = []

    def quantum_play(self):
        self.states[1].append(
            GameState(self.blueprint, 1, 0, 0, 0, 0, {ore_bot: 1, clay_bot: 0, obs_bot: 0, geo_bot: 0}))
        # TODO: not working good
        for minute in range(1, 25):
            for state in self.states[minute]:
                for action in state.get_valid_actions():
                    new_state = state.next_state(action=action)
                    if not worse_than_any_in(new_state, self.ok_states):
                        self.states[minute + 1].append(new_state)
                        self.ok_states.append(new_state)
        best_end_state = max(self.states[25], key=lambda state: state.geo)
        return best_end_state.geo * self.blueprint.id


def worse_than_any_in(cur_state: GameState, states: list[GameState]):
    return any(cur_state.strictly_worse_than(other_state) for other_state in states)


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
        game = AutoGame(bp)
        scores.append(game.quantum_play())
    print(sum(scores))


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
