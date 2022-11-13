from typing import Optional


class NodeError(Exception):
    pass


class TrieError(Exception):
    pass


def damerau_levinstein():
    pass


class Node:
    def __init__(self, key=None):
        self.key = key
        self.kids = dict()
        self.is_word = False

    def add_kid(self, new):
        sibling = self.kids.get(new.key[0])
        if sibling and sibling.key == new.key:
            raise NodeError
        self.kids[new.key[0]] = new

    def presearch_keys(self, string) -> set[str]:
        length = len(string)
        return set(key for key in self.kids.keys() if abs(length - len(key)) < 3)

    def get(self, string: str):
        return self.kids.get(string)

    def get_all(self):
        return self.kids.keys()

    @staticmethod
    def compare(first: str, second: str) -> int:
        eq = 0
        for i in range(min(len(first), len(second))):
            if first[i] == second[i]:
                eq += 1
                continue
            break
        return eq

    def split(self, ind, is_word=False):

        if ind > len(self.key) or not self.key:
            raise NodeError

        self.is_word = False
        if is_word:
            self.is_word = True

        if ind == len(self.key):
            self.is_word = True

        new_string, self.key = Node(self.key[ind:]), self.key[:ind]
        new_string.kids = self.kids
        self.kids = dict()
        self.kids[new_string.key[0]] = new_string
        new_string.is_word = True


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        cur: Node = self.root
        string = word
        while string:
            new: Node = cur.get(string[0])
            if new:
                ind = Node.compare(new.key, string)
                string = string[ind:]
                if not string:
                    new.split(ind, True)
                    break
                cur = new
            else:
                cur.add_kid(Node(string))
                string = ""
