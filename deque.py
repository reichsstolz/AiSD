import re
import sys

class Deque:
    def __init__(self, size):
        self.size = size
        self.massiv = [None] * size
        self.top = -1
        self.tail = -1
        self.count = 0

    def pushf(self, value):
        if self.size == self.count:
            print("overflow")
            return

        self.top = (self.top - 1) % self.size

        if not self.count:
            self.top = self.size // 2
            self.tail = self.size // 2

        self.count += 1
        self.massiv[self.top] = value
        return

    def pushb(self, value):
        if self.size == self.count:
            print("overflow")
            return

        self.tail = (self.tail + 1) % self.size

        if not self.count:
            self.top = self.size // 2
            self.tail = self.size // 2

        self.count += 1
        self.massiv[self.tail] = value
        return

    def popb(self):
        if not self.count:
            print("underflow")
            return

        tail = self.massiv[self.tail]
        self.tail = (self.tail - 1) % self.size
        self.count -= 1

        if not self.count:
            self.top = self.tail = -1

        return tail

    def print(self):
        if not self.count:
            print("empty")
            return

        ind = self.top
        values = []
        for i in range(self.count):
            values.append(self.massiv[ind])
            ind = (ind + 1) % self.size
        print(" ".join(values))
        # print(self.massiv)
        # print(self.top)
        # print(self.tail)

    def popf(self):
        if not self.count:
            print("underflow")
            return

        front = self.massiv[self.top]
        self.top = (self.top + 1) % self.size
        self.count -= 1

        if not self.count:
            self.top = self.tail = -1

        return front


if __name__ == "__main__":
    #command_re = re.compile("(pushb|pushf|set_size) ([^\S]+)")
    pushb_re = re.compile("pushb ([\\S]+)$")
    pushf_re = re.compile("pushf ([\\S]+)$")
    popb_re = re.compile("popb$")
    popf_re = re.compile("popf$")
    set_size_re = re.compile("set_size ([\\d]+)$")
    print_re = re.compile("print$")
    deque = None
    for line in sys.stdin:
        line = line.replace('\n', '')
        arg = line.split()

        if re.match(set_size_re, line) and not deque:
            deque = Deque(int(arg[1]))
        elif re.match(pushb_re, line) and deque:
                deque.pushb(arg[1])
        elif re.match(pushf_re, line) and deque:
                deque.pushf(arg[1])
        elif re.match(popb_re, line) and deque:
            val = deque.popb()
            if val:
                print(val)
        elif re.match(popf_re, line) and deque:
            val = deque.popf()
            if val:
                print(val)
        elif re.match(print_re, line) and deque:
            deque.print()
        elif len(line) != 0:
            print('error')



"""
        if re.fullmatch(command_re, line):
            command, value = line.split(" ")

            if command == "pushb" and deque:
                deque.pushb(value)
                continue

            elif command == "pushf" and deque:
                deque.pushf(value)
                continue

            elif command == "set_size" and value.isdigit() and not deque:
                deque = Deque(int(value))
                continue

            else:
                print("error")
                continue

        elif not deque:
            print('error')
            continue

        elif re.fullmatch("(popb|popf|print)", line):

            if "print" == line:
                 deque.print()
                 continue

            elif "popb" == line:
                val = deque.popb()
                if val:
                    print(val)
                continue

            elif "popf" == line:
                val = deque.popf()
                if val:
                    print(val)
                continue

        elif line != "":
            print("error")
"""