BLACK = 0
WHITE = 1

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))
# pylint: disable=import-error
import computer
# pylint: enable=import-error

with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

program = computer.Computer(code)
# program.trace = True

grid = {}
x = 0
y = 0
facing = UP

first = True

while program.state != computer.State.HALT:
    color = grid[(x,y)] if (x,y) in grid else WHITE if first else BLACK
    first = False
    program.execute([color])

    new_color, turn = program.outputs
    program.outputs = []

    grid[(x,y)] = new_color

    facing = (facing + (3 if turn == 0 else 1)) % 4
    if facing == UP:
        y += 1
    elif facing == DOWN:
        y -= 1
    elif facing == LEFT:
        x -= 1
    else:
        x += 1

print(f'Stage one: {len (grid)}')

minx = min(grid.keys(), key=lambda x: x[0])[0]
miny = min(grid.keys(), key=lambda x: x[1])[1]

minx = min([x[0] for x in grid])
miny = min([x[1] for x in grid])
maxx = max([x[0] for x in grid])
maxy = max([x[1] for x in grid])

print('Stage two:')
for y in range(maxy, miny - 1, -1):
    for x in range(minx-2, maxx+2):
        if (x,y) in grid and grid[(x,y)] == WHITE:
            print("X", end="")
        else:
            print(" ", end="")

    print()