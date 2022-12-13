import json
from functools import cmp_to_key


# returns True if ordered, False if unordered, None to keep checking
def ordered(val1, val2):
    # Both numbers, smaller should come first
    if isinstance(val1, int) and isinstance(val2, int):
        if val1 < val2:
            return True
        if val1 > val2:
            return False
        return None

    # Both lists
    if isinstance(val1, list) and isinstance(val2, list):
        # recursively check items in list, up to the length of the shorter list
        for item1, item2 in zip(val1, val2):
            order = ordered(item1, item2)
            if order is not None:
                return order

        # If there's no difference through the length of the shorter, compare lengths
        size_diff = len(val1) - len(val2)
        if size_diff < 0:
            return True
        if size_diff > 0:
            return False
        return None

    # If one is a number and one is a list, treat the number as a list of length 1
    if isinstance(val1, list) and isinstance(val2, int):
        return ordered(val1, [val2])
    if isinstance(val1, int) and isinstance(val2, list):
        return ordered([val1], val2)

    raise f"I don't know how to compare {(val1, val2)}!"


# return C-style {-1,0,1} to enable sorting
def numeric_ordered(val1, val2):
    order = ordered(val1, val2)
    if order is True:
        return -1
    if order is False:
        return 1
    return 0


def read_input():
    index = 1
    pairs = []
    with open("input") as file:
        for line in file:
            line1 = json.loads(line.strip())
            line2 = json.loads(file.readline().strip())
            file.readline()
            pairs.append((index, line1, line2))
            index += 1

    return pairs


def part1():
    pairs = read_input()
    print(sum([index for index, sig1, sig2 in pairs if ordered(sig1, sig2)]))


def part2():
    decoder1 = [[2]]
    decoder2 = [[6]]
    all_signals = [decoder1, decoder2]

    pairs = read_input()
    for _, sig1, sig2 in pairs:
        all_signals.append(sig1)
        all_signals.append(sig2)

    all_signals.sort(key=cmp_to_key(numeric_ordered))

    product = 1
    for idx, signal in enumerate(all_signals):
        if signal == decoder1 or signal == decoder2:
            product *= idx + 1
    print(product)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
