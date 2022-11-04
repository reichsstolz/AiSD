import sys
from typing import Optional
from collections import deque
from re import compile


class Error(Exception):
    pass


class Node:
    def __init__(self, key, value, parent=None):
        self.value = value
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    def assign_left(self, node):
        if node is None:
            self.left = None
            return
        self.left = node
        node.parent = self

    def assign_right(self, node):
        if node is None:
            self.right = None
            return
        self.right = node
        node.parent = self


def add(level: deque, node: Optional[Node], times=1):
    if not level:
        if node:
            level.append(node)
            return
        level.append(times)
        return

    last = level.pop()
    if type(last) == int:
        if node is None:
            last += times
            level.append(last)
        else:
            level.append(last)
            level.append(node)
    else:
        if node is None:
            level.append(last)
            level.append(times)
        else:
            level.append(last)
            level.append(node)


class Splay:
    def __init__(self, root):
        self.root: Node = root

    def search(self, key, as_command=False) -> Optional[Node]:
        if as_command and self.empty():
            return

        if self.empty():
            raise Error

        current: Node = self.root
        prev: Optional[Node] = None

        while current and key != current.key:
            prev = current
            if key > current.key:
                current = current.right
                continue
            current = current.left

        if not current:
            self._splay(prev)
            return current

        self._splay(current)

        return current

    def _zig(self, node: Node):
        parent: Node = node.parent
        gparent: Optional[Node] = parent.parent

        if gparent:
            if gparent.left == parent:
                gparent.assign_left(node)
            else:
                gparent.assign_right(node)
        else:
            self.root = node
            node.parent = None

        if parent.right == node:
            parent.assign_right(node.left)
            node.assign_left(parent)

        elif parent.left == node:
            parent.assign_left(node.right)
            node.assign_right(parent)

    def set(self, key, value):
        node = self.search(key)
        if node is None:
            raise Error

        node.value = value
        # self._splay(node)

    def insert(self, key, value):
        node = Node(key, value)
        if self.empty():
            self.root = node
            return node

        current = self.root

        while True:
            if current.key < node.key:
                if current.right is None:
                    current.assign_right(node)
                    self._splay(node)
                    return
                current = current.right

            elif current.key > node.key:
                if current.left is None:
                    current.assign_left(node)
                    self._splay(node)
                    return
                current = current.left
            else:
                self._splay(current)
                raise Error

    def _zig_zig(self, node: Node):
        self._zig(node.parent)
        self._zig(node)

    def _zig_zag(self, node: Node):
        self._zig(node)
        self._zig(node)

    def _splay(self, node: Node):
        while node.parent is not None:
            parent: Node = node.parent
            gparent: Optional[Node] = parent.parent

            if gparent is None:
                self._zig(node)
            elif (gparent.left == parent and parent.left == node) or \
                    (gparent.right == parent and parent.right == node):
                self._zig_zig(node)
            else:
                self._zig_zag(node)

    def empty(self) -> bool:
        return self.root is None

    def min(self) -> Optional[Node]:
        if self.empty():
            raise Error
        cur = self.root
        while cur.left:
            cur = cur.left
        self._splay(cur)
        return cur

    def max(self) -> Optional[Node]:
        if self.empty():
            raise Error
        cur = self.root
        while cur.right:
            cur = cur.right
        self._splay(cur)
        return cur

    def _merge(self, left: Optional[Node], right: Optional[Node]) -> Node:
        if left is None:
            return right

        if right is None:
            return left

        top = left

        while top.right is not None:
            top = top.right

        self._splay(top)
        top.assign_right(right)

        return top

    def delete(self, key):
        node = self.search(key)

        if node is None:
            raise Error

        left = node.left
        right = node.right

        if left is not None:
            left.parent = None

        if right is not None:
            right.parent = None

        self.root = self._merge(left, right)

    # def print(self):
    #     if self.empty():
    #         print("_")
    #         return
    #     current_lvl = deque([self.root])
    #     next_lvl = deque()
    #     kids_alive = False
    #     string = ""
    #
    #     while True:
    #         node = current_lvl.popleft()
    #
    #         if type(node) != int:
    #             if node.parent is None:
    #                 print(f"[{node.key} {node.value}]", end="")
    #                 #string += f"[{node.key} {node.value}]"
    #             else:
    #                 print(f"[{node.key} {node.value} {node.parent.key}]", end="")
    #                 #string += f"[{node.key} {node.value} {node.parent.key}]"
    #
    #             if node.left or node.right:
    #                 kids_alive = True
    #
    #             add(next_lvl, node.left)
    #             add(next_lvl, node.right)
    #
    #         else:
    #             print("_ " * (node - 1), end="")
    #             print("_", end="")
    #             #string +="_ "*(node-1)
    #             #string += "_"
    #             add(next_lvl, None, times=node*2)
    #
    #         if current_lvl:
    #             print(end=" ")
    #             #string+=" "
    #
    #         else:
    #             print()
    #             #print(string)
    #             if not kids_alive:
    #                 break
    #             kids_alive = False
    #             current_lvl = next_lvl
    #             next_lvl = deque()
    #             string = ""


def print_tree(tree: Splay):
    if tree.empty():
        print("_")
        return
    current_lvl = deque([tree.root])
    next_lvl = deque()
    kids_alive = False
    string = ""

    while True:
        node = current_lvl.popleft()

        if type(node) != int:
            if node.parent is None:
                print(f"[{node.key} {node.value}]", end="")
                # string += f"[{node.key} {node.value}]"
            else:
                print(f"[{node.key} {node.value} {node.parent.key}]", end="")
                # string += f"[{node.key} {node.value} {node.parent.key}]"

            if node.left or node.right:
                kids_alive = True

            add(next_lvl, node.left)
            add(next_lvl, node.right)

        else:
            print("_ " * (node - 1), end="")
            print("_", end="")
            # string +="_ "*(node-1)
            # string += "_"
            add(next_lvl, None, times=node * 2)

        if current_lvl:
            print(end=" ")
            # string+=" "

        else:
            print()
            # print(string)
            if not kids_alive:
                break
            kids_alive = False
            current_lvl = next_lvl
            next_lvl = deque()
            string = ""


def main():
    tree = Splay(None)
    # test = open("A_test/test12.txt", "r")
    add_re = compile(r"add (-\d+|\d+) (|\S+)")
    set_re = compile(r"set (-\d+|\d+) (|\S+)")
    search_re = compile(r"search (-\d+|\d+)")
    max_re = compile(r"max")
    min_re = compile(r"min")
    print_re = compile(r"print")
    delete_re = compile(r"delete (-\d+|\d+)")
    # for line in test:
    for line in sys.stdin:
        line = line.replace('\n', '')
        args = line.split()
        try:
            if add_re.fullmatch(line):
                if len(args) == 2:
                    tree.insert(int(args[1]), "")
                    continue
                tree.insert(int(args[1]), args[2])
            elif set_re.fullmatch(line):
                if len(args) == 2:
                    tree.set(int(args[1]), "")
                    continue
                tree.set(int(args[1]), args[2])
            elif search_re.fullmatch(line):
                node = tree.search(int(args[1]), as_command=True)
                if node is None:
                    print(0)
                    continue
                print(f"1 {node.value}")
            elif max_re.fullmatch(line):
                node = tree.max()
                if node is None:
                    continue
                print(f"{node.key} {node.value}")
            elif min_re.fullmatch(line):
                node = tree.min()
                if node is None:
                    continue
                print(f"{node.key} {node.value}")
            elif print_re.fullmatch(line):
                print_tree(tree)
            elif delete_re.fullmatch(line):
                tree.delete(int(args[1]))
            elif line != "":
                raise Error
        except Error:
            print("error")

    # test.close()


if __name__ == "__main__":
    main()
