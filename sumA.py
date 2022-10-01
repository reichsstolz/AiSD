import sys


def parse(string):
    num = '0'
    sum_num = 0
    found_digit = False
    for symbol in string:

        if symbol == "-" and not found_digit:
            found_digit = True
            num = "-" + num

        elif symbol.isdigit():
            found_digit = True
            num += symbol

        elif found_digit:
            found_digit = False
            # print(num, sum_num)
            sum_num += int(num)
            num = '0'

    sum_num += int(num)
    return sum_num


if __name__ == "__main__":
    result = 0

    for line in sys.stdin:
        line = line.replace('\n', '')

        result += parse(line)
    print(result)
