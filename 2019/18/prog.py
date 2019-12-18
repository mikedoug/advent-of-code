import copy
import hashlib

class Maze(object):
    key_symbols = 'abcdefghijklmnopqrstuvwxyz'
    door_symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    def __init__(self, maze, location=None, move_count=0, remaining_keys=None, lastmove=None, found_keys='', last_n_places=[]):
        self.maze = copy.deepcopy(maze)
        self.location = self.find('@') if location is None else location
        self.move_count = move_count
        self.remaining_keys = remaining_keys
        self.lastmove = lastmove
        self.found_keys = found_keys
        self.last_n_places = last_n_places

        if self.remaining_keys is None:
            self.remaining_keys = 0
            for c in Maze.key_symbols:
                if self.find(c) is not None:
                    self.remaining_keys += 1

    @classmethod
    def from_lines(clazz, lines):
        return Maze([list(line) for line in lines])

    @classmethod
    def from_maze(clazz, maze):
        return Maze(maze.maze, maze.location, maze.move_count, maze.remaining_keys, maze.lastmove, maze.found_keys, maze.last_n_places)

    def _is_equiv(self, other):
        return self.location == other.location and self.move_count == other.move_count \
            and self.remaining_keys == other.remaining_keys \
            and list(sorted(self.found_keys)) == list(sorted(other.found_keys))

    def hash(self):
        return hashlib.sha256(f'{self.location}{self.move_count}{self.remaining_keys}{sorted(self.found_keys)}'.encode()).digest()

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

    def available_moves(self):
        moves = []

        for offset in [(-1,0), (1,0), (0,-1), (0,1)]:
            offset_location = Maze.location_calc(self.location, offset)
            found_at_offset = self.at(offset_location)

            if found_at_offset == '#':
                continue

            if offset_location in self.last_n_places:
                continue

            if found_at_offset in Maze.door_symbols and found_at_offset.lower() not in self.found_keys:
                continue

            moves.append(offset)

        return moves

    def move(self, offset):
        self.maze[self.location[0]][self.location[1]] = '.'
        orig_location = self.location
        
        self.location = (self.location[0] + offset[0], self.location[1] + offset[1])
        original = self.maze[self.location[0]][self.location[1]]
        if original in Maze.key_symbols:
            self.remaining_keys -= 1
            self.found_keys += original
            self.last_n_places = []
            print(f' --- {self.move_count:10} {self.location} {self.remaining_keys} {self.found_keys}')
        elif original in Maze.door_symbols:
            self.last_n_places = []
        else:
            self.last_n_places += [orig_location]
            if len(self.last_n_places) > 20:
                self.last_n_places.pop(0)

        self.maze[self.location[0]][self.location[1]] = '@'
        self.move_count += 1
        self.lastmove = offset

    def print(self):
        for line in self.maze:
            print (''.join(line))
        print(f'{self.move_count:10} {self.location} {self.remaining_keys} {self.found_keys}')


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


lines = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        lines.append(line.rstrip())

maze = Maze.from_lines(lines)
maze.print()
run(maze)