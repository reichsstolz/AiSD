import sys


class Dependency:
    def __init__(self, name, parent=None, is_project=False):
        self.name = name
        self.parent = set()
        self.is_project = is_project
        if parent:
            self.parent = {parent}

    def add_parent(self, parent):
        self.parent.add(parent)

    def get_path(self, current, path):  # c 3.7 dict хранит порядок добавления

        if current.is_project:
            print(" ".join(list(path.keys())[::-1]))
            return

        if not current.parent or path.get(current.name):
            return

        path[current.name] = 1

        for x in current.parent:
            self.get_path(x, path)
        path.pop(current.name)


class Graph:
    def __init__(self, head, vulnerable):
        self.nodes = dict()
        self.head = head
        self.vulnerable = set(vulnerable)

    def get_child(self, name, parent):
        child = self.nodes.get(name)
        if child:
            child.add_parent(parent)
            return
        self.nodes[name] = Dependency(name, parent=parent)

    def get_parent(self, name):
        parent = self.nodes.get(name)
        if parent:
            return parent
        parent = Dependency(name)
        self.nodes[name] = parent
        return parent

    def print_paths(self):
        for name in self.vulnerable:
            if not self.nodes.get(name):
                continue
            self.nodes[name].get_path(self.nodes[name], dict())


def main():
    #test = open("C_test/test.txt", "r")
    vulnerable = input().split()  # input().split()
    line = input().split()  # input().split()
    graph = Graph(Dependency("project", is_project=True), vulnerable)

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
    # test.close()


if __name__ == '__main__':
    main()
