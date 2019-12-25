import itertools
import copy
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import computer # pylint: disable=import-error

class Map(object):
    def __init__(self, layers, iterations = 0):
        self.max_y = len(layers[0])
        self.max_x = len(layers[0][0])
        self.layers = layers
        self.iterations = iterations

    def empty_layer(self):
        return ['.' * self.max_x for _ in range(self.max_y)]

    def print(self, layer=0):
        # print (self.layers)
        layer += (len(self.layers) // 2)
        print(f"Layer {layer - len(self.layers) // 2} after {self.iterations} minute(s)")
        print('\n'.join(self.layers[layer]))
        print()

    def tick(self):
        layer = len(self.layers) // 2
        newlines = []
        for iy in range(self.max_y):
            line = ''
            for ix in range(self.max_x):
                count = 1 if iy > 0 and self.layers[layer][iy-1][ix] == '#' else 0
                count += 1 if iy < self.max_y - 1 and self.layers[layer][iy+1][ix] == '#' else 0
                count += 1 if ix > 0 and self.layers[layer][iy][ix-1] == '#' else 0
                count += 1 if ix < self.max_x - 1 and self.layers[layer][iy][ix+1] == '#' else 0

                if self.layers[layer][iy][ix] == '#':
                    line += '#' if count == 1 else '.'
                else:
                    line += '#' if count == 1 or count == 2 else '.'
                # line += f'{count}'

            newlines.append(line)

        return Map([newlines], self.iterations + 1)

    def multi_tick(self):
        templayers = [self.empty_layer()] + self.layers + [self.empty_layer()]

        newlayers = []
        for layer in range(len(templayers)):
            newlines = []
            for iy in range(self.max_y):
                line = ''
                for ix in range(self.max_x):
                    # print (f'{layer} ({i}, {j})')

                    if ix == 2 and iy == 2:
                        line += '?'
                    else:
                        count = 0
                        if layer < len(templayers) -1:
                            count += 1 if ix == 0 and templayers[layer+1][2][1] == '#' else 0
                            count += 1 if ix == self.max_x - 1 and templayers[layer+1][2][3] == '#' else 0
                            count += 1 if iy == 0 and templayers[layer+1][1][2] == '#' else 0
                            count += 1 if iy == self.max_y - 1 and templayers[layer+1][3][2] == '#' else 0
                        
                        if layer > 0:
                            if ix == 2:
                                if iy == 1:
                                    for z in range(self.max_y):
                                        count += 1 if templayers[layer-1][0][z] == '#' else 0
                                if iy == 3:
                                    for z in range(self.max_y):
                                        count += 1 if templayers[layer-1][4][z] == '#' else 0

                            if iy == 2:
                                if ix == 1:
                                    for z in range(self.max_y):
                                        count += 1 if templayers[layer-1][z][0] == '#' else 0
                                if ix == 3:
                                    for z in range(self.max_y):
                                        count += 1 if templayers[layer-1][z][4] == '#' else 0

                        count += 1 if iy > 0 and templayers[layer][iy-1][ix] == '#' else 0
                        count += 1 if iy < self.max_y - 1 and templayers[layer][iy+1][ix] == '#' else 0
                        count += 1 if ix > 0 and templayers[layer][iy][ix-1] == '#' else 0
                        count += 1 if ix < self.max_x - 1 and templayers[layer][iy][ix+1] == '#' else 0

                        # print (count)

                        if templayers[layer][iy][ix] == '#':
                            line += '#' if count == 1 else '.'
                        else:
                            line += '#' if count == 1 or count == 2 else '.'

                newlines.append(line)
            
            newlayers.append(newlines)

        return Map(newlayers, self.iterations + 1)

    def biodiversity(self, layer=0):
        layer += (len(self.layers) // 2)

        value = 0
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.layers[layer][y][x] == '#':
                    value += pow(2, y*5 + x)
        return value

    def count_bugs(self):
        count = 0
        for layer in self.layers:
            for y in range(self.max_y):
                for x in range(self.max_x):
                    if layer[y][x] == '#':
                        count += 1

        return count

with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f.readlines()]

# Step 1
m = Map([lines])
m.print()
seen = set([m.biodiversity()])
while True:
    m = m.tick()
    bd = m.biodiversity()
    if bd in seen:
        m.print()
        print(f'Biodiversity: {bd}')
        print(f'Bugs: {m.count_bugs()}')
        break
    seen.add(bd)    

m = Map([lines])
m.print()
for iteration in range(200):
    m = m.multi_tick()

# for layer in range(-10,11):
    # m.print(layer)
print(f'Bugs: {m.count_bugs()}')
print(f'Layers: {len(m.layers)}')
