alpha = "abcdefghijklmnopqrstuvwxyz"

def gen_alpha_scores():
    scores = {}
    for idx, letter in enumerate(alpha, start=1):
        scores[letter] = idx
        scores[letter.upper()] = idx + 26
    return scores

def part1(packs, scores):
    score = 0
    for items in packs:
        if len(items) % 2 != 0:
            print(f"ERROR: got non-even number of items {len(items), items}")

        half = int(len(items) / 2)
        unique_left = set(items[:half])
        unique_right = set(items[half:])
        overlap = unique_right.intersection(unique_left)
        if len(overlap) != 1:
            print(f"ERROR: got multiple overlap {overlap} in {(left, right)}")

        score += scores[overlap.pop()]
    print(f"Score 1: {score}")

def part2(packs, scores):
    score = 0
    for idx in range(0, len(packs), 3):
        elf1 = set(packs[idx])
        elf2 = set(packs[idx + 1])
        elf3 = set(packs[idx + 2])
        shared = elf1.intersection(elf2).intersection(elf3)
        if len(shared) != 1:
            print(f"ERROR: didn't get 1 shared between {(elf1, elf2, elf3)}")

        score += scores[shared.pop()]
    print(f"Score 2: {score}")


def main():
    packs = []
    with open("input") as file:
        for line in file:
            packs.append(line.strip())

    scores = gen_alpha_scores()

    part1(packs, scores)
    part2(packs, scores)


if __name__ == '__main__':
    main()
