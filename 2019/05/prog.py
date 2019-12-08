import unittest

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))
# pylint: disable=import-error
import computer
# pylint: enable=import-error

def run(value):
    with open("program.txt", "r") as f:
        program = list(map(lambda x: int(x), f.readline().rstrip().split(",")))
    program = computer.Computer(program)
    results = program.execute([value])
    print (results)

run(1)
run(5)

if __name__ == '__main__':
    unittest.main()