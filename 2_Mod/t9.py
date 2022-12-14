import sys
from typing import *


class NodeError(Exception):
    pass


class TrieError(Exception):
    pass


class Damerau_Levinstein:
    INF = sys.maxsize

    @staticmethod
    def __make_matrix(key: str, string: str) -> list[list[int]]:
        """
        Делает начальную матрицу
        """
        l_key = len(key)
        l_str = len(string)

        d = [[0] * (l_str + 2) for i in range(l_key + 2)]
        # INF = (l_key + l_str)
        d[0][0] = Damerau_Levinstein.INF

        for i in range(1, l_key + 2):
            d[i][1] = i - 1
            d[i][0] = Damerau_Levinstein.INF
        for j in range(1, l_str + 2):
            d[1][j] = j - 1
            d[0][j] = Damerau_Levinstein.INF
        return d

    @staticmethod
    def update_distance(key: str, string: str, prev_d=None, prev_last_pos=None):
        """
        Считает расстояние дамерау-левенштейна.
        Сложность O(l_key*l_string)
        Сложность по памяти O(l_key*l_string)
        В данном случае счёт происходит с определённого оффсета.
        prev_d - таблица с предыдущего шага
        prev_last_pos - словарь с последней позицией символа
        """
        l_key = len(key)
        l_string = len(string)
        last_pos = dict()

        if prev_d is None:
            new_d = Damerau_Levinstein.__make_matrix(key, string)
            offset = 0

            for i in key + string:
                if i not in last_pos:
                    last_pos[i] = 0
        else:
            new_d = []
            new_d.extend(prev_d)
            offset = len(new_d) - 2
            last_pos = prev_last_pos.copy()

            for i in range(new_d[-1][1], new_d[-1][1] + l_key):
                new_d.extend([[Damerau_Levinstein.INF, i + 1] + [0] * l_string])

            for i in key:
                if i not in last_pos:
                    last_pos[i] = 0

        for i in range(1 + offset, len(key) + 1 + offset):
            last = 0
            for j in range(1, len(string) + 1):
                _i = last_pos[string[j - 1]]
                _j = last
                if key[i - offset - 1] == string[j - 1]:
                    new_d[i + 1][j + 1] = new_d[i][j]
                    last = j
                else:
                    new_d[i + 1][j + 1] = min(new_d[i][j],
                                              new_d[i + 1][j],
                                              new_d[i][j + 1]) + 1
                new_d[i + 1][j + 1] = min(new_d[i + 1][j + 1],
                                          new_d[_i][_j] + i - _i + j - _j - 1)
            last_pos[key[i - offset - 1]] = i
        return new_d, last_pos


def prefix_len(first: str, second: str) -> int:
    """
    Вычисление одинакового префикса
    Сложность O(min(len(first), len(second)))
    Сложность по памяти O(1)
    """
    eq = 0
    for i in range(min(len(first), len(second))):
        if first[i] == second[i]:
            eq += 1
            continue
        break
    return eq


class Node:
    def __init__(self, key=None, word=None):
        self.key = key
        self.kids = dict()
        self.word = word

    def add_kid(self, new):
        sibling = self.kids.get(new.key[0])
        if sibling:
            raise NodeError
        self.kids[new.key[0]] = new

    def get(self, string: str):
        return self.kids.get(string)

    def get_all(self):
        return self.kids.values()

    def split(self, ind: int, word=None):
        """
        Разделение ноды префиксного дерева по определённому индексу
        Сложность O(1)
        Сложность по памяти O(1)
        """
        if ind > len(self.key) or not self.key:
            raise NodeError

        old_word = self.word
        self.word = None
        if word:
            self.word = word

        if ind == len(self.key):
            self.word = old_word

        new_string, self.key = Node(key=self.key[ind:], word=old_word), self.key[:ind]
        new_string.kids = self.kids
        self.kids = dict()
        self.kids[new_string.key[0]] = new_string


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str):
        """
        Вставка в префиксное дерево
        Сложность O(len(word))
        Cложность по памяти O(1)
        """
        cur: Node = self.root
        string = word

        while string:
            new: Node = cur.get(string[0])

            if new and string.startswith(new.key):
                string = string[len(new.key):]
                if not string:
                    new.word = word
                    break
                cur = new

            elif new:
                ind = prefix_len(new.key, string)
                string = string[ind:]
                if not string:
                    new.split(ind=ind, word=word)
                    break
                new.split(ind=ind)
                cur = new

            else:
                cur.add_kid(Node(key=string, word=word))
                string = ""

    @staticmethod
    def __search(word: str, cur: Node, found: list, prev_d=None, prev_last_pos=None):
        """
        word - искомое слово
        сur - текущая нода
        found - список найденных слов
        prev_d - прошлая матрица для дамерау-левенштейна
        prev_last_pos - последняя позиция символа для дамерау-левенштейна
        Сложность по времени = вычисление расстояния Дамерау-Левенштейна + рекурсивный обход детей текущей
        вершины (если расстояние <= 1).
        Потомков в худшем случае N-1
        Общая Сложность O(N*len(string)*len(cur.key)), где N число вершин в дереве
        Сложность по памяти O(len(found))
        """
        new_d, new_last_pos = Damerau_Levinstein.update_distance(cur.key, word, prev_d, prev_last_pos)
        if new_d[-1][-1] <= 1 and cur.word is not None:
            found.append(cur.word)
            for new in cur.get_all():
                Trie.__search(word, new, found, new_d, new_last_pos)

        elif min(new_d[-1]) <= 1:
            for new in cur.get_all():
                Trie.__search(word, new, found, new_d, new_last_pos)

    def search(self, word: str):
        found = []
        for i in self.root.get_all():
            self.__search(word, i, found)
        return found


if __name__ == "__main__":
    trie = Trie()
    n = input()
    n = int(n)
    while n != 0:
        s = input()
        if not s:
            continue
        n -= 1
        trie.insert(s.lower())
    for line in sys.stdin:
        line = line.replace('\n', '')
        if len(line) == 0:
            continue
        found = trie.search(line.lower())
        print(line, end=" ")
        if line.lower() in found:
            print("- ok")
        elif found:
            print(f"-> {', '.join(sorted(found))}")
        else:
            print("-?")
