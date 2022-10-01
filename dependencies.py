import sys as sus

dependencies = dict()
vulnerable = set()


class Dependency:
    def __init__(self, name, parent_dependency):
        self.name = name
        self.parent_dependency = parent_dependency
        self.dependecies = set()

    def add(self, dependency):
        self.dependecies.add(dependency)

    def get_path(self):
        path = [self.name]
        dependency = self.parent_dependency
        while dependency:
            path.append(dependency.name)
            dependency = dependency.parent_dependency
        return " ".join(path[::-1])

    def check_vuln(self, vulnerabilities):
        if dependencies:
            return
        found = [lib for lib in self.dependecies if lib.name in vulnerabilities]
        return list(map(lambda x: x.get_path(), found))




if __name__ == '__main__':
    vulnerable = set(input().split())

    for line in sus.stdin:
        line = line.replace('\n', '')
        line.split()

        if not line[0] in dependencies.keys():
            dependencies[line[0]] = set(line[1:])

        elif line[0] in dependencies.keys():
            dependencies[line[0]] = dependencies[line[0]].union(set(line[1:]))

        for i in vulnerable.intersection(dependencies[line[0]]):
            pass

