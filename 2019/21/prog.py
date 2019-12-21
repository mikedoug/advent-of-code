import itertools
import copy
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

program = computer.Computer(code)

# (!A or !B or !C) and D
commandlist = [\
'''NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
'''   
,

# (!A or !B or !C) and D and (E or H)

'''NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
AND E T
OR E T
OR H T
AND T J
RUN
'''   
]


for cmd in commandlist:
    # cmd = '\n'.join(cmd) + '\nWALK\n'
    program = computer.Computer(code)
    program.execute([])
    while(program.get_state() != computer.State.HALT):
        print(''.join([chr(x) for x in program.get_outputs()]), end='')
        # cmd = input("> ") + chr(10)
        program.clear_outputs()

        print(f'Sending:\n{cmd}')
        program.execute([ord(x) for x in cmd])

        outputs = program.get_outputs()
        if len(outputs) > 0 and (outputs[0] > 255):
            break

    # outputs = program.get_outputs()
    for x in outputs:
        if x < 256:
            print(chr(x), end='')
        else:
            print(f'\n{x}\n')
