import itertools

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))
# pylint: disable=import-error
import computer
# pylint: enable=import-error

with open("input.txt", "r") as f:
    # software = list(map(lambda x: int(x),f.readline().rstrip().split(",")))
    software = [int(x) for x in f.readline().rstrip().split(",")]


# For the single pass, I am a sucker for efficiency so this method keeps
# me from redoing calculations by doing a depth-first search.
def single_pass(stage=1, max_stage=5, input=0, used_phases=[]):
    outputs = []

    for a in range(5):
        if a in used_phases:
            continue
        program = computer.Computer(software)
        results = program.execute([a, input])
        output = results[0]

        if stage < max_stage:
            outputs += single_pass(stage+1, max_stage, output, used_phases + [a])
        else:
            return [output]

    return outputs

outputs = single_pass()
print (f"Maximum output part one: {max(outputs)}")
if max(outputs) != 929800:
    print("^^^^^^ FAIL ^^^^^^")


def feedback_loop(phases):
    programs = []
    for phase in phases:
        program = computer.Computer(software)
        program.safe_execute([phase])

        programs.append(program)

    input = 0
    while True:
        for program in programs:
            program.safe_execute([input])
            input = program.outputs[-1]

        if programs[-1].state == computer.State.HALT:
            return input

outputs = []
for permutation in itertools.permutations([5,6,7,8,9]):
    outputs.append(feedback_loop(permutation))

print (f"Maximum output part two: {max(outputs)}")
if max(outputs) != 15432220:
    print("^^^^^^ FAIL ^^^^^^")



