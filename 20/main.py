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


def mixup(multiplier=1, rounds=1):
    original_idx, zero = load()
    length = len(original_idx)
    validate_integrity(zero, length)

    for node in original_idx.values():
        node.value *= multiplier

    total_moves = length * rounds
    for i in range(total_moves):
        if i % 1000 == 0:
            print(f"\t- {i}/{total_moves}")
        cur = original_idx[i % length]
        new_place = cur
        val = cur.value
        mod_val = val % (length - 1)
        if val == 0:
            continue
        while mod_val > 0:
            new_place = new_place.next
            if new_place == cur:
                new_place = new_place.next
            mod_val -= 1
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

    validate_integrity(zero, length)
    moves = (1000, 2000, 3000)
    score = 0
    for steps in moves:
        cur = zero
        for i in range(steps):
            cur = cur.next
        score += cur.value
    print(score)


def validate_integrity(zero, length):
    cur = zero
    i = 0
    while True:
        i += 1
        cur = cur.next
        if cur == zero:
            break
        if i > length:
            break
    if i != length:
        raise RuntimeError("Forwards integrity is shite.")

    cur = zero
    i = 0
    while True:
        i += 1
        cur = cur.prior
        if cur == zero:
            break
        if i > length:
            break
    if i != length:
        raise RuntimeError("Backwards integrity is shite.")

def main():
    mixup(1, 1)
    mixup(811589153, 10)


if __name__ == '__main__':
    main()

