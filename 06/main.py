def find_unique(line, buffer_size):
    for i in range(0, len(line)):
        chars = line[i: i + buffer_size]
        if len(set(chars)) == buffer_size:
            print(i + buffer_size)
            break


def main():
    with open("input") as file:
        line = file.readline().strip()
        find_unique(line, 4)
        find_unique(line, 14)


if __name__ == '__main__':
    main()
