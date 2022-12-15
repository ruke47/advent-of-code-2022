import re

input_pattern = re.compile(r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)")


class Span:
    def __init__(self, begin_incl, end_incl):
        self.begin_incl = begin_incl
        self.end_incl = end_incl

    def __str__(self):
        return f"{(self.begin_incl, self.end_incl)}"

    def __repr__(self):
        return self.__str__()

    def overlaps(self, other):
        first, second = sorted([self, other], key=lambda span: span.begin_incl)
        return second.begin_incl <= first.end_incl

    def combine(self, other):
        if not self.overlaps(other):
            raise f"Cannot combine {self, other}"
        begin = min(self.begin_incl, other.begin_incl)
        end = max(self.end_incl, other.end_incl)
        return Span(begin, end)

    def size(self):
        return abs(self.end_incl - self.begin_incl) + 1


class Sensor:
    def __init__(self, position, nearest_beacon):
        self.position = position
        self.nearest_beacon = nearest_beacon
        px, py = position
        bx, by = nearest_beacon
        self.radius = abs(px - bx) + abs(py - by)

    def range_at_y(self, y):
        px, py = self.position
        dy = abs(py - y)
        if dy > self.radius:
            return None
        else:
            range_begin = px - self.radius + dy
            range_end = px + self.radius - dy
            return Span(range_begin, range_end)


def read_input():
    sensors = []
    with open("input") as file:
        for line in file:
            match = input_pattern.fullmatch(line.strip())
            if not match:
                raise f"Could not parse line: {line}"
            sensors.append(Sensor((int(match.group("sensor_x")), int(match.group("sensor_y"))),
                                  (int(match.group("beacon_x")), int(match.group("beacon_y")))))

    return sensors


def combine_spans(spans):
    sorted_spans = sorted(spans, key=lambda span: span.begin_incl)
    sorted_spans.reverse()
    disjoint_spans = []
    working = sorted_spans.pop()
    other = None
    while len(sorted_spans):
        other = sorted_spans.pop()
        if working.overlaps(other):
            working = working.combine(other)
            other = None
        else:
            disjoint_spans.append(working)
            working = other
    disjoint_spans.append(working)
    if other:
        disjoint_spans.append(other)

    return disjoint_spans


def part1():
    sensors = read_input()
    nearby_spans = []
    test_y = 2000000
    for sensor in sensors:
        span = sensor.range_at_y(test_y)
        if span:
            nearby_spans.append(span)
    positions_at_y = sum([span.size() for span in combine_spans(nearby_spans)])
    beacons_at_y = set([sensor.nearest_beacon for sensor in sensors if sensor.nearest_beacon[1] == test_y])
    print(positions_at_y - len(beacons_at_y))


def part2():
    sensors = read_input()
    for test_y in range(0, 4_000_000):
        nearby_spans = []
        for sensor in sensors:
            span = sensor.range_at_y(test_y)
            if span:
                nearby_spans.append(span)
        joined_spans = combine_spans(nearby_spans)
        if len(joined_spans) > 1:
            print(joined_spans)
            print((joined_spans[0].end_incl + 1) * 4000000 + test_y)
        if test_y % 10_000 == 0:
            print(f"\t - {test_y}")


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
