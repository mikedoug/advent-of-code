import math

def get_angles(fieldset, point, sort=False):
    angles = {}
    for dest in fieldset:
        if point == dest:
            continue

        angle = math.degrees(math.atan2(dest[1] - point[1], dest[0] - point[0])) + 90
        angle += 360 if angle < 0 else 0

        if angle not in angles:
            angles[angle] = []
        angles[angle].append(dest)

    if sort:
        for angle in angles:
            angles[angle] = list(sorted(angles[angle], key=lambda x: line_len(point, x)))

    return angles

def line_len(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return math.sqrt(x*x + y*y)


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

    # Step 1
    for point in fieldset.keys():
        fieldset[point] = len(get_angles(fieldset, point))

    (station, count) = max(fieldset.items(), key=lambda x: x[1])
    print(f'Step One: {station} length = {count}')
    print()

    # Step 2
    angles = get_angles(fieldset, station, sort=True)

    destroyed = []
    while len(angles) > 0:
        angle_keys = list(sorted(angles.keys()))
        for angle in angle_keys:
            point = angles[angle].pop(0)
            if len(angles[angle]) == 0:
                del angles[angle]
            destroyed.append((point, angle))
            # print(f'{len(destroyed):5}: {point} @ {angle}')

    print(f'200th destroyed asteroid: {destroyed[199]}')

main()