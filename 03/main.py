alpha = "abcdefghijklmnopqrstuvwxyz"

def gen_alpha_scores():
    scores = {}
    for idx, letter in enumerate(alpha, start=1):
        scores[letter] = idx
        scores[letter.upper()] = idx + 26
    return scores


def main():
    packs = []
    with open("input") as file:
        for line in file:
            items = line.strip()
            if len(items) % 2 != 0:
                print(f"ERROR: got non-even number of items {len(items), items}")

            half = int(len(items) / 2)
            left = items[:half]
            right = items[half:]

            unique_left = set(left)
            unique_right = set(right)
            unique = set(items)
            overlap = unique_right.intersection(unique_left)
            if len(overlap) != 1:
                print(f"ERROR: got multiple overlap {overlap} in {(left, right)}")

            packs.append((unique, overlap.pop()))

    scores = gen_alpha_scores()

    score = sum([scores[overlap] for (unique, overlap) in packs])
    print(f"Sum Scores 1: {score}")

    score2 = 0
    for i in range(0, len(packs), 3):
        elf1 = packs[i][0]
        elf2 = packs[i + 1][0]
        elf3 = packs[i + 2][0]

        shared = elf1.intersection(elf2).intersection(elf3)
        if len(shared) != 1:
            print(f"ERROR: didn't get 1 shared between {(elf1, elf2, elf3)}")

        score2 += scores[shared.pop()]
    print(f"Score 2: {score2}")


if __name__ == '__main__':
    main()
