import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

class Map(object):
    def __init__(self):
        self.map = {(0,0): 'S'}
        self.found = False

    def print(self):
        minx = min([x[0] for x in self.map.keys()])
        miny = min([x[1] for x in self.map.keys()])
        maxx = max([x[0] for x in self.map.keys()])
        maxy = max([x[1] for x in self.map.keys()])

        for x in range (minx, maxx+1):
            for y in range (miny, maxy+1):
                if (x,y) not in self.map:
                    print ('#', end='')
                else:
                    print(self.map[(x,y)], end='')

            print()

    def mapit(self, pos=(0,0), undo=None):
        while not self.found:
            options = list(filter(
                lambda x: x[1] not in self.map,
                [
                    (1,(pos[0]-1, pos[1]), 2),
                    (2,(pos[0]+1, pos[1]), 1),
                    (3,(pos[0], pos[1]-1), 4),
                    (4,(pos[0], pos[1]+1), 3)
                ]))

            if len(options) == 0:
                break

            dir = options[0]
            program.execute([dir[0]])
            output = program.get_outputs()[0]
            program.clear_outputs()

            if output == 0:  # Wall
                self.map[dir[1]] = '#'
            elif output == 2:
                self.map[dir[1]] = '*'
                self.oxygen_position = dir[1]
                self.mapit(dir[1], dir[2])
            else:
                self.map[dir[1]] = ' '
                self.mapit(dir[1], dir[2])

        if undo is not None:
            program.execute([undo])
            output = program.get_outputs()[0]
            program.clear_outputs()

            if output != 1:
                print(f"INVALID CODE {output}")
                exit(-1)

    def findpath(self, pos=(0,0), undo=None, acc=0, path=[]):
        options = list(filter(
            lambda x: x[1] in self.map and x[1] not in path and self.map[x[1]] != '#',
            [
                (1,(pos[0]-1, pos[1]), 2),
                (2,(pos[0]+1, pos[1]), 1),
                (3,(pos[0], pos[1]-1), 4),
                (4,(pos[0], pos[1]+1), 3)
            ]))

        lengths = []
        for dir in options:
            if self.map[dir[1]] == ' ':
                lengths.append(self.findpath(dir[1], dir[2], acc + 1, path + [pos]))
            elif self.map[dir[1]] == '*':
                lengths.append(acc + 1)
                
        return min(lengths) if len(lengths) > 0 else 9999999999999

    def timeO2(self, pos=None, acc=0, path=[]):
        if pos == None:
            pos = self.oxygen_position

        options = filter(
            lambda x: x[1] in self.map and x[1] not in path and self.map[x[1]] == ' ',
            [
                (1,(pos[0]-1, pos[1]), 2),
                (2,(pos[0]+1, pos[1]), 1),
                (3,(pos[0], pos[1]-1), 4),
                (4,(pos[0], pos[1]+1), 3)
            ])

        lengths = [self.timeO2(dir[1], acc + 1, path + [pos]) for dir in options]
        return max(lengths) if len(lengths) > 0 else acc


with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

program = computer.Computer(code)

map = Map()
map.mapit()
map.print()
print(map.findpath())
print(map.timeO2())

