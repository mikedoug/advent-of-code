import sys

class WirePath(object):
    def __init__(self, pathstr):
        self.commands = list(map(lambda x: [x[0], int(x[1:])], pathstr.split(",")))
        print(pathstr)
        print(self.commands)

    def segments(self):
        segments = []
        loc = (0,0)
        for command in self.commands:
            if command[0] == 'R':
                newloc = (loc[0] + command[1], loc[1])
            elif command[0] == 'L':
                newloc = (loc[0] - command[1], loc[1])
            elif command[0] == 'U':
                newloc = (loc[0], loc[1] + command[1])
            elif command[0] == 'D':
                newloc = (loc[0], loc[1] - command[1])
            else:
                raise Exception(f'Invalid command {command}')
            
            segments.append((loc, newloc))
            loc = newloc
        
        return segments

    def stepsToPoint(self, point):
        distance = 0

        for segment in self.segments():
            if onSegment(segment[0], point, segment[1]):
                return distance + pointDistance(segment[0], point)
            else:
                distance += pointDistance(segment[0], segment[1])


def pointDistance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

# Intersection detection code from: https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

# Given three colinear points p, q, r, the function checks if 
# point q lies on line segment 'pr' 
def onSegment(p, q, r):
    return q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])
  
# To find orientation of ordered triplet (p, q, r). 
# The function returns following values 
# 0 --> p, q and r are colinear 
# 1 --> Clockwise 
# 2 --> Counterclockwise 
def orientation(p, q, r):
    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/ 
    # for details of below formula. 
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
  
    if val == 0:
        return 0  # colinear 
  
    return 1 if (val > 0) else 2 # clock or counterclock wise 
  
# The main function that returns True if line segment 'p1q1' 
# and 'p2q2' intersect. 
def doIntersect(p1, q1, p2, q2): 
    # Find the four orientations needed for general and special cases 
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
  
    # General case 
    if o1 != o2 and o3 != o4:
        return True
  
    # Special Cases 
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1 
    if o1 == 0 and onSegment(p1, p2, q1):
        return True
  
    # p1, q1 and q2 are colinear and q2 lies on segment p1q1 
    if o2 == 0 and onSegment(p1, q2, q1):
        return True
  
    # p2, q2 and p1 are colinear and p1 lies on segment p2q2 
    if o3 == 0 and onSegment(p2, p1, q2):
        return True
  
    # p2, q2 and q1 are colinear and q1 lies on segment p2q2 
    if o4 == 0 and onSegment(p2, q1, q2):
        return True
  
    return False # Doesn't fall in any of the above cases 


def findAllOverlappingPoints(p1, q1, p2, q2):
    points = list()
    for x in range(p1[0], q1[0] + 1):
        for y in range(p1[1], q1[1] + 1):
            point = (x, y)
            if onSegment(p2, point, q2):
                points.append(point)
    return points

# Intersection code from: https://www.geeksforgeeks.org/program-for-point-of-intersection-of-two-lines/

def lineIntersection(A, B, C, D):
    # Line AB represented as a1x + b1y = c1 
    a1 = B[1] - A[1]
    b1 = A[0] - B[0]
    c1 = a1*(A[0]) + b1*(A[1])
  
    # Line CD represented as a2x + b2y = c2 
    a2 = D[1] - C[1]
    b2 = C[0] - D[0]
    c2 = a2*(C[0])+ b2*(C[1])
  
    determinant = a1*b2 - a2*b1
  
    if determinant == 0:
        return findAllOverlappingPoints(A,B,C,D)

    x = (b2*c1 - b1*c2)/determinant
    y = (a1*c2 - a2*c1)/determinant
    return [(int(x), int(y))]

wire1 = WirePath(sys.stdin.readline().rstrip())
wire2 = WirePath(sys.stdin.readline().rstrip())

print (wire1.segments())

points = []
for w1seg in wire1.segments():
    for w2seg in wire2.segments():
        if doIntersect(w1seg[0], w1seg[1], w2seg[0], w2seg[1]):
            newpoints = lineIntersection(w1seg[0], w1seg[1], w2seg[0], w2seg[1])
            print(f'Intersection: {w1seg} {w2seg} = {newpoints}')
            points += newpoints

def manhattanDistance(point):
    return abs(point[0]) + abs(point[1])

print(points)
points = filter(lambda x: x != (0,0), points)

closest = None
steps = None
for point in points:
    if closest is None or manhattanDistance(point) < manhattanDistance(closest):
        closest = point

    newsteps = wire1.stepsToPoint(point) + wire2.stepsToPoint(point)
    if steps is None or newsteps < steps:
        steps = newsteps
    


print(f'Closest point {closest} has distance {manhattanDistance(closest)}')
print(f'Fastest Path Summation is {steps}')

