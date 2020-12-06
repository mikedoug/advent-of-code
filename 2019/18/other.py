data18 = open("input.txt").readlines()

KEYS = "abcdefghijklmnopqrstuvwxyz"

# Part 1 plan:
# ------------
# Do (letters +1) BFS's, finding the distances between each pair of keys 
# (and between the keys and the starting point), recording for each 
# destination key the doors and keys that you pass through on the way.
#
# Then do a breadth first memoized walk through the different ways to 
# collect keys - for each key keeping track of the distance taken to get
# there. At the end we will have a shortest distance to all keys.
# 
# It worked!

# Performs a BFS from a given source point to all reachable points of interest
def distances_from(source, data):
    sx,sy = source
    visited = set([(sx,sy)])
    queue = [(sx,sy, 0, "")]
    routeinfo = {}

    for (x, y, dist, route) in queue:
        contents = data[y][x]
        if contents not in ".@1234#" and dist>0:
            #print("  ",contents,"found at distance",dist,". Route:", route)
            routeinfo[contents] = (dist, route)
            route = route + contents
        visited.add((x,y))

        for d in [(1,0),(0,1),(-1,0),(0,-1)]:
            newx, newy = x+d[0], y+d[1]
            if data[newy][newx]!='#' and (newx,newy) not in visited:
                queue.append((newx,newy, dist+1, route))
    return routeinfo

# Find the route information for all points of interest in the map
def find_routeinfo(data):
    routeinfo = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            content = data[y][x]
            if content in KEYS+"@1234":
                routeinfo[content] = distances_from((x,y),data)
    return routeinfo

def aoc18_1(data):
    routeinfo = find_routeinfo(data)
    keys = frozenset(k for k in routeinfo.keys() if k in KEYS)

    # Our route information for each round is a dictionary mapping
    #  (current location, current keys) -> distance from start

    info = {('@',frozenset()):0}
    for _ in range(len(keys)):
        nextinfo = {}
        for item in info:
            curloc, curkeys, curdist = item[0], item[1], info[item]
            for newkey in keys:
                if newkey not in curkeys:
                    dist, route = routeinfo[curloc][newkey]
                    reachable = all((c in curkeys or c.lower() in curkeys) for c in route)

                    if reachable:
                        newdist = curdist + dist
                        newkeys = frozenset(curkeys | set((newkey,)))

                        if (newkey, newkeys) not in nextinfo or newdist < nextinfo[(newkey, newkeys)]:
                            nextinfo[(newkey,newkeys)] = newdist
        info = nextinfo

    print("There are",len(info),"final positions.")
    print("Best total distance:",min(info.values()))

# Part 2 plan:
# ------------
# Replace @ with 1234, and find the distances as before.
# Our state is now the positions of all 4 robots, but the general plan is the same - 
# only one robot moves at a time, and the keys are shared.

def update_for_part_2(data):
    data = [list(line) for line in data]
    for sy in range(len(data)):
        for sx in range(len(data[0])):
            if data[sy][sx] == '@':
                for (dx,dy) in [(0,0),(1,0),(0,1),(-1,0),(0,-1)]:
                    data[sy+dy][sx+dx]='#'
                data[sy-1][sx-1] = '1'
                data[sy-1][sx+1] = '2'
                data[sy+1][sx-1] = '3'
                data[sy+1][sx+1] = '4'
                return ["".join(line) for line in data]

def aoc18_2(data):
    data = update_for_part_2(data)

    routeinfo = find_routeinfo(data)
    keys = frozenset(k for k in routeinfo.keys() if k in KEYS)

    # Each state is now (position of all robots,keys collected) -> distance

    info = {(('1','2','3','4'),frozenset()):0}

    for _ in range(len(keys)):
        nextinfo = {}
        for item in info:
            curlocs, curkeys, curdist = item[0], item[1], info[item]

            for newkey in keys:
                if newkey not in curkeys:
                    for robot in range(4):
                        if newkey in routeinfo[curlocs[robot]]:
                            dist, route = routeinfo[curlocs[robot]][newkey]
                            reachable = all((c in curkeys or c.lower() in curkeys) for c in route)

                            if reachable:
                                newdist = curdist + dist
                                newkeys = frozenset(curkeys | set((newkey,)))
                                newlocs = list(curlocs)
                                newlocs[robot] = newkey
                                newlocs = tuple(newlocs)

                                if (newlocs, newkeys) not in nextinfo or newdist < nextinfo[(newlocs, newkeys)]:
                                    nextinfo[(newlocs,newkeys)] = newdist
        info = nextinfo

    print("There are",len(info),"final positions.")
    print("Best total distance:",min(info.values()))

print("Day 18")
print("------")

print("Part 1")
aoc18_1(data18)

print("\nPart 2")
aoc18_2(data18)