from math import floor, prod


class Monke:
    def __init__(self, id, items, inspect_fn, test_num, true_monke_id, false_monke_id, troupe):
        self.id = id
        self.items = items
        self.inspect_fn = inspect_fn
        self.test_num = test_num
        self.true_monke_id = true_monke_id
        self.false_monke_id = false_monke_id
        self.troupe = troupe
        troupe.append(self)
        self.inspections = 0

    def inspect_items(self, worry_divisor, common_modulo):
        while self.items:
            item = self.items.pop(0)
            new_val = self.inspect_fn(item)

            if worry_divisor:
                bored_val = floor(new_val / 3)
            else:
                bored_val = new_val

            bored_val = bored_val % common_modulo

            if bored_val % self.test_num == 0:
                self.troupe[self.true_monke_id].accept_item(bored_val)
            else:
                self.troupe[self.false_monke_id].accept_item(bored_val)
            self.inspections += 1

    def accept_item(self, item):
        self.items.append(item)


def get_fresh_troupe():
    troupe = []
    Monke(0, [54, 61, 97, 63, 74], lambda item: item * 7, 17, 5, 3, troupe)
    Monke(1, [61, 70, 97, 64, 99, 83, 52, 87], lambda item: item + 8, 2, 7, 6, troupe)
    Monke(2, [60, 67, 80, 65], lambda item: item * 13, 5, 1, 6, troupe)
    Monke(3, [61, 70, 76, 69, 82, 56], lambda item: item + 7, 3, 5, 2, troupe)
    Monke(4, [79, 98], lambda item: item + 2, 7, 0, 3, troupe)
    Monke(5, [72, 79, 55], lambda item: item + 1, 13, 2, 1, troupe)
    Monke(6, [63], lambda item: item + 4, 19, 7, 4, troupe)
    Monke(7, [72, 51, 93, 63, 80, 86, 81], lambda item: item * item, 11, 0, 4, troupe)
    return troupe


def run_troupe(rounds, worry_divisor):
    troupe = get_fresh_troupe()
    common_modulo = prod([monke.test_num for monke in troupe])
    for rd in range(rounds):
        for monke in troupe:
            monke.inspect_items(worry_divisor, common_modulo)

    inspections = [monke.inspections for monke in troupe]
    inspections.sort()
    print(inspections[6] * inspections[7])


def main():
    run_troupe(20, True)
    run_troupe(10000, False)


if __name__ == '__main__':
    main()
