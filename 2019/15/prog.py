import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

class Map(object):
    def __init__(self, program):
        self.map = {(0,0): 'S'}
        self.program = program

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

    @classmethod
    def _options_from_pos(clazz, pos):
        return [
            (1,(pos[0]-1, pos[1]), 2),
            (2,(pos[0]+1, pos[1]), 1),
            (3,(pos[0], pos[1]-1), 4),
            (4,(pos[0], pos[1]+1), 3)
        ]

    def mapit(self, pos=(0,0), undo=None):
        while True:
            options = list(filter(lambda x: x[1] not in self.map, Map._options_from_pos(pos)))

            if len(options) == 0:
                break

            move_code, new_pos, undo_code = options[0]
            self.program.execute([move_code])
            output = self.program.get_outputs()[0]
            self.program.clear_outputs()

            if output == 0:  # Wall
                self.map[new_pos] = '#'
            elif output == 1:
                self.map[new_pos] = ' '
                self.mapit(new_pos, undo_code)
            elif output == 2:
                self.map[new_pos] = '*'
                self.oxygen_position = new_pos
                self.mapit(new_pos, undo_code)
            else:
                raise Exception(f'Invalid response from program {output}')

        if undo is not None:
            self.program.execute([undo])
            output = self.program.pop_output()

            if output != 1:
                print(f"INVALID CODE ON UNDO{output}")
                exit(-1)

    def findpath(self, pos=(0,0), undo=None, acc=0, path=[]):
        options = list(filter(
            lambda x: x[1] in self.map and x[1] not in path and self.map[x[1]] != '#',
            Map._options_from_pos(pos)
        ))

        lengths = []
        for _, new_pos, undo_code in options:
            if self.map[new_pos] == ' ':
                lengths.append(self.findpath(new_pos, undo_code, acc + 1, path + [pos]))
            elif self.map[new_pos] == '*':
                lengths.append(acc + 1)
                
        return min(lengths) if len(lengths) > 0 else 9999999999999

    def timeO2(self, pos=None, acc=0, path=[]):
        if pos == None:
            pos = self.oxygen_position

        options = filter(lambda x: x[1] in self.map and x[1] not in path and self.map[x[1]] == ' ', Map._options_from_pos(pos))

        lengths = [self.timeO2(dir[1], acc + 1, path + [pos]) for dir in options]
        return max(lengths) if len(lengths) > 0 else acc


with open("input.txt", "r") as f:
    code = [int(x) for x in f.readline().rstrip().split(',')]

map = Map(computer.Computer(code))
map.mapit()
map.print()
print(map.findpath())
print(map.timeO2())

