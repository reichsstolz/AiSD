import random
from math import log2, log, ceil, e, floor, sqrt
from blume_filter import BlumeFilter, init_primes, init_hash_functions
from blume_filter import BitArray as mybit

class BitArray:
    def __init__(self, size: int):
        self.__bit_size = size
        self.__byte_size = ceil(size / 8)
        self.__set = bytearray(self.__byte_size)

    def set(self, index: int):
        if index < 0 or index >= self.__bit_size:
            raise IndexError("out of range")
        self.__set[index >> 3] |= 1 << (index % 8)

    def set_range(self, indexes):
        for index in indexes:
            self.set(index)

    def get(self, index) -> bool:
        if index < 0 or index >= self.__bit_size:
            raise IndexError("out of range")
        return (self.__set[index >> 3] & (1 << index % 8)) != 0

    def get_range(self, indexes) -> list[bool]:
        return [self.get(index) for index in indexes]

    def __iter__(self):
        for bit in range(self.__bit_size):
            yield self.get(bit)

    def __len__(self) -> int:
        return self.__bit_size


def generate_primes(count: int) -> list[int]:
    # Чтобы найти максимальное простое число используем формулу n * logn + n * log(log(n)), n >= 6
    # Из-за этого мы на самом деле рассчитываем чуть больше простых чисел, чем нужно
    if count < 6:
        return [2, 3, 5, 7, 11][:count:]
    num_count = floor(count * log(count) + count * log(log(count)))
    sieve = BitArray(num_count)
    for i in range(3, int(sqrt(num_count)) + 1, 2):
        if not sieve.get(i):
            sieve.set_range(range(i * i, num_count, 2 * i))
    result = [2] + [i for i in range(3, num_count, 2) if not sieve.get(i)]
    return result[:count:]


if __name__ == "__main__":

    test0 = [bin(i)[2:][::-1] for i in random.sample(range(0, 10000), k=10000)]
    test0 = list(test0)

    for bit in test0:
        x = mybit(len(bit))
        for i in range(len(bit)):
            if bit[i] == "1":
                x.set(i)

        assert (x.get_array() == bit)
        for i in range(len(bit)):
            if bit[i] == "1":
                assert (x.get(i))
            else:
                assert (not x.get(i))
    size = random.sample(range(0, 1000000), k=1)[0]
    n_hash_func = random.sample(range(0, 1000), k=1)[0]

    test1 = random.sample(range(0, 1000000), k=10000)
    b = BlumeFilter(size, init_hash_functions(n_hash_func, size))
    for i in test1:
        b.add(i)
    for i in test1:
        assert (b.search(i))

    test2 = random.sample(range(0, 1000), k=2)
    x = init_primes(test2[0])
    y = generate_primes(test2[0])
    try:
        assert (x == y)
    except AssertionError:
        for i in range(len(x)):
            if x[i] != y[i]:
                print(i, x[i], y[i])
    assert (init_primes(test2[1]) == generate_primes(test2[1]))