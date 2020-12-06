import copy
import hashlib

class Maze(object):
    key_symbols = 'abcdefghijklmnopqrstuvwxyz'
    door_symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    def __init__(self, maze):
        self.maze = copy.deepcopy(maze)
        self.__simplify()

    @classmethod
    def from_lines(clazz, lines):
        return Maze([list(line) for line in lines])

    def __count_surrounding_walls(self, rowi, coli):
        count=0
        for test in ((-1,0), (1,0), (0,-1), (0,1)):
            if self.maze[rowi+test[0]][coli+test[1]] == '#':
                count += 1
        return count

    def __simplify(self):
        modified = True
        while modified:
            modified = False

            for rowi, row in enumerate(self.maze):
                for coli, cell in enumerate(row):
                    if cell == '.' and self.__count_surrounding_walls(rowi, coli) == 3:
                        self.maze[rowi][coli] = '#'
                        modified = True

    def find(self, char):
        for rowi, row in enumerate(self.maze):
            try:
                columni = row.index(char)
                return (rowi, columni)
            except:
                pass

        return None

    @classmethod
    def location_calc(clazz, location, offset):
        return (location[0] + offset[0], location[1] + offset[1])

    def at(self, location):
        return self.maze[location[0]][location[1]]

    def set_at(self, location, symbol):
        self.maze[location[0]][location[1]] = symbol

    def available_moves(self, location):
        moves = []

        for offset in [(-1,0), (1,0), (0,-1), (0,1)]:
            offset_location = Maze.location_calc(location, offset)
            found_at_offset = self.at(offset_location)

            if found_at_offset == '#':
                continue

            # if found_at_offset in Maze.door_symbols and found_at_offset.lower() not in self.found_keys:
            #     continue

            moves.append(self.location_calc(location, offset))

        return moves

    def print(self):
        for line in self.maze:
            print (''.join(line).replace('.', ' ').replace('#', '\u2588'))


def run_old(maze):
    states = [maze]

    i = 0
    while len(states) > 0:
    # for _ in range(200):
        maze = states.pop(0)

        i += 1
        if i % 1000 == 0:
            print(f'States: {len(states)+1}')
            maze.print()

        for move in maze.available_moves():
            newmaze = Maze.from_maze(maze)
            newmaze.move(move)
            # newmaze.print()

            states.append(newmaze)

            if newmaze.remaining_keys == 0:
                newmaze.print()
                print(f"SOLUTION FOUND in {newmaze.move_count} steps")
                exit(0)

            # newmaze.print()
            # input()


def run(maze):
    next_round = {maze.hash: maze}

    i = 0
    while len(next_round) > 0:
        mazes = next_round.values()
        next_round = {}

        for maze in mazes:

            i += 1
            if i % 1000 == 0:
                print(f'States: {len(mazes)} {len(next_round)+1}')
                maze.print()

            for move in maze.available_moves():
                newmaze = Maze.from_maze(maze)
                newmaze.move(move)
                # newmaze.print()

                next_round[newmaze.hash()] = newmaze

                if newmaze.remaining_keys == 0:
                    newmaze.print()
                    print(f"SOLUTION FOUND in {newmaze.move_count} steps")
                    exit(0)

                # newmaze.print()
                # input()

class Walker(object):
    def __init__(self, maze, symbol=None):
        self.maze = maze
        if symbol is not None:
            self.location = maze.find(symbol)
        self.steps = 0
        self.symbol = symbol
        self.symbols = []  # [(symbol, distance), ...]
        self.done = False

    def clone(self):
        r = Walker(self.maze)
        r.location = self.location
        r.steps = self.steps
        r.symbol = self.symbol
        r.symbols = copy.copy(self.symbols)
        r.done = self.done
        return r

    def move(self):
        original_location = self.location
        moves = list(self.maze.available_moves(self.location))
        # print(f'Evaluating from {original_location} has moves: {moves}')

        if len(moves) == 0:
            self.done = True
            return [self]

        self.steps += 1
        response = [self] + [self.clone() for _ in range(len(moves) -1)]
        # print (response)
        for i, newlocation in enumerate(moves):
            response[i].location = newlocation
            symbol = self.maze.at(newlocation)

            if symbol is not None and symbol != '.':
                response[i].symbols.append((symbol, self.steps))
        
        self.maze.set_at(original_location, '#')

        return response

    def __repr__(self):
        return f'{self.steps} {self.location} {self.symbols}'

def walk_paths(walker):
    queue = [walker]

    paths = {}
    while len(queue) > 0:
        walker = queue.pop(0)
        walkers = walker.move()
        for walker in walkers:
            path = ''
            if walker.done:
                for symbol in walker.symbols:
                    if symbol[0] in Maze.key_symbols:
                        paths[symbol[0]] = (symbol[1], path)
                        path += symbol[0]
                    elif symbol[0] in Maze.door_symbols:
                        path += symbol[0]
            else:
                queue.append(walker)

    return paths
    

# [(a, 5), (b, 10), ...]

#{'@': {'a': (5, None), 'b': (15, 'DG')}


def map_paths(maze):
    paths = {}  # paths[src + dest] = (distance,'obSTAclEs')
    for symbol in f'@{Maze.key_symbols}':
        if maze.find(symbol) is None:
            continue
        usemaze = copy.deepcopy(maze)
        paths[symbol] = walk_paths(Walker(usemaze, symbol))   

    return paths

lines = []
with open("input2.txt", "r") as f:
    for line in f.readlines():
        lines.append(line.rstrip())

srcmaze = Maze.from_lines(lines)
srcmaze.print()

# run(maze)
paths = map_paths(srcmaze)
print (paths)

class PathWalker(object):
    def __init__(self, location, keys=None, distance=0):
        self.location = location
        self.keys = list(keys) if keys is not None else []
        self.distance = distance

    def clone(self):
        return PathWalker(self.location, self.keys, self.distance)

    def add(self, key, distance):
        self.location = key
        self.distance += distance
        self.keys.append(key.upper())

    def number_of_keys(self):
        return len(self.keys)

    def options(self, paths):
        options={}
        for destination in paths[self.location]:
            if destination.upper() in self.keys:
                continue
            if any(door.upper() not in self.keys for door in paths[self.location][destination][1]):
                continue
            options[destination] = paths[self.location][destination]

        return options

def runpaths(paths):
    queue = [PathWalker('@')]
    found_least = None
    total_keys = len(paths.keys()) - 1
    print(f"Total keys: {total_keys}")
    while len(queue) > 0:
        # print (f"Queue Length: {len(queue)}")
        lowest = None
        for i, walker in enumerate(queue):
            if lowest is None or walker.distance < queue[i].distance:
                lowest = i
        walker = queue.pop(i)

        print()
        print(f'Walking from {walker.location} so far {walker.distance} and {walker.keys}')
        for key,info in walker.options(paths).items():
            print(f' -- {key} {info}')
            newwalker = walker.clone()
            newwalker.add(key, info[0])

            if newwalker.number_of_keys() == total_keys:
                if found_least is None or newwalker.distance < found_least.distance:
                    found_least = newwalker
                    print(f"FOUND: {found_least.distance} {''.join(found_least.keys)}")
                else:
                    print(f"FOUND - SKIPPED: {newwalker.distance} {''.join(newwalker.keys)}")
            elif found_least is None or newwalker.distance < found_least.distance:
                print(f"{newwalker.distance} {len(newwalker.keys)}")
                queue.append(newwalker)
            else:
                print(f"{newwalker.distance} {len(newwalker.keys)} PRUNED")

    print(f"FOUND: {found_least.distance} {''.join(found_least.keys)}")

    # options = list(filter(lambda x: print(paths[location][x][1]), paths[location]))


runpaths(paths)