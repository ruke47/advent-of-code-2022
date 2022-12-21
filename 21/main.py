import re

val_re = re.compile(r"(\d+)")
op_re = re.compile(r"(\w{4}) ([+-/*]) (\w{4})")
human = "humn"

class Monke:
    def __init__(self, name, job, troupe: dict[str, "Monke"]):
        self.name = name
        self.job_str = job
        self.troupe = troupe
        self.value = None
        self.rhs = None
        self.lhs = None
        self.op = None
        self.parse_job(job)

    def __str__(self):
        return f"{self.name}: {self.job_str}"

    def __repr__(self):
        return self.__str__()

    def parse_job(self, job_str):
        if val_m := val_re.match(job_str):
            self.value = int(val_m.group(1))
        elif op_m := op_re.match(job_str):
            self.lhs = op_m.group(1)
            self.op = op_m.group(2)
            self.rhs = op_m.group(3)
        else:
            raise RuntimeError(f"Can't parse job for {self.name}: {job_str}")

    def get_val(self):
        if self.value:
            return self.value
        else:
            rhs_val = self.troupe[self.rhs].get_val()
            lhs_val = self.troupe[self.lhs].get_val()
            return do_op(self.op, lhs_val, rhs_val)

    def get_eq(self):
        if self.name == human:
            return human
        elif self.value:
            return self.value
        else:
            rhs = self.troupe[self.rhs].get_eq()
            lhs = self.troupe[self.lhs].get_eq()
            if is_number(rhs) and is_number(lhs):
                return do_op(self.op, lhs, rhs)
            else:
                return lhs, self.op, rhs


def do_op(op, lhs, rhs):
    if op == '+':
        value = lhs + rhs
    elif op == '-':
        value = lhs - rhs
    elif op == '*':
        value = lhs * rhs
    elif op == '/':
        value = int(lhs / rhs)
    else:
        raise RuntimeError(f"illegal op: {op}")
    return value


def is_number(val):
    return isinstance(val, int) or isinstance(val, float)


def load():
    troupe = {}
    with open("input") as file:
        for line in file:
            name, job = line.strip().split(": ")
            troupe[name] = Monke(name, job, troupe)
    return troupe


def part1():
    troupe = load()
    root = troupe["root"]
    print(root.get_val())


def part2():
    troupe = load()
    root = troupe["root"]
    rhs = troupe[root.rhs].get_eq()
    lhs = troupe[root.lhs].get_eq()
    equation, value = (rhs, lhs) if isinstance(lhs, int) else (lhs, rhs)
    print(f"{value} = {equation}")
    while equation != human:
        lhs, op, rhs = equation
        if op == '+':
            # x + 4 = 7
            if is_number(rhs):
                value -= rhs
                equation = lhs
            # 4 + x = 7
            elif is_number(lhs):
                value -= lhs
                equation = rhs
            else:
                raise RuntimeError(f"Bad eq: {equation}")
        elif op == '-':
            # x - 4 = 7
            if is_number(rhs):
                value += rhs
                equation = lhs
            # 4 - x = 7
            elif is_number(lhs):
                value -= lhs
                value *= -1
                equation = rhs
            else:
                raise RuntimeError(f"Bad eq: {equation}")
        elif op == '*':
            # x * 4 = 7
            if is_number(rhs):
                value = int(value / rhs)
                equation = lhs
            # 4 * x = 7
            elif is_number(lhs):
                value = int(value / lhs)
                equation = rhs
            else:
                raise RuntimeError(f"Bad eq: {equation}")
        elif op == '/':
            # x / 4 == 7
            if is_number(rhs):
                value *= rhs
                equation = lhs
            # 4 / x = 7
            elif is_number(lhs):
                value = int(lhs / value)
                equation = rhs
            else:
                raise RuntimeError(f"Bad eq: {equation}")

        print(f"{value} = {equation}")


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()

