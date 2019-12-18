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

        results = []
        print(f'START {pos}')
        while True:
            if last_dir != 'RIGHT' and self.memory.get((pos[0]-1,pos[1]), '&') == '#':
                # Left
                for i in range(500):
                    if self.memory.get((pos[0]-i-1,pos[1]), '&') != '#':
                        break
                turn = '<==' if last_dir == 'UP' else '==>'
                print(f'{turn} {i} -- LEFT {pos}')
                results.append(('L' if last_dir == 'UP' else 'R', i))
                pos = (pos[0] - i, pos[1])
                last_dir = 'LEFT'
            elif last_dir != 'LEFT' and self.memory.get((pos[0]+1,pos[1]), '&') == '#':
                # Right
                for i in range(0,500):
                    if self.memory.get((pos[0]+i+1,pos[1]), '&') != '#':
                        break
                turn = '==>' if last_dir == 'UP' else '<=='
                print(f'{turn} {i} -- RIGHT {pos}')
                results.append(('R' if last_dir == 'UP' else 'L', i))
                pos = (pos[0] + i, pos[1])
                last_dir = 'RIGHT'
            elif last_dir != 'DOWN' and self.memory.get((pos[0],pos[1]-1), '&') == '#':
                # Up
                for i in range(0,500):
                    if self.memory.get((pos[0],pos[1]-i-1), '&') != '#':
                        break
                turn = '==>' if last_dir == 'LEFT' else '<=='
                print(f'{turn} {i} -- UP {pos}')
                results.append(('R' if last_dir == 'LEFT' else 'L', i))
                pos = (pos[0], pos[1] - i)
                last_dir = 'UP'
            elif last_dir != 'UP' and self.memory.get((pos[0],pos[1]+1), '&') == '#':
                # Down
                for i in range(0,500):
                    if self.memory.get((pos[0],pos[1]+i+1), '&') != '#':
                        break
                turn = '==>' if last_dir == 'RIGHT' else '<=='
                print(f'{turn} {i} -- DOWN {pos}')
                results.append(('R' if last_dir == 'RIGHT' else 'L', i))
                pos = (pos[0], pos[1] + i)
                last_dir = 'DOWN'
            else:
                break

        return results

def multicount_splatter(partial, full):
    splatted = list(full)
    skip_until = None
    count = 0
    for i in range(len(full)-len(partial)+1):
        if skip_until is not None and i < skip_until:
            continue
        if full[i:i+len(partial)] == partial:
            count += 1
            skip_until = i + len(partial)
            splatted[i:i+len(partial)] = [None] * len(partial)

    return (count,splatted)

def decompose_analysis(startpath, maxsegments=3):
    states = [[startpath,[]]]
    complete = []
    while len(states) > 0:
        path, history = states.pop(0)

        # Always start with the first non-None entry
        start = list(filter(lambda x: x[1] is not None, enumerate(path))).pop(0)[0]

        # Find all sub-strings starting from there that repeat, and enqueue it for futher analysis
        for i in range(1,len(path)):
            search = path[start:start+i]
            if search[-1] is None:
                break

            (count, filtered) = multicount_splatter(search, path)
            if count > 1:
                if any(filter(lambda x: x is not None, filtered)):
                    if len(history) < maxsegments - 1:
                        states.append([filtered, history + [search]])
                else:
                    complete.append(history + [search])

    return complete

def decompose(startpath):
    options = decompose_analysis(startpath)
    if len(options) == 0:
        raise Exception("Solution not found...")

    print ("OPTIONS:")
    for option in options:
        print (f'{len(option):4} {option}')
    print()

    solution = options[0]
    print(solution)

    path = list(startpath)
    replacements = list('ABC')
    for i, entry in enumerate(solution):
        j = 0
        while j < len(path):
            if path[j:j+len(entry)] == entry:
                path[j:j+len(entry)] = replacements[i]
            j += 1
    results=[','.join(path)]

    for entry in solution:
        results.append(','.join([str(item) for sublist in entry for item in sublist]))

    return results


tracker = Tracker(program)
tracker.print()

intersections = tracker.find_intersections()

print(sum([x[0] * x[1] for x in intersections]))

path = tracker.walk()
path_results = decompose(path)

code[0] = 2
program = computer.Computer(code)

def mapit(command):
    response = []
    for line in command:
        response.append([ord(x) for x in line] + [10])

    return response

commands = mapit(path_results + ['n'])

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
