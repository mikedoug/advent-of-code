import unittest
# pylint: disable=import-error
import computer
# pylint: enable=import-error

class TestComputer(unittest.TestCase):
    def setUp(self):
        with open("../05/program.txt", "r") as f:
            self.program = list(map(lambda x: int(x), f.readline().rstrip().split(",")))

    def test_1(self):
        program = computer.Computer(self.program)
        results = program.execute([1])
        self.assertEqual(results[-1], 5182797)

    def test_5(self):
        program = computer.Computer(self.program)
        results = program.execute([5])
        self.assertEqual(results, [12077198])

    def test_add(self):
        program = computer.Computer([1101,2,3,7,4,7,99,0])
        self.assertEqual(program.execute([]), [5])
        program = computer.Computer([1001,7,3,7,4,7,99,2])
        self.assertEqual(program.execute([]), [5])
        program = computer.Computer([1,7,6,7,4,7,99,2])
        self.assertEqual(program.execute([]), [101])

    def test_mul(self):
        program = computer.Computer([1102,2,3,7,4,7,99,0])
        self.assertEqual(program.execute([]), [6])
        program = computer.Computer([1002,7,3,7,4,7,99,2])
        self.assertEqual(program.execute([]), [6])
        program = computer.Computer([2,7,6,7,4,7,99,2])
        self.assertEqual(program.execute([]), [198])

    def test_input(self):
        program = computer.Computer([3,9,1002,9,3,9,4,9,99,0])
        self.assertEqual(program.execute([2]), [6])

        program = computer.Computer([3,11,3,12,2,11,12,11,4,11,99,0,0])
        self.assertEqual(program.state, computer.State.INIT)
        self.assertEqual(program.safe_execute([2]), None)
        self.assertEqual(program.state, computer.State.WAIT)
        self.assertEqual(program.safe_execute([3]), [6])
        self.assertEqual(program.state, computer.State.HALT)


if __name__ == '__main__':
    unittest.main()