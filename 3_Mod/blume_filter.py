import re
import sys
from math import log2, log, ceil, e

PRIMES = list()


class Error(Exception):
    pass


class BitArray:
    def __init__(self, size: int):
        self.size = size
        self.__array = bytearray()
        self.__array.extend([0] * ceil(size / 8))

    def set(self, ind: int, val: bool):
        array_ind = ind // 8
        bit_ind = 7 - ind % 8
        bit = 2 ** bit_ind

        if array_ind > self.size:
            raise IndexError

        if val and (self.__array[array_ind] < bit or bin(self.__array[array_ind])[::-1][bit_ind] == "0"):
            self.__array[array_ind] += bit
        elif not val and self.__array[array_ind] >= bit:
            if bin(self.__array[array_ind])[::-1][bit_ind] == "1":
                self.__array[array_ind] -= bit

    def get(self, ind: int) -> bool:
        array_ind = ind // 8
        bit_ind = 7 - ind % 8
        bit = 2 ** bit_ind

        if array_ind > self.size:
            raise IndexError

        if self.__array[array_ind] >= bit and bin(self.__array[array_ind])[::-1][bit_ind] == "1":
            return True
        return False

    def get_array(self):
        return "".join([bin(a)[2:].zfill(8) for a in self.__array])[:self.size]


def init_primes(n):
    if n <= 6:  # оценка простых чисел работает до n<=6
        return [2, 3, 5, 7, 11, 13]
    sieve = [i for i in range(round(n * (log(n) + log(log(n))) + 1))]
    i = 2
    l_sieve = len(sieve)
    while i < l_sieve:
        if sieve[i] != 0:
            j = i ** 2
            while j < len(sieve):
                sieve[j] = 0
                j = j + i
        i += 1
    sieve = set(sieve)
    sieve.remove(0)
    sieve.remove(1)
    return list(sieve)


class BlumeFilter:
    M = 2 ** 31 - 1

    def __init__(self, size, n_hash_func):
        self.__bitarray = BitArray(size)  # проверить правильное округление
        self.__n_hash_func = n_hash_func

    def __hash_func(self, i, x, pi):
        return (((i + 1) * x + pi) % self.M) % self.__bitarray.size

    def add(self, x):
        for i in range(self.__n_hash_func):
            ind = self.__hash_func(i, x, PRIMES[i])
            self.__bitarray.set(ind, True)

    def search(self, x):
        for i in range(self.__n_hash_func):
            ind = self.__hash_func(i, x, PRIMES[i + 1])
            if not self.__bitarray.get(ind):
                return False
        return True

    def get_bit_array(self):
        return self.__bitarray.get_array()


if __name__ == "__main__":
    set_re = re.compile(r"set (\d+\.\d+|\d+) (\d+\.\d+|\d+)")
    add_re = re.compile(r"add (\d+)")
    search_re = re.compile(r"search (\d+)")
    print_re = re.compile(r"print")
    blume_filter = None

    for line in sys.stdin:
        line = line.rstrip('\n')
        args = line.split()

        try:
            if set_re.fullmatch(line):
                n = float(args[1])
                p = float(args[2])
                size = round(((-n) * log2(p)) / log(2))
                n_hash_func = round(-log2(p))
                blume_filter = BlumeFilter(size, n_hash_func)
                PRIMES = init_primes(n_hash_func)
                print(size, n_hash_func)

            elif add_re.fullmatch(line) and blume_filter:
                blume_filter.add(int(args[1]))
                print(blume_filter.get_bit_array())

            elif search_re.fullmatch(line) and blume_filter:
                print(int(blume_filter.search(int(args[1]))))

            elif print_re.fullmatch(line) and blume_filter:
                print(blume_filter.get_bit_array())

            elif line != "":
                raise Error

        except Error:
            print("error")
