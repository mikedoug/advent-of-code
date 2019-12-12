BLACK = 0
WHITE = 1

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

grid = {(0,0): WHITE}
location = (0, 0)
facing = -1j

while program.get_state() != computer.State.HALT:
    color = grid.get(location, BLACK)
    program.execute([color])

    new_color, turn = program.get_outputs()
    program.clear_outputs()

    grid[location] = new_color
    facing *= 1j if turn == 1 else -1j
    location = (location[0] + int(facing.real), location[1] + int(facing.imag))

print(f'Stage one: {len (grid)}')

minx = min(grid.keys(), key=lambda x: x[0])[0]
miny = min(grid.keys(), key=lambda x: x[1])[1]

minx = min([x[0] for x in grid])
miny = min([x[1] for x in grid])
maxx = max([x[0] for x in grid])
maxy = max([x[1] for x in grid])

print('Stage two:')
# for y in range(maxy, miny - 1, -1):
for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        if grid.get((x,y), BLACK) == WHITE:
            print("XX", end="")
        else:
            print("  ", end="")
    print()