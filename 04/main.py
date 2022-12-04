def split_line(line):
    parts = line.split(",")
    return parse_part(parts[0]), parse_part(parts[1])


def parse_part(string):
    parts = string.split("-")
    return int(parts[0]), int(parts[1])


def part1(ranges):
    fully_contained = 0
    for (range1, range2) in ranges:
        if range1[0] <= range2[0] and range1[1] >= range2[1]:
            fully_contained += 1
        elif range1[0] >= range2[0] and range1[1] <= range2[1]:
            fully_contained += 1

    print(f"Fully Contained: {fully_contained}")


def part2(ranges):
    overlap = 0
    for (range1, range2) in ranges:
        if range1[0] < range2[0] and range1[1] < range2[0]:
            pass
        elif range2[0] < range1[0] and range2[1] < range1[0]:
            pass
        else:
            overlap += 1

    print(f"Partially Contained: {overlap}")


def main():
    ranges = []
    with open("input") as file:
        for line in file:
            ranges.append(split_line(line.strip()))

    part1(ranges)
    part2(ranges)


if __name__ == '__main__':
    main()
