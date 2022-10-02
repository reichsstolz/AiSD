import sys as sus

nodes = set()


class Dependency:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = set()
        if parent:
            self.parent = {parent}

    def add_parent(self, parent):
        self.parent.add(parent)

    def get_path(self):
        paths = [self.name]
        current = {self}
        while [x for x in current if not x.parent is None]:
            for i in range(len(paths)):
                for lib in current:
                    if paths[i].split()[0] == lib.name and lib.parent:
                        for parent in lib.parent:
                            paths.append(f"{parent.name} " + paths[i])
                        paths.remove(paths[i])
            buffer = set()
            for s in map(lambda x: x.parent, current):
                buffer.update(s)
            current = buffer
        return paths


def find_child(name, parent):
    for node in nodes:
        if node.name == name:
            node.add_parent(parent)
            return node
    return Dependency(name, parent)


def extract_nodes(name):
    found = []
    for node in nodes:
        if node.name == name:
            found.append(node)
    return found


if __name__ == '__main__':
    test = open("test.txt", "r")
    vulnerable = set(test.readline().split())
    line = test.readline().split()
    project = Dependency('project')
    nodes.update(Dependency(name, project) for name in line)

    for line in test:
        line = line.replace('\n', '').split()
        extracted = extract_nodes(line[0])

        if not extracted:
            lost_lib = Dependency(line[0])
            nodes.add(lost_lib)
            nodes.update(find_child(name, lost_lib) for name in line[1:])
            continue

        for item in extracted:
            nodes.update(find_child(name, item) for name in line[1:])

    nodes = set(x for x in nodes if x.parent)

    for i in nodes:
        if i.name in vulnerable:
            print(i.get_path())