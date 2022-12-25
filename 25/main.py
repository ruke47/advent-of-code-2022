import unittest

example = False

values = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2
}

snaf_chars = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2'
}


def parse_snaf(snaf: str) -> int:
    total = 0
    for exp, char in enumerate(snaf[::-1]):
        total += values[char] * (5 ** exp)
    return total


def to_snaf(num: int) -> str:
    exp = 0
    snaf = []
    max_repr = {-1: 0, 0: 2}
    while abs(num) > max_repr[exp]:
        exp += 1
        max_repr[exp] = max_repr[exp - 1] + 2 * (5 ** exp)
    starting_exp = exp
    starting_num = num

    while exp >= 0:
        digit = int(num / (5 ** exp))
        num -= digit * (5 ** exp)
        if abs(num) > max_repr[exp - 1]:
            if num < 0:
                digit -= 1
                num += 5 ** exp
            else:
                digit += 1
                num -= 5 ** exp
        snaf.append(snaf_chars[digit])
        exp -= 1

    if num != 0:
        raise RuntimeError(f"I did math wrong! {starting_num, starting_exp, snaf}")

    return ''.join(snaf)


def load():
    filename = "example" if example else "input"
    with open(filename) as file:
        return [line.strip() for line in file]


def part1():
    snafs = load()
    snaf_sum = sum(parse_snaf(snaf) for snaf in snafs)
    print(to_snaf(snaf_sum))


def main():
    part1()


if __name__ == '__main__':
    main()

class SnafTest(unittest.TestCase):
    def test_small_nums(self):
        self.assertEqual('==', to_snaf(-12))
        self.assertEqual('=-', to_snaf(-11))
        self.assertEqual('=0', to_snaf(-10))
        self.assertEqual('=1', to_snaf(-9))
        self.assertEqual('=2', to_snaf(-8))
        self.assertEqual('-=', to_snaf(-7))
        self.assertEqual('--', to_snaf(-6))
        self.assertEqual('-0', to_snaf(-5))
        self.assertEqual('-1', to_snaf(-4))
        self.assertEqual('-2', to_snaf(-3))
        self.assertEqual('=', to_snaf(-2))
        self.assertEqual('-', to_snaf(-1))
        self.assertEqual('0', to_snaf(0))
        self.assertEqual('1', to_snaf(1))
        self.assertEqual('2', to_snaf(2))
        self.assertEqual('1=', to_snaf(3))
        self.assertEqual('1-', to_snaf(4))
        self.assertEqual('10', to_snaf(5))
        self.assertEqual('11', to_snaf(6))
        self.assertEqual('12', to_snaf(7))
        self.assertEqual('2=', to_snaf(8))
        self.assertEqual('2-', to_snaf(9))
        self.assertEqual('20', to_snaf(10))
        self.assertEqual('21', to_snaf(11))
        self.assertEqual('22', to_snaf(12))

    def test_bigger_nums(self):
        digits = '=-012'
        for fours in digits:
            for threes in digits:
                for twos in digits:
                    for ones in digits:
                        snaf = fours + threes + twos + ones
                        while snaf and snaf[0] == '0':
                            snaf = snaf[1:]
                        if not snaf:
                            snaf = '0'
                        num = parse_snaf(snaf)
                        try:
                            got_snaf = to_snaf(num)
                            self.assertEqual(snaf, got_snaf, f"Expected {snaf} ({num}) to be {got_snaf}")
                        except KeyError as e:
                            print(f"Got a keyError on {snaf} ({num})")

