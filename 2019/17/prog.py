import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

program = computer.Computer(code)
program.execute([])

class Tracker(object):
    direction = '^>v<'
    def __init__(self,computer):
        self.memory = {}
        self.robot = None
        x = 0
        y = 0
        while True:
            try:
                i = computer.pop_output()
            except IndexError:
                break
            if i == 10:
                if x == 0 and y == 0:
                    # Junk 10 at the start
                    continue
                if x == 0:
                    # A double newline, end graph
                    break
                y += 1
                x = 0
            else:
                self.memory[(x,y)] = chr(i)
                c = chr(i)
                if c in Tracker.direction:
                    self.robot = (x,y)
                x += 1

        self.count_x = max(self.memory.keys(), key=lambda x: x[0])[0] + 1
        self.count_y = max(self.memory.keys(), key=lambda x: x[1])[1] + 1

    def print(self):
        for y in range(0, self.count_y):
            for x in range(0, self.count_x):
                c = self.memory.get((x,y), '&')
                print(c, end='')
            print()

    def find_intersections(self):
        results = []
        for y in range(0, self.count_y):
            for x in range(0, self.count_x):
                if self.memory.get((x,y), '&') == '#' and self.memory.get((x-1,y), '&') == '#' and self.memory.get((x+1,y), '&') == '#' and self.memory.get((x,y-1), '&') == '#' and self.memory.get((x,y+1), '&') == '#':
                    results.append((x,y))
        return results

    def walk(self):
        pos = self.robot
        last_dir = 'UP'

        print(f'START {pos}')
        while True:
            if last_dir != 'RIGHT' and self.memory.get((pos[0]-1,pos[1]), '&') == '#':
                # Left
                for i in range(500):
                    if self.memory.get((pos[0]-i-1,pos[1]), '&') != '#':
                        break
                turn = '<==' if last_dir == 'UP' else '==>'
                print(f'{turn} {i} -- LEFT {pos}')
                pos = (pos[0] - i, pos[1])
                last_dir = 'LEFT'
            elif last_dir != 'LEFT' and self.memory.get((pos[0]+1,pos[1]), '&') == '#':
                # Right
                for i in range(0,500):
                    if self.memory.get((pos[0]+i+1,pos[1]), '&') != '#':
                        break
                turn = '==>' if last_dir == 'UP' else '<=='
                print(f'{turn} {i} -- RIGHT {pos}')
                pos = (pos[0] + i, pos[1])
                last_dir = 'RIGHT'
            elif last_dir != 'DOWN' and self.memory.get((pos[0],pos[1]-1), '&') == '#':
                # Up
                for i in range(0,500):
                    if self.memory.get((pos[0],pos[1]-i-1), '&') != '#':
                        break
                turn = '==>' if last_dir == 'LEFT' else '<=='
                print(f'{turn} {i} -- UP {pos}')
                pos = (pos[0], pos[1] - i)
                last_dir = 'UP'
            elif last_dir != 'UP' and self.memory.get((pos[0],pos[1]+1), '&') == '#':
                # Down
                for i in range(0,500):
                    if self.memory.get((pos[0],pos[1]+i+1), '&') != '#':
                        break
                turn = '==>' if last_dir == 'RIGHT' else '<=='
                print(f'{turn} {i} -- DOWN {pos}')
                pos = (pos[0], pos[1] + i)
                last_dir = 'DOWN'
            else:
                break


tracker = Tracker(program)
tracker.print()

intersections = tracker.find_intersections()

print(sum([x[0] * x[1] for x in intersections]))

tracker.walk()

code[0] = 2
program = computer.Computer(code)

def mapit(command):
    response = []
    for line in command:
        response.append([ord(x) for x in line] + [10])

    return response

commands = mapit([
    "A,B,A,C,A,B,C,A,B,C",
    "R,8,R,10,R,10",
    "R,4,R,8,R,10,R,12",
    "R,12,R,4,L,12,L,12",
    "n"
])

program.execute([])

t = Tracker(program)
t.print()

for i in range(5):
    print (">> " + ''.join([chr(x) for x in program.get_outputs()]), end='')
    print ("<< " + ''.join([chr(x) for x in commands[i]]), end='')

    program.clear_outputs()
    program.execute(commands[i])

t = Tracker(program)
t.print()
print (program.get_outputs())
program.clear_outputs()

print (program.get_state())
