import math

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


def find_visible(fieldset, point):
    visibleset = list()
    for dest in fieldset:
        if point == dest:
            continue

        visible = True
        for test in fieldset:
            if test == point or test == dest:
                continue

            if orientation(point, test, dest) == 0:
                if onSegment(point, test, dest):
                    visible = False
                    break

        if visible:
            visibleset.append(dest)

    return visibleset


def destroy(fieldset, station):
    fieldset = list(fieldset)

    start = 1
    iteration = 1
    while len(fieldset) > 1:
        print(f'PASS: {iteration}')
        visiblelist = find_visible(fieldset, station)

        angles = {}
        for point in visiblelist:
            angle = math.degrees(math.atan2(point[1] - station[1], point[0] - station[0])) + 90
            angle = angle + 360 if angle < 0 else angle
            angles[point] = angle # if angle != 360 else 0.0

            fieldset.remove(point)

        for i,(point,angle) in enumerate(sorted(angles.items(), key=lambda x: x[1])):
            print(f'  {i+start:4}: {point} angle = {angle}')
        
        start += len(visiblelist)
        iteration += 1


def main():
    # Read the field
    field = []
    with open("input.txt", "r") as f:
        field = list(map(lambda x: x.rstrip(), f.readlines()))

    # Parse the field
    fieldset = {}
    for y in range(len(field)):
        row = field[y]
        for x in range(len(row)):
            if row[x] != '.':
                fieldset[(x,y)] = 0

    for point in fieldset:
        fieldset[point] = find_visible(fieldset, point)

    station, visiblelist = max(fieldset.items(), key=lambda x: len(x[1]))
    print(f'Total asteroids: {len(fieldset)}')
    print(f'Step One: {station} length = {len(visiblelist)}')
    print()

    destroy(fieldset, station)
main()