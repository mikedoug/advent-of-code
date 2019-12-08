import unittest

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))
# pylint: disable=import-error
import computer
# pylint: enable=import-error

class TestComputer(unittest.TestCase):
    def setUp(self):
        with open("program.txt", "r") as f:
            self.program = list(map(lambda x: int(x), f.readline().rstrip().split(",")))

    def test_1(self):
        program = computer.Computer(self.program)
        results = program.execute([1])
        self.assertEqual(results[-1], 5182797)

    def test_5(self):
        program = computer.Computer(self.program)
        results = program.execute([5])
        self.assertEqual(results, [12077198])


if __name__ == '__main__':
    unittest.main()