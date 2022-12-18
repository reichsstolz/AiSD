import sys
from math import floor


class Item:
    def __init__(self, weight: int, price: int):
        self.weight = weight
        self.price = price
        self.indexes = set()

    def add(self, x):
        self.indexes.add(x)


class Knapsack:
    def __init__(self, p: float, max_weight: int, items: list[Item]):
        self.p = p
        self.max_weight = max_weight
        self.items = items
        self.weights: list[int] = [item.weight for item in items]
        self.prices: list[int] = [item.price for item in items]
        self.original_prices: list[int] = [item.price for item in items]
        self.fake_items = self.__init_fake_items()

    def __init_fake_items(self) -> list[Item]:
        k = 1
        if self.p != 0:
            k = len(self.items) / self.p / max(self.prices)
        if k < 1:
            self.prices = list(map(lambda x: floor(k * x), self.prices))
        return [Item(0, 0)] + [Item(self.max_weight + 1, 0) for _ in range(sum(self.prices) + 1)]

    def start(self):
        l_items = len(self.items)
        for i in range(l_items):
            x = sum(self.prices)
            while x >= self.prices[i]:
                dif = x - self.prices[i]
                if self.fake_items[dif].weight + self.weights[i] < self.fake_items[x].weight:
                    self.fake_items[x].price = self.fake_items[dif].price + self.original_prices[i]
                    self.fake_items[x].weight = self.fake_items[dif].weight + self.weights[i]
                    self.fake_items[x].indexes = self.fake_items[dif].indexes.copy()
                    self.fake_items[x].add(i)
                x -= 1

        for item in self.fake_items[::-1]:
            if item.weight <= self.max_weight:
                return item


def main():
    p = float(input())
    max_weight = int(input())
    items = list()

    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue
        weight, price = line.split()
        items.append(Item(int(weight), int(price)))

    knapsack = Knapsack(p, max_weight, items)
    solution = knapsack.start()
    print(solution.weight, solution.price)
    for i in solution.indexes:
        print(i + 1)


if __name__ == "__main__":
    main()
