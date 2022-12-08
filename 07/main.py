import re


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = {}
        self.own_filesize = 0
        self.total_filesize = 0
        self.children = {}

    def add_file(self, name, size):
        self.files[name] = size
        self.own_filesize += size
        self.total_filesize += size
        if self.parent:
            self.parent.add_child_filesize(size)

    def add_child_filesize(self, size):
        self.total_filesize += size
        if self.parent:
            self.parent.add_child_filesize(size)

    def add_dir(self, name):
        new_dir = Directory(name, self)
        self.children[name] = new_dir
        return new_dir

    def get_dir(self, name):
        if name == "..":
            return self.parent
        elif name in self.children:
            return self.children[name]
        else:
            raise f"No such child dir {name}!"


cd_pattern = re.compile(r"\$ cd (\S+)")
ls_pattern = re.compile(r"\$ ls")
dir_pattern = re.compile(r"dir (\S+)")
file_pattern = re.compile(r"(\d+) (\S+)")

def main():
    with open("input") as file:
        root = Directory("/")
        cd = root
        all_dirs = [root]
        for line in file:
            cd_match = cd_pattern.fullmatch(line.strip())
            ls_match = ls_pattern.fullmatch(line.strip())
            dir_match = dir_pattern.fullmatch(line.strip())
            file_match = file_pattern.fullmatch(line.strip())

            if cd_match:
                cd = cd.get_dir(cd_match.group(1))
            elif ls_match:
                # an ls is always preceeded by a cd in the input
                continue
            elif dir_match:
                all_dirs.append(cd.add_dir(dir_match.group(1)))
            elif file_match:
                cd.add_file(file_match.group(2), int(file_match.group(1)))
            else:
                raise f"None matched {line}"

        print(sum(directory.total_filesize for directory in all_dirs if directory.total_filesize <= 100000))

        cur_free_space = 70000000 - root.total_filesize
        min_size_to_delete = 30000000 - cur_free_space
        print(min(directory.total_filesize for directory in all_dirs if directory.total_filesize >= min_size_to_delete))


if __name__ == '__main__':
    main()
