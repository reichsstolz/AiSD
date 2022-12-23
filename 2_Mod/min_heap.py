import sys
from typing import Optional
from re import compile


class Error(Exception):
    pass


class Node:
    def __init__(self, key: int, value: str, index: int):
        self.value = value
        self.key = key
        self.index = index


class Heap:
    def __init__(self) -> object:
        self.list = list()
        self.dict = dict()

    def _heapify_down(self, node: Node):
        cur: Node = node
        left: Node = self._get_left(node)
        right: Node = self._get_right(node)
        while True:
            node = self._search_min(cur, left, right)
            if node.key != cur.key:
                self._swap(cur, node)
                left = self._get_left(cur)
                right = self._get_right(cur)
            else:
                break

    def _heapify_up(self, node: Node):
        if self.empty():
            return
        cur = node
        parent: Node = self._get_parent(cur)
        while parent and parent.key > cur.key:
            self._swap(parent, cur)
            parent = self._get_parent(cur)

    @staticmethod
    def _search_min(*nodes): # не функция минимума, смотрите ниже
        cur = nodes[0]
        for node in nodes:
            if cur is None:
                cur = node
            if node and node.key < cur.key:
                cur = node
        return cur

    def search(self, key: int) -> Optional[Node]:
        return self.dict.get(key)

    def _get_left(self, node: Node) -> Optional[Node]:
        if (node.index << 1) + 1 < len(self.list):
            return self.list[(node.index << 1) + 1]

    def _get_right(self, node: Node) -> Optional[Node]:
        if (node.index << 1) + 2 < len(self.list):
            return self.list[(node.index << 1) + 2]

    def _get_parent(self, node):
        if node.index != 0:
            return self.list[node.index - 1 >> 1]

    def _swap(self, first: Node, second: Node):
        self.list[first.index], self.list[second.index] = self.list[second.index], self.list[first.index]
        first.index, second.index = second.index, first.index

    def set_node(self, key: int, value: str):
        node = self.search(key)
        if node:
            node.value = value
            self._heapify_up(node)
        else:
            raise Error

    def insert(self, key: int, value):
        if self.dict.get(key):
            raise Error
        node = Node(key, value, len(self.list))
        self.dict[key] = node
        self.list.append(node)
        self._heapify_up(node)

    def empty(self) -> bool:
        if self.dict:
            return False
        return True

    def min_node(self, *nodes: Node) -> Optional[Node]:
        if self.empty():
            raise Error
        return self.list[0]

    def max_node(self) -> Optional[Node]:
        if self.empty():
            raise Error
        return max(self.list[len(self.list) // 2:], key=lambda x: x.key)

    def delete(self, key: int):
        node = self.dict.get(key)
        if node is None:
            raise Error
        self.dict.pop(key)
        last = self.list[len(self.list) - 1]
        self._swap(node, last)
        self.list.pop()
        self._heapify_up(last)
        self._heapify_down(last)

    def extract(self) -> Node:
        if self.empty():
            raise Error
        node = self.list[0]
        self.dict.pop(node.key)
        last = self.list[len(self.list) - 1]
        self._swap(node, last)
        self.list.pop()
        self._heapify_up(last)
        self._heapify_down(last)
        node.index = None
        return node


def print_heap(heap: Heap):
    if heap.empty():
        print("_")
        return
    lvl_nodes_count = 1
    next_lvl_count = lvl_nodes_count * 2
    i = 0
    while i != len(heap.list):
        if i == 0:
            print(f"[{heap.list[i].key} {heap.list[i].value}]", end="")
            lvl_nodes_count -= 1
        elif lvl_nodes_count != 0:
            print(f"[{heap.list[i].key} {heap.list[i].value} {heap.list[i - 1 >> 1].key}]", end="")
            lvl_nodes_count -= 1
        if lvl_nodes_count != 0:
            print(end=" ")
        else:
            print()
            lvl_nodes_count = next_lvl_count
            next_lvl_count *= 2
        i += 1

    if lvl_nodes_count != next_lvl_count / 2:
        print(" ".join(["_"] * lvl_nodes_count))


def main():
    heap = Heap()
    # test = open("B_test/16test.txt", "r")
    add_re = compile(r"add (-\d+|\d+) (|\S+)")
    set_re = compile(r"set (-\d+|\d+) (|\S+)")
    search_re = compile(r"search (-\d+|\d+)")
    max_re = compile(r"max")
    min_re = compile(r"min")
    print_re = compile(r"print")
    delete_re = compile(r"delete (-\d+|\d+)")
    extract_re = compile(r"extract")
    # for line in test:
    for line in sys.stdin:
        line = line.replace('\n', '')
        args = line.split()
        try:
            if add_re.fullmatch(line):
                if len(args) == 2:
                    heap.insert(int(args[1]), "")
                    continue
                heap.insert(int(args[1]), args[2])
            elif set_re.fullmatch(line):
                if len(args) == 2:
                    heap.set_node(int(args[1]), "")
                    continue
                heap.set_node(int(args[1]), args[2])
            elif search_re.fullmatch(line):
                node = heap.search(int(args[1]))
                if node is None:
                    print(0)
                    continue
                print(f"1 {node.index} {node.value}")
            elif max_re.fullmatch(line):
                node = heap.max_node()
                if node is None:
                    continue
                print(f"{node.key} {node.index} {node.value}")
            elif min_re.fullmatch(line):
                node = heap.min_node()
                if node is None:
                    continue
                print(f"{node.key} {node.index} {node.value}")
            elif print_re.fullmatch(line):
                print_heap(heap)
            elif extract_re.fullmatch(line):
                node = heap.extract()
                print(f"{node.key} {node.value}")
            elif delete_re.fullmatch(line):
                heap.delete(int(args[1]))
            elif line != "":
                raise Error
        except Error:
            print("error")

    # test.close()


if __name__ == "__main__":
    main()
