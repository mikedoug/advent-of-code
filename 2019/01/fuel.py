import sys

def fuel(mass):
    extra = int(int(mass)/3) - 2
    if extra > 0:
        return extra + fuel(extra)
    else:
        return 0

tally = 0

for mass in sys.stdin:
    tally += fuel(mass)

print(tally)
