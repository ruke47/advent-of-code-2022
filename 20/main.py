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
    for i in range(length):
        cur = original_idx[i]
        new_place = cur
        val = cur.value
        if val == 0:
            continue
        if val > 0:
            while val > 0:
                new_place = new_place.next
                val -= 1
        elif val < 0:
            while val < 0:
                new_place = new_place.prior
                val += 1
            # move back 1 more so it's the same as if we'd come at this from the front
            new_place = new_place.prior
        # use temp variables to avoid gunking up state
        cur_next_prior = cur.prior
        cur_prior_next = cur.next
        cur_prior = new_place.prior
        cur_next = new_place.next

        cur.next.prior = cur_next_prior
        cur.prior.next = cur_prior_next
        new_place.next.prior = cur
        new_place.next = cur
        cur.prior = cur_prior
        cur.next = cur_next

    print_array(zero)

    moves = sorted([1000 % length, 2000 % length, 3000 % length])
    progressive_moves = (moves[0], moves[1] - moves[0], moves[2] - moves[1])
    sum = 0
    cur = zero
    for steps in progressive_moves:
        for i in range(steps):
            cur = cur.next
        sum += cur.value
    print(sum)

def print_array(zero):
    cur = zero
    arr = []
    while True:
        arr.append(cur.value)
        cur = cur.next
        if cur == zero:
            break


def main():
    part1()


if __name__ == '__main__':
    main()

