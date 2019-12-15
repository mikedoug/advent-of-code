import sys

with open("input.txt", "r") as f:
    values = [int(x.strip()) for x in f.readlines()]

print (sum(values))

frequencies = set([0])
f = 0
while True:
    for value in values:
        f += value
        if f in frequencies:
            print (f)
            exit(0)
        frequencies.add(f)
