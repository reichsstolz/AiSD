import sys
import sys as sus


class Path:
    def __init__(self, start):
        self.path = [start]

    def in_path(self, node):
        return node in self.path

    def update(self):
        if self.is_end():
            return {self}
        return set(self.clone(node) for node in self.path[0].parent if self.clone(node))

    def clone(self, node):
        new = Path(None)
        new.path = self.path.copy()
        if not new.in_path(node):
            new.path.insert(0, node)
            return new

    def is_end(self):
        if self.path[0].parent:
            return False
        return True

    def __str__(self):
       return " ".join([x.name for x in self.path[1:]])


class Dependency:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = set()
        if parent:
            self.parent = {parent}

    def add_parent(self, parent):
        self.parent.add(parent)

    def get_path(self):
        paths = {Path(self)}
        while False in [x.is_end() for x in paths]:
            buffer = set()
            for p in map(lambda path: path.update(), paths):
                if p:
                    buffer.update(p)
            paths = buffer
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
                    if path.in_path(self.head):
                        print(str(path))


def main():
    #test = open("test.txt", "r")
    vulnerable = set(input().split())
    line = input().split()
    graph = Graph(Dependency('project'), vulnerable)

    for i in line:
        graph.get_child(i, graph.head)

    for line in sys.stdin:
        line = line.replace('\n', '').split()
        if not line:
            continue
        parent = graph.get_parent(line[0])

        for name in line[1:]:
            graph.get_child(name, parent)

    graph.print_paths()
    #test.close()


if __name__ == '__main__':
    main()
    