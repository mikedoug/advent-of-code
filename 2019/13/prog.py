import time
import curses
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

program = computer.Computer(code)
# program.trace = True

## STEP ONE
grid = {}
while program.get_state() != computer.State.HALT:
    program.execute([])
    outputs = program.get_outputs()
    for i in range(0,len(outputs),3):
        grid[(outputs[i], outputs[i+1])] = outputs[i+2]

    program.clear_outputs()

print(f'Step One: {len(list(filter(lambda x: x == 2, grid.values())))}')


## STEP TWO
win = curses.initscr()
curses.curs_set(0) # pylint: disable=no-member
curses.noecho()    # pylint: disable=no-member
win.clear()
win.nodelay(True)

#        EMPTY, WALL,    BLOCK,    HPADDLE, BALL
blocks = [' ', '\u2589', '\u220e', '\u2589', '\u25cf']
blocks = [' ', 'X',      '.',      'T',      '*']

grid = {}

ballx = None
paddlex = None
score = None

code[0] = 2
program = computer.Computer(code)
inputs = []
while program.get_state() != computer.State.HALT:
    program.execute(inputs)
    outputs = program.get_outputs()
    if len(outputs) == 0:
        break
    for i in range(0,len(outputs),3):
        x, y, a = outputs[i:i+3]
        # grid[(outputs[i], outputs[i+1])] = outputs[i+2]
        # win.addch(outputs[i+1], outputs[i], blocks[outputs[i+2]])
        if x == -1 and y == 0:
            score = a
            win.addstr(0, 5, f'Score: {a}    ')
        else:
            win.addch(y+2, x, blocks[a])
            if a == 3:
                paddlex = x
            elif a == 4:
                ballx = x

    program.clear_outputs()
    win.refresh()
    
    if paddlex < ballx:
        inputs = [1]
    elif paddlex > ballx:
        inputs = [-1]
    else:
        inputs = [0]

    if win.getch() != -1:
        score = None
        break

    # time.sleep(0.05)

    # c = win.getch()
    # if int(c) == 97: # 'a'
    #     inputs = [-1]
    # elif int(c) == 100: # 'd'
    #     inputs = [1]
    # else:
    #     inputs = [0]

print(f"Step 2: {score}")