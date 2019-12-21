import copy
# import msvcrt
import sys

class Portal(object):
    def __init__(self, tag):
        self.points = []
        self.tag = tag
        self.outer = None

    def add(self, point, is_outer):
        if len(self.points) == 2:
            raise Exception(f"Too many points for portal {self.tag} {point}")

        self.points.append(point)

        if is_outer:
            self.outer = point

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return self.__str__()

class Jump(object):
    def __init__(self, destination, tag, is_outer=False):
        self.destination = destination
        self.tag = tag
        self.is_outer = is_outer

    def __str__(self):
        return '!'

    def __repr__(self):
        return f'!{self.tag}!'

class Entry(object):
    pass

class Exit(object):
    def __str__(self):
        return '$'
    pass

class Maze(object):
    def __init__(self, lines, enable_layers=False, enable_jumping=True):
        self.maze = []

        for line in lines:
            self.maze.append(list(line))

        self.enable_layers = enable_layers
        self.layer = 0

        self.print()
        print(len(self.maze[0]))
        print(len(self.maze[1]))
        self.__init_portals()

        self.win = False
        self.moves = 0

        self.enable_jumping = enable_jumping
        self.found_jump = None

        self.at = tuple(self.entry)
        self.jump_path = [(0,self.at)]
        self.maze[self.at[0]][self.at[1]] = 'o'

        self.__simplify()

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

    def __init_portals(self):
        self.portals = {}

        for col in range(len(self.maze[0])):
            if self.maze[0][col] != ' ':

                tag = self.maze[0][col] + self.maze[1][col]
                self.__add_portal(tag, (1,col,2,col), True)

            if self.maze[-2][col] != ' ':
                tag = self.maze[-2][col] + self.maze[-1][col]
                self.__add_portal(tag, (len(self.maze) - 2, col, len(self.maze) - 3, col), True)

        for row in range(len(self.maze)):
            if self.maze[row][0] != ' ':
                tag = self.maze[row][0] + self.maze[row][1]
                self.__add_portal(tag, (row, 1, row, 2), True)
            if self.maze[row][-2] != ' ':
                tag = self.maze[row][-2] + self.maze[row][-1]
                self.__add_portal(tag, (row, len(self.maze[0]) - 2, row, len(self.maze[0]) - 3), True)

        # Find the center
        center_row = center_bottom_row = center_top_row = len(self.maze) // 2
        center_col = center_right_col = center_left_col = len(self.maze[0]) // 2

        while self.maze[center_top_row-1][center_col] not in ".#":
            center_top_row -= 1
        while self.maze[center_bottom_row+1][center_col] not in ".#":
            center_bottom_row += 1
        while self.maze[center_row][center_left_col-1] not in ".#":
            center_left_col -= 1
        while self.maze[center_row][center_right_col+1] not in ".#":
            center_right_col += 1

        for col in range(center_left_col, center_right_col + 1):
            if self.maze[center_top_row][col] != ' ' and self.maze[center_top_row+1][col] != ' ':
                tag = self.maze[center_top_row][col] + self.maze[center_top_row+1][col]
                self.__add_portal(tag, (center_top_row, col, center_top_row-1, col))

            if self.maze[center_bottom_row-1][col] != ' ' and self.maze[center_bottom_row][col] != ' ':
                tag = self.maze[center_bottom_row-1][col] + self.maze[center_bottom_row][col]
                self.__add_portal(tag, (center_bottom_row, col, center_bottom_row+1, col))

        for row in range(center_top_row, center_bottom_row+1):
            if self.maze[row][center_left_col] != ' ' and self.maze[row][center_left_col+1] != ' ':
                tag = self.maze[row][center_left_col] + self.maze[row][center_left_col+1]
                self.__add_portal(tag, (row, center_left_col, row, center_left_col-1))
            if self.maze[row][center_right_col-1] != ' ' and self.maze[row][center_right_col] != ' ':
                tag = self.maze[row][center_right_col-1] + self.maze[row][center_right_col]
                self.__add_portal(tag, (row, center_right_col, row, center_right_col+1))

        for tag in filter(lambda x: x != 'AA' and x != 'ZZ', self.portals):
            portal = self.portals[tag]
            if len(portal.points) != 2:
                raise Exception("Invalid portal")

            ptA = portal.points[0]
            ptA_is_outer = ptA == portal.outer
            ptB = portal.points[1]
            ptB_is_outer = ptB == portal.outer

            print (ptA, ptA_is_outer, ptB, ptB_is_outer)


            self.maze[ptA[0]][ptA[1]] = Jump((ptB[2], ptB[3]), tag, ptA_is_outer)
            self.maze[ptB[0]][ptB[1]] = Jump((ptA[2], ptA[3]), tag, ptB_is_outer)


        self.entry = self.portals['AA'].points[0][2:]
        self.exit = self.portals['ZZ'].points[0][0:2]

        self.maze[self.entry[0]][self.entry[1]] = '#'
        self.maze[self.exit[0]][self.exit[1]] = Exit()

    def print(self):
        for row in self.maze:
            print (''.join([str(x) if x != '.' else ' ' for x in row]))

    def move(self, offset):
        moveto = (self.at[0] + offset[0], self.at[1] + offset[1])
        nextlocation = self.maze[moveto[0]][moveto[1]]

        dest = None
        if isinstance(nextlocation, Jump):
            if self.enable_jumping:
                dest = nextlocation.destination
                self.jump_path.append((self.layer, nextlocation.tag, nextlocation.is_outer))

                if self.enable_layers:
                    if nextlocation.is_outer:
                        self.layer -= 1
                    else:
                        self.layer += 1
            else:
                self.found_jump = nextlocation
                self.moves += 1

            # print (f"You used portal {nextlocation.tag}")
        elif isinstance(nextlocation, Exit):
            self.win = True
        elif nextlocation != '#' and not isinstance(nextlocation, Entry):
            dest = moveto
            self.jump_path.append((self.layer, dest))

        if dest is not None:
            self.moves += 1
            self.maze[self.at[0]][self.at[1]] = '.'
            self.at = dest
            self.maze[self.at[0]][self.at[1]] = 'o'

    def start_at(self, dest):
        self.maze[self.at[0]][self.at[1]] = '.'
        self.at = dest
        self.maze[self.at[0]][self.at[1]] = 'o'
        self.jump_path = [(0,self.at)]

    def reject_location(self, location, entity):
        if isinstance(entity, Jump):

            # If jumping is not enabled, we don't have to worry about rejecting Jump points
            # if not self.enable_jumping:
            #     return False

            tag_path = list(map(lambda x: x, filter(lambda x: isinstance(x[1], str), self.jump_path)))

            if len(tag_path) > 0 and tag_path[-1][1] == entity.tag:
                return True
            return (self.layer, entity.tag) in self.jump_path

            # print (tag_path)
            # for i in range(len(tag_path)-1):
            #     if tag_path[i][1] == tag_path[-1][1] and tag_path[i+1][1] == entity.tag and \
            #         tag_path[i][2] == tag_path[-1][2] and tag_path[i+1][2] == entity.is_outer:
            #         print("Rejecting:")
            #         print (tag_path)
            #         print (entity.tag, entity.is_outer)
            #         print()
            #         return True

        return (self.layer, location) in self.jump_path

    def available_moves(self):
        moves = []
        for test in ((-1,0), (1,0), (0,-1), (0,1)):
            test_location = (self.at[0] + test[0], self.at[1] + test[1])
            test_point = self.maze[self.at[0] + test[0]][self.at[1] + test[1]]
            if self.reject_location(test_location, test_point):
                continue 
            if self.enable_layers and isinstance(test_point, Jump) and self.layer == 0 and test_point.is_outer:
                continue
            if self.enable_layers and isinstance(test_point, Exit) and self.layer != 0:
                continue
            if test_point == '.' or isinstance(test_point, Jump) or isinstance(test_point, Exit):
                moves.append(test)
        return moves

    # Format of point: x,y,a,b  x,y = location of jump pad; a,b = point on map the pad connects to
    def __add_portal(self, tag, point, is_outer=False):
        if tag not in self.portals:
            self.portals[tag] = Portal(tag)

        self.portals[tag].add(point, is_outer)

def map_paths(srcmaze):
    srcmaze.enable_layers = False
    srcmaze.enable_jumping = False

    results = {}  # {[start, inner bool]}{[end, inner bool]} = distance
    for tag, portal in srcmaze.portals.items():
        if tag == 'ZZ':
            continue

        for outer, point in enumerate(portal.points):
            outer = 'outer' if outer == 0 else 'inner'

            start_point = (point[2], point[3])
            # print (f'{tag} {outer} {start_point}')

            walkmaze = copy.deepcopy(srcmaze)
            walkmaze.start_at(start_point)

            queue = [walkmaze]
            src_key = (tag, outer)

            while len(queue) > 0:
                walkmaze = queue.pop(0)

                moves = walkmaze.available_moves()
                dest_key = None
                distance = None
                if len(moves) == 1:
                    # walkmaze.print()
                    # print (walkmaze.jump_path)
                    # print (moves[0])
                    walkmaze.move(moves[0])
                    # print (walkmaze.jump_path)
                    # print()
                    if walkmaze.win:
                        dest_key = ('ZZ', 'outer')
                        distance = walkmaze.moves
                    elif walkmaze.found_jump is not None:
                        dest_key = (walkmaze.found_jump.tag, 'outer' if walkmaze.found_jump.is_outer else 'inner')
                        distance = walkmaze.moves
                    else:
                        queue.append(walkmaze)
                else:
                    for move in moves:
                        newmaze = copy.deepcopy(walkmaze)
                        newmaze.move(move)
                        if newmaze.win:
                            dest_key = ('ZZ', 'outer')
                            distance = newmaze.moves
                        elif newmaze.found_jump is not None:
                            dest_key = (newmaze.found_jump.tag, 'outer' if newmaze.found_jump.is_outer else 'inner')
                            distance = newmaze.moves
                        else:
                            queue.append(newmaze)

                if dest_key is not None and distance > 1:
                    results[src_key] = results[src_key] if src_key in results else {}
                    results[src_key][dest_key] = distance
                    # print (f"--- {src_key} -> {dest_key} = {distance}")

    return results


def solve(maze):
    queue = [maze]

    i = 0
    while len(queue) > 0:
        i += 1
        if i % 1000 == 0:
            print(len(queue))
        maze = queue.pop(0)

        moves = maze.available_moves()
        if len(moves) == 1:
            # maze.print()
            # print (maze.jump_path)
            # print (moves[0])
            maze.move(moves[0])
            # print (maze.jump_path)
            # print()
            if maze.win:
                maze.print()
                print(f'You win in {maze.moves} steps {maze.jump_path}')
                return
            queue.append(maze)
        else:
            for move in moves:
                newmaze = copy.deepcopy(maze)
                newmaze.move(move)
                if newmaze.win:
                    maze.print()
                    print(f'You win in {maze.moves} steps {maze.jump_path}')
                    return
                queue.append(newmaze)

# Manually drive the maze
def manual(maze):
    while True:
        maze.print()
        print(maze.layer)
        print(maze.jump_path)
        print(maze.available_moves())

        # x = msvcrt.getch()
        x = 'q'
        if x == b'q':
            exit(0)
        if x == b'w':
            maze.move((-1, 0))
        elif x == b'a':
            maze.move((0, -1))
        elif x == b's':
            maze.move((1, 0))
        elif x == b'd':
            maze.move((0, 1))
        if maze.win:
            maze.print()
            print(f"You win! in {maze.moves} moves")
            exit(0)

class PathWalker(object):
    def __init__(self, paths, enable_layers):
        self.paths = paths
        self.location = ('AA', 'outer')
        self.distance = 0
        self.layer = 0
        self.enable_layers = enable_layers
        self.moves = 0
        self.history = []

    def nextSteps(self):
        destinations = self.paths[self.location]

        results = []
        for destination in destinations:
            layer_distance = self.paths[self.location][destination]

            if self.enable_layers:
                if self.layer == 0 and destination[0] != 'ZZ' and destination[1] == 'outer':
                    continue
                if self.layer + layer_distance[0] != -1 and destination[0] == 'ZZ':
                    continue

            newpw = copy.deepcopy(self)
            newpw.moveTo(destination)
            results.append(newpw)
        return results

    def moveTo(self, destination):
        layer_distance = self.paths[self.location][destination]
        self.layer += layer_distance[0]
        self.distance += layer_distance[1]

        jumpto = (destination[0], 'outer' if destination[1] == 'inner' else 'inner')
        self.location = jumpto

        self.moves += 1

        self.history.append((destination))

    def __str__(self):
        return f'PathWalker: {self.layer:5} {self.moves:5} {self.distance:10} {self.location}'

def walk_paths(paths, enable_layers):
    queue = [PathWalker(paths, enable_layers)]

    exit_found = None
    while len(queue) > 0:
        print (f'\nQueue Length: {len(queue)}')

        # Work the current walker that has the shortest distance
        which = sorted(enumerate(queue), key=lambda x: x[1].distance).pop(0)
        walker = queue.pop(which[0])
        print (walker.distance, walker.location, "-->", walker.paths[walker.location])
        print(walker.layer, walker.history)

        for n in walker.nextSteps():
            print(f' === {n.history}')
            print(f'     {n}')
            if n.location == ('ZZ', 'inner'):
                if enable_layers and n.layer != -1:
                    continue
                if exit_found is None or n.distance < exit_found.distance:
                    print("FOUND EXIT:", n)
                    exit_found = n
            elif enable_layers and n.layer < 0:
                # We can't follow a path into negative space
                continue

            if exit_found is None or n.distance < exit_found.distance:
                queue.append(n)

    print("Exit:", exit_found)
    # links = []
    # for i in range(len(exit_found.history)-1):
    #     links.append(f'{exit_found.history[i]} => {exit_found.history[i+1]}')
    # for link in sorted(links):
    #     print (link)

def optimize_paths(paths, step=1):
    for src, dests in paths.items():
        print (src, dests)

    print()

    newpaths = {}
    changed = False

    for src, dests in paths.items():
        print (src, dests)

        if step == 2 and len(dests) > 1:
            # For step 2 we cannot compress anything that has multiple destinations
            print(f'CANNOT COMPRESS MULTI STEP {src} => {dests}')
            newpaths[src] = paths[src]
            continue

        for dest,layer_dist in dests.items():
            follow_dest = (dest[0], 'inner' if dest[1] != 'inner' else 'outer')
            print(f'TRYING TO COMPRESS {src} ==> {dest}/{follow_dest}')
            if src not in newpaths:
                newpaths[src] = {}

            if dest[0] != 'ZZ' and len(paths[follow_dest]) == 1:
                for newdest, newlayer_dist in paths[follow_dest].items():
                    pass
                print(f'  -- Found {paths[follow_dest]}')
                print(f'      {newdest} {newlayer_dist}')
                print (newdest, newlayer_dist)
                newpaths[src][newdest] = (layer_dist[0] + newlayer_dist[0], layer_dist[1] + newlayer_dist[1])
                changed = True
                print(f'        COMPRESSED {src} ==> {dest}/{follow_dest} to {newdest} {newpaths[src][newdest]}')
            else:
                print(f'No Compresion found')
                newpaths[src][dest] = layer_dist

            print()
            print()

    
    if changed:
        return optimize_paths(newpaths, step)
    return paths


def paths_add_layers(paths):
    newpaths = {}
    for src, dests in paths.items():
        print (src, dests)
        for dest,dist in dests.items():
            if src not in newpaths:
                newpaths[src] = {}
            layer_diff = -1 if dest[1] == 'outer' else 1
            newpaths[src][dest] = (layer_diff, dist)

    return newpaths


with open("input2.txt", "r") as f:
    lines = [x.rstrip("\n") for x in f.readlines()]

# maze = Maze(lines)
# maze.print()
# solve(maze)
# manual(maze)


maze = Maze(lines, True)
maze.print()
print('Mapping paths...')
paths = map_paths(maze)
# paths = {('RX', 'outer'): {('ZZ', 'outer'): 10, ('WS', 'inner'): 89}, ('RX', 'inner'): {('WJ', 'outer'): 81}, ('AN', 'outer'): {('GP', 'outer'): 5, ('KV', 'inner'): 59, ('VN', 'inner'): 61}, ('AN', 'inner'): {('QD', 'outer'): 81}, ('GP', 'outer'): {('AN', 'outer'): 5, ('KV', 'inner'): 57, ('VN', 'inner'): 59}, ('GP', 'inner'): {('LS', 'outer'): 77}, ('YV', 'outer'): {('FM', 'inner'): 73}, ('YV', 'inner'): {('HY', 'outer'): 77}, ('JY', 'outer'): {('QD', 'inner'): 85}, ('JY', 'inner'): {('AO', 'outer'): 73}, ('KV', 'outer'): {('TT', 'inner'): 87}, ('KV', 'inner'): {('VN', 'inner'): 5, ('GP', 'outer'): 57, ('AN', 'outer'): 59}, ('LF', 'outer'): {('BU', 'inner'): 71}, ('LF', 'inner'): {('JM', 'outer'): 83}, ('AO', 'outer'): {('JY', 'inner'): 73}, ('AO', 'inner'): {('UB', 'outer'): 65}, ('AA', 'outer'): {('AO', 'outer'): 5, ('JY', 'inner'): 75}, ('QD', 'outer'): {('AN', 'inner'): 81}, ('QD', 'inner'): {('JY', 'outer'): 85}, ('PW', 'outer'): {('QE', 'inner'): 67}, ('PW', 'inner'): {('FM', 'outer'): 45}, ('LD', 'outer'): {('YD', 'inner'): 55}, ('LD', 'inner'): {('QE', 'outer'): 79}, ('YD', 'outer'): {('IV', 'inner'): 71}, ('YD', 'inner'): {('LD', 'outer'): 55}, ('HY', 'outer'): {('YV', 'inner'): 77}, ('HY', 'inner'): {('WS', 'outer'): 79}, ('UO', 'outer'): {('LS', 'inner'): 49}, ('UO', 'inner'): {('IV', 'outer'): 47}, ('VN', 'outer'): {('TG', 'inner'): 49}, ('VN', 'inner'): {('KV', 'inner'): 5, ('GP', 'outer'): 59, ('AN', 'outer'): 61}, ('BU', 'outer'): {('WJ', 'inner'): 43}, ('BU', 'inner'): {('LF', 'outer'): 71}, ('IV', 'outer'): {('UO', 'inner'): 47}, ('IV', 'inner'): {('YD', 'outer'): 71}, ('TG', 'outer'): {('JM', 'inner'): 53}, ('TG', 'inner'): {('VN', 'outer'): 49}, ('QE', 'outer'): {('LD', 'inner'): 79}, ('QE', 'inner'): {('PW', 'outer'): 67}, ('UB', 'outer'): {('AO', 'inner'): 65}, ('UB', 'inner'): {('BM', 'outer'): 95}, ('JM', 'outer'): {('LF', 'inner'): 83}, ('JM', 'inner'): {('TG', 'outer'): 53}, ('WS', 'outer'): {('HY', 'inner'): 79}, ('WS', 'inner'): {('ZZ', 'outer'): 81, ('RX', 'outer'): 89}, ('BM', 'outer'): {('UB', 'inner'): 95}, ('BM', 'inner'): {('TT', 'outer'): 79}, ('FM', 'outer'): {('PW', 'inner'): 45}, ('FM', 'inner'): {('YV', 'outer'): 73}, ('TT', 'outer'): {('BM', 'inner'): 79}, ('TT', 'inner'): {('KV', 'outer'): 87}, ('WJ', 'outer'): {('RX', 'inner'): 81}, ('WJ', 'inner'): {('BU', 'outer'): 43}, ('LS', 'outer'): {('GP', 'inner'): 77}, ('LS', 'inner'): {('UO', 'outer'): 49}}
paths = paths_add_layers(paths)
paths = optimize_paths(paths, 2)
print("FINISHED")
for src, dests in paths.items():
    print (src, dests)

# print (paths)
print()
walk_paths(paths, True)

# with open("input.txt", "r") as f:
#     lines = [x.rstrip("\r\n") for x in f.readlines()]

# simplify(lines)
# exit(0)
