def main():
    with open("input") as file:
        all_elves = []
        cur_elf = []
        for line in file:
            if line.strip():
                cur_elf.append(int(line.strip()))
            else:
                all_elves.append(cur_elf)
                cur_elf = []
        if len(cur_elf) > 0:
            all_elves.append(cur_elf)

    elfscores = []
    for elf in all_elves:
        score = 0
        for food in elf:
            score += food
        elfscores.append(score)

    print(f"Max Score: {max(elfscores)}")

    elfscores.sort(reverse=True)
    print(f"Top 3: {elfscores[0] + elfscores[1] + elfscores[2]}")


if __name__ == '__main__':
   main()

