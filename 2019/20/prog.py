import copy
import msvcrt
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
    def __init__(self, lines, enable_layers=False):
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
            dest = nextlocation.destination
            self.jump_path.append((self.layer, nextlocation.tag, nextlocation.is_outer))

            if self.enable_layers:
                if nextlocation.is_outer:
                    self.layer -= 1
                else:
                    self.layer += 1

            # print (f"You used portal {nextlocation.tag}")
        elif isinstance(nextlocation, Exit):
            self.win = True
        elif nextlocation != '#':
            dest = moveto
            self.jump_path.append((self.layer, dest))

        if dest is not None:
            self.moves += 1
            self.maze[self.at[0]][self.at[1]] = '.'
            self.at = dest
            self.maze[self.at[0]][self.at[1]] = 'o'

    def reject_location(self, location, entity):
        if isinstance(entity, Jump):
            tag_path = list(map(lambda x: x, filter(lambda x: isinstance(x[1], str), self.jump_path)))
            if len(tag_path) > 0 and tag_path[-1][1] == entity.tag:
                return True

            # print (tag_path)
            # for i in range(len(tag_path)-1):
            #     if tag_path[i][1] == tag_path[-1][1] and tag_path[i+1][1] == entity.tag and \
            #         tag_path[i][2] == tag_path[-1][2] and tag_path[i+1][2] == entity.is_outer:
            #         print("Rejecting:")
            #         print (tag_path)
            #         print (entity.tag, entity.is_outer)
            #         print()
            #         return True

            return (self.layer, entity.tag) in self.jump_path

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

        x = msvcrt.getch()
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


# def count_surrounding_walls(maze, rowi, coli):
#     count=0
#     for test in ((-1,0), (1,0), (0,-1), (0,1)):
#         if maze[rowi+test[0]][coli+test[1]] == '#':
#             count += 1
#     return count

# def simplify(lines):
#     maze = []
#     for line in lines:
#         maze.append(list(line))    

#     while True:
#         modified = False

#         for rowi, row in enumerate(maze):
#             for coli, cell in enumerate(row):
#                 if cell == '.' and count_surrounding_walls(maze, rowi, coli) == 3:
#                     maze[rowi][coli] = '#'
#                     modified = True

#         if not modified:
#             for row in maze:
#                 print (''.join([str(x) for x in row]))            
#             exit(0)


with open("input2.txt", "r") as f:
    lines = [x.rstrip("\n") for x in f.readlines()]

maze = Maze(lines, True)
maze.print()
solve(maze)
# manual(maze)

# with open("input.txt", "r") as f:
#     lines = [x.rstrip("\r\n") for x in f.readlines()]

# simplify(lines)
# exit(0)
