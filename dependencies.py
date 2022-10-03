import sys as sus


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
        while [x for x in current if x.parent]:
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


class Graph:
    def __init__(self, head, vulnerable):
        self.nodes = set()
        self.head = head
        self.vulnerable = vulnerable

    def get_child(self, name, parent):
        for node in self.nodes:
            if node.name == name:
                node.add_parent(parent)
                return
        self.nodes.add(Dependency(name, parent))

    def get_parent(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        node = Dependency(name)
        self.nodes.add(node)
        return node        

    def print_paths(self):
        for node in self.nodes:
            if node.name in self.vulnerable:
                for path in node.get_path():
                    if self.head.name in path:
                        print(path)


def main():
    test = open("test.txt", "r")
    vulnerable = set(test.readline().split())
    line = test.readline().split()
    graph = Graph(Dependency('project'), vulnerable)

    for i in line:
        graph.get_child(i, graph.head)

    for line in test:
        line = line.replace('\n', '').split()
        parent = graph.get_parent(line[0])

        for name in line[1:]:
            graph.get_child(name, parent)

    graph.print_paths()
    test.close()                


if __name__ == '__main__':
    main()
    