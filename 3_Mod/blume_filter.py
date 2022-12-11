import re
import sys
from math import log2, log, ceil, sqrt


class Error(Exception):
    pass


class BitArray:
    def __init__(self, bitarray_size: int):
        self.__size = bitarray_size
        self.__array = bytearray()
        self.__array.extend([0] * (ceil(bitarray_size / 8)))

    def set(self, ind: int):
        bit_ind = 7 - ind % 8
        bit = 2 ** bit_ind

        if ind >= self.__size or ind < 0:
            raise Error

        self.__array[ind // 8] |= bit

    def get(self, ind: int) -> bool:
        bit_ind = 7 - ind % 8
        bit = 2 ** bit_ind

        if ind >= self.__size or ind < 0:
            raise Error

        return self.__array[ind // 8] & bit != 0

    def __len__(self):
        return self.__size

    def get_array(self):
        return "".join([bin(a)[2:].zfill(8) for a in self.__array])[:self.__size]
        # return [int(self.get(i)) for i in range(self.size)]


def init_primes(n) -> list[int]:
    if n < 6:  # оценка простых чисел работает для n>=6
        return [2, 3, 5, 7, 11][:n]
    estimation = round(n * log(n) + n * log(log(n)))
    sieve = BitArray(estimation)
    for i in range(3, int(sqrt(estimation)) + 1, 2):
        if not sieve.get(i):
            for j in range(i * i, estimation, 2 * i):
                sieve.set(j)
    primes = [2] + [i for i in range(3, estimation, 2) if not sieve.get(i)]
    return primes[:n]


def get_new_hash_function(i, m, prime, l_bitarray):
    return lambda x: (((i + 1) * x + prime) % m) % l_bitarray


def init_hash_functions(n_hash, l_bitarray):
    m = 2 ** 31 - 1
    primes = init_primes(n_hash)
    return [get_new_hash_function(i, m, primes[i], l_bitarray) for i in range(n_hash)]


class BlumeFilter:

    def __init__(self, l_bitarray, hash_functions):
        self.__bitarray = BitArray(l_bitarray)
        self.__hash_functions = hash_functions

    def add(self, x):
        if x < 0:
            raise Error
        for f in self.__hash_functions:
            ind = f(x)
            self.__bitarray.set(ind)

    def search(self, x):
        for f in self.__hash_functions:
            ind = f(x)
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
            if set_re.fullmatch(line) and not blume_filter:
                n = float(args[1])
                p = float(args[2])
                if p <= 0 or p >= 1 or n <= 0:
                    raise Error
                size = round(((-n) * log2(p)) / log(2))
                n_hash_func = round(-log2(p))
                if size <= 0 or n_hash_func <= 0:
                    raise Error
                blume_filter = BlumeFilter(size, init_hash_functions(n_hash_func, size))
                print(size, n_hash_func)

            elif add_re.fullmatch(line) and blume_filter:
                blume_filter.add(int(args[1]))
                # print(blume_filter.get_bit_array())

            elif search_re.fullmatch(line) and blume_filter:
                print(int(blume_filter.search(int(args[1]))))

            elif print_re.fullmatch(line) and blume_filter:
                # print("".join(map(str, blume_filter.get_array())))
                print(blume_filter.get_bit_array())

            elif line != "":
                raise Error

        except Error:
            print("error")
