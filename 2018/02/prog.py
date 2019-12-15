import sys
from collections import Counter

with open("input.txt", "r") as f:
    ids = [x.strip() for x in f.readlines()]

twos = 0
threes = 0

for id in ids:
    counter = Counter(id)
    if 2 in counter.values():
        twos += 1
    if 3 in counter.values():
        threes += 1
        
print (twos * threes)

for i, id1 in enumerate(ids):
    for id2 in ids[i+1:]:
        diff = 0
        for ic, c in enumerate(id1):
            if c != id2[ic]:
                diff += 1
                if diff > 1:
                    break
        if diff == 1:
            print (f'ids: {id1} {id2}')