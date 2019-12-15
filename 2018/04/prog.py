import re

with open("input.txt", "r") as f:
    lines = sorted([x.strip() for x in f.readlines()])

r = re.compile(r'.\d{4}-\d\d-\d\d (?P<hour>\d\d):(?P<minute>\d\d). (?P<what>Guard #(?P<id>\d+) begins shift|falls asleep|wakes up)')

guards = {}
current_guard = None
current_asleep = None
for line in lines:
    print(line)
    match = r.match(line)
    hour, minute, what, guard = int(match['hour']), int(match['minute']), match['what'], match['id']
    if hour == 23:
        hour = 0
        minute = 0

    if what.endswith('begins shift'):
        current_guard = guard
        current_awake = 0
    elif what == 'falls asleep':
        current_asleep = minute
    elif what == 'wakes up':
        if current_guard not in guards:
            guards[current_guard] = [0 for i in range(60)]
        for i in range(current_asleep, minute):
            guards[current_guard][i] += 1
        current_asleep = None

guard_total_minutes = dict(zip (guards.keys(), [sum(guards[guard]) for guard in guards]))
find_max = [None, 0]
for guard in guards:
    if guard_total_minutes[guard] > find_max[1]:
        find_max = [guard, guard_total_minutes[guard]]
print (find_max)
max_guard = find_max[0]

max_guard = max(guards.items(), key=lambda x: x[1])
print (max_guard)

max_minute = max(enumerate(max_guard[1]), key=lambda x: x[1])
print (max_minute)

print (int(max_guard[0]) * max_minute[0])

find_max = [0, None, None]
for guard in guards:
    for i in range(60):
        if guards[guard][i] > find_max[0]:
            find_max = [guards[guard][i], guard, i]

print (find_max)
print (int(find_max[1]) * find_max[2])
