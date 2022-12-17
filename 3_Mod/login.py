import sys


class LogSystemError(Exception):
    pass


class LoginSystem:
    def __init__(self, attempts, block_period, b, b_max, unix_time, login_time):
        self.block_end = 0
        self.attempts = attempts
        self.block_period = block_period
        self.b_cur = b
        self.b_max = b_max
        self.unix_time = unix_time
        self.last_login = -1
        self.next_login = -1
        self.login_time = login_time
        for i in range(len(self.login_time)):
            self.login(i)

    def block(self):
        self.block_end = self.login_time[self.next_login] + self.b_cur
        self.b_cur *= 2
        if self.b_cur > self.b_max:
            self.b_cur = self.b_max
        self.last_login = -1
        self.next_login = -1

    def login(self, index: int):
        if 2 * self.b_max <= self.unix_time - self.login_time[index]:
            return
        elif self.next_login == self.last_login == -1:
            self.last_login = index
            self.next_login = index
            if self.attempts == 1:
                self.block()
            return

        if self.login_time[index] - self.login_time[self.last_login] > self.block_period:
            self.last_login += 1
            self.next_login += 1
            return
        else:
            self.next_login += 1

        if self.next_login - self.last_login + 1 == self.attempts:
            self.block()


def main():
    init_args = input().split()
    attempts = []
    for line in sys.stdin:
        line = line.rstrip("\n")
        attempts.append(int(line))
    system = LoginSystem(int(init_args[0]), int(init_args[1]), int(init_args[2]), int(init_args[3]), int(init_args[4]),
                         sorted(attempts))

    if system.unix_time <= system.block_end:
        print(system.block_end)
    else:
        print("ok")


if __name__ == "__main__":
    main()

#  Cложность по времени O(nlogn)
#  Обработка O(n)
#  sorted использует сортировку Timsort - O(nlogn)
#  По памяти O(n)