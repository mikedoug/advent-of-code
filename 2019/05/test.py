import unittest
import computer

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