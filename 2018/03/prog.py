import sys
import re

class Claim(object):
    r = re.compile(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$")
    def __init__(self, line=None):
        if line is not None:
            matches = Claim.r.match(line)
            self.id = int(matches[1])

            self.x = int(matches[2])
            self.y = int(matches[3])

            self.w = int(matches[4])
            self.h = int(matches[5])

            self.x2 = self.x + self.w - 1
            self.y2 = self.y + self.h - 1

    def contains(self, x, y):
        return x >= self.x and x <= self.x2 and \
               y >= self.y and y <= self.y2

    def intersect(self, other):
        if (self.x > other.x2) or (self.x2 < other.x) or \
           (self.y > other.y2) or (self.y2 < other.y):
            return None

        x = max(self.x, other.x)
        x2 = min(self.x2, other.x2)
        y = max(self.y, other.y)
        y2 = min(self.y2, other.y2)

        return (x, y, x2, y2)

    def __str__(self):
        return (f'#{self.id} @ {self.x},{self.y}: {self.w}x{self.h}: {self.x2} {self.y2}')


def safe_remove(list, value):
    try:
        list.remove(value)
    except:
        pass

with open("input.txt", "r") as f:
    lines = [x.strip() for x in f.readlines()]

claims = [Claim(x) for x in lines]

clean = [claim.id for claim in claims]

overlapped = set()
for i1, claim1 in enumerate(claims):
    for i2, claim2 in enumerate(claims):
        if i2 <= i1:
            continue

        overlap = claim1.intersect(claim2)

        if overlap is not None:
            safe_remove(clean, claim1.id)
            safe_remove(clean, claim2.id)
            for x in range(overlap[0], overlap[2]+1):
                for y in range(overlap[1], overlap[3]+1):
                    overlapped.add((x,y))


print (len(overlapped))
print (clean)
