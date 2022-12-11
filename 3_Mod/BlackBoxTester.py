import subprocess
from subprocess import *

TEST_DIR = "A_test"
TEST_N = 3
PROGRAM = "blume_filter"


def main():
    for i in range(1, TEST_N + 1):
        with open(f"{TEST_DIR}/{i}test.txt") as file:
            test = file.read()
        res = subprocess.run(["python3.10", f"{PROGRAM}.py"], stdout=PIPE, input=test, encoding="utf-8")
        out = res.stdout
        with open(f"{TEST_DIR}/{i}ans.txt") as file:
            ans = file.read()
        if ans == out:
            print(f"TEST {i} passed")
        else:
            print(f"TEST {i} failed")
            answer = ans.split("\n")
            output = out.split("\n")
            print(output)
            print(answer)
            min_len = min(len(output), len(answer))
            i = 0
            while answer[i] == output[i] and i < min_len:
                i += 1
            print(f"ANSWER:\n{answer[i]}\nOUTPUT:\n{output[i]}")


if __name__ == "__main__":
    main()
