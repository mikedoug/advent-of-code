import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))
# pylint: disable=import-error
import computer
# pylint: enable=import-error

with open("program.txt", "r") as f:
    program = [int(x) for x in f.readline().rstrip().split(",")]

# Step 1
step1_program = [program[0], 12, 2] + program[3:]
step1_computer = computer.Computer(step1_program)
step1_computer.execute()
print(f"Step 1 answer: {step1_computer.memory[0]}")

# Step 2
for a in range(0,100):
    for b in range(0,100):
        step2_program = [program[0], a, b] + program[3:]

        step2_computer = computer.Computer(step2_program)
        step2_computer.execute()
        if step2_computer.memory[0] == 19690720:
            print(f'Step 2 answer: {a * 100 + b}')
            sys.exit(0)
