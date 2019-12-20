import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]


# row, column
points = [(0,0)]
rows = {0: (0,0), 1: (-1, -1), 2: (-1, -1)}

# for row in range(3,9999999999999):
for row in range(760,9999999999999):
    try:
        col = min(map(lambda x: x[1], filter(lambda x: x[0] == row - 1, points))) - 1
    except:
        col = 0
    found = False
    start_col = None
    while True:
        program = computer.Computer(code)
        program.execute([col, row])
        output = program.pop_output()
        # print(f' -- {col} {row} {output}')
        if output == 1:
            if start_col is None:
                start_col = col
            points.append((row, col))
            found = True
        elif found:
            break
        col += 1

    if start_col is None:
        rows[row] = (-1, -1)
    else:
        rows[row] = (start_col, col -1)


    find_size = 100
    if row + 1 >= find_size:
        print(f'{row} width={rows[row][1] - rows[row][0] + 1} {rows[row]}')
        # print (f'Row: {row} {rows[row]}  {row-find_size+1} {rows[row-find_size+1]}')
        right_col = rows[row][0] + find_size - 1
        if right_col <= rows[row][1]:
            top_row = row - find_size + 1
            if top_row in rows and rows[top_row][0] <= rows[row][0] and \
                right_col <= rows[top_row][1]:
                print(f'Found square at {row-find_size+1} {rows[row][0]}  {rows[row][0]*10000 + row-find_size+1}')
                break




# print (len(points))

# for row in range(50):
#     print(f'{row:5} ', end='')
#     for col in range(50):
#         if (row, col) in points:
#             print ("#", end='')
#         else:
#             print (".", end='')
#     print(f' {rows[row] if row in rows else ""}')