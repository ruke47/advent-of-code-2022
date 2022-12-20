class Node:
    def __init__(self, value, prior=None):
        self.value = value
        self.prior = prior
        self.next = None

    def __str__(self):
        return f"{self.prior.value} <[{self.value}]> {self.next.value}"

    def __repr__(self):
        return self.__str__()


def load():
    head = None
    zero = None
    original_idx = {}
    with open("input") as file:
        for idx, line in enumerate(file):
            node = Node(int(line.strip()))
            if not head:
                head = node
            original_idx[idx] = node
            if idx - 1 in original_idx:
                prior = original_idx[idx - 1]
                prior.next = node
                node.prior = prior
            if node.value == 0:
                zero = node
    tail = original_idx[len(original_idx) - 1]
    tail.next = head
    head.prior = tail
    return original_idx, zero


def part1():
    original_idx, zero = load()
    length = len(original_idx)
    print_array(zero)
    print_array_backwards(zero)
    for i in range(length):
        if i % 100 == 0:
            print(f"\t- {i}/{length}")
        cur = original_idx[i]
        new_place = cur
        val = cur.value
        if val == 0:
            continue
        if val > 0:
            while val > 0:
                new_place = new_place.next
                if new_place == cur:
                    new_place = new_place.next
                val -= 1
            if cur == new_place or new_place.next == cur:
                continue
        elif val < 0:
            while val < 0:
                new_place = new_place.prior
                if new_place == cur:
                    new_place = new_place.prior
                val += 1
            # move back 1 more so it's the same as if we'd come at this from the front
            new_place = new_place.prior
            if cur == new_place or new_place.next == cur:
                continue
        # use temp variables to avoid gunking up state
        out_next = cur.next
        out_prior = cur.prior

        in_prior = new_place
        in_next = new_place.next

        out_next.prior = out_prior
        out_prior.next = out_next

        in_prior.next = cur
        cur.prior = in_prior
        cur.next = in_next
        in_next.prior = cur

        for node in (out_prior, out_next, in_prior, in_next, cur, new_place):
            if node.next.prior != node or node.prior.next != node:
                raise RuntimeError("You've fucked up now. Now, you've fucked up.")

    print_array(zero)
    print_array_backwards(zero)

    moves = (1000, 2000, 3000)
    sum = 0
    for steps in moves:
        cur = zero
        for i in range(steps):
            cur = cur.next
        sum += cur.value
    print(sum)


def print_array(zero):
    cur = zero
    arr = []
    i = 0
    while True:
        i += 1
        arr.append(cur.value)
        cur = cur.next
        if cur == zero:
            break
        if i > 5002:
            break
    print(i)
    print(arr)

def print_array_backwards(zero):
    cur = zero
    arr = []
    i = 0
    while True:
        i += 1
        arr.append(cur.value)
        cur = cur.prior
        if cur == zero:
            break
        if i > 5002:
            break
    print(i)
    print(arr)

def main():
    part1()


if __name__ == '__main__':
    main()

