import re


def print_tops(stacks):
    top = ""
    for i in range(9):
        top += stacks[i][-1]
    print(f"Tops: {top}")


def copy_stacks(stacks):
    return {k: v.copy() for (k, v) in stacks.items()}


def part1(stacks, instructions):
    for idx, (count, src, dest) in enumerate(instructions):
        if len(stacks[src]) == 0:
            print(f"{idx}: source is empty! {src, dest}")
            for stack_idx in range(9):
                print(f"stack[{stack_idx}]: {stacks[stack_idx]}")
                raise
        for i in range(count):
            stacks[dest].append(stacks[src].pop())

    print_tops(stacks)


def part2(stacks, instructions):
    for idx, (count, src, dest) in enumerate(instructions):
        group = stacks[src][count * -1:]
        for item in group:
            # just get rid of ONE from src
            stacks[src].pop()
            # append to dest in stack order
            stacks[dest].append(item)

    print_tops(stacks)


def main():
    stacks = {}
    for i in range(9):
        stacks[i] = []
    # count, src, dest
    instructions = []

    with open("input") as file:
        for line in file:
            trimmed = line.strip()
            if trimmed:
                for idx, char in enumerate(trimmed):
                    if char != ' ':
                        stacks[idx].insert(0, char)
            else:
                break

        instruction_pattern = re.compile("move (\d+) from (\d+) to (\d+)\n")
        for line in file:
            matches = instruction_pattern.fullmatch(line)
            if not matches:
                print(f"ERROR: line didn't match pattern: {line}")
                raise
            instructions.append((int(matches[1]), int(matches[2]) - 1, int(matches[3]) - 1))

        # make sure it looks right
        # for i in range(10):
        #    print(f"instruction[{i}]: {instructions[i]}")

    part1(copy_stacks(stacks), instructions)
    part2(copy_stacks(stacks), instructions)


if __name__ == '__main__':
    main()
