import math
import numpy as np

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
                    # print(f'{point} {test} {dest} OBSCURED')
                    visible = False
                    break

        if visible:
            # print(f'                                     {point} {test} {dest} VISIBLE')
            visibleset.append(dest)

    return visibleset
    # print(f'{point} has {fieldset[point]} visible')

# get_angle from: https://stackoverflow.com/questions/13226038/calculating-angle-between-two-vectors-in-python
def get_angle(p0, p1=np.array([0,0]), p2=None):
    ''' compute angle (in degrees) for p0p1p2 corner
    Inputs:
        p0,p1,p2 - points in the form of [x,y]
    '''
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return np.degrees(angle) + 180.0


def destroy(fieldset, station):
    fieldset = list(fieldset)

    start = 1
    iteration = 1
    while len(fieldset) > 1:
        print(f'PASS: {iteration}')
        visiblelist = find_visible(fieldset, station)

        angles = {}
        for point in visiblelist:
            angle = get_angle( (station[0], station[1] + 50), station, point)
            angles[point] = angle if angle != 360 else 0.0

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