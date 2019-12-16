import sys
import numpy

with open("input.txt", "r") as f:
    data = [int(x) for x in list(f.readline().rstrip())]

def fft1(numbers):
    def gen_multiplier(i, max_length):
        pattern = [0, 1, 0, -1]

        m = []

        skip_one = 1
        while True:
            for x in range(4):
                m += [pattern[x] for a in range(i - skip_one)]
                skip_one = 0
                if len(m) >= max_length:
                    return m

    newlist = [0 for i in range(len(numbers))]
    for i in range(len(numbers)):
        mask = gen_multiplier(i+1, len(numbers))

        for z in range(len(numbers)):
            newlist[i] += numbers[z] * mask[z]
        newlist[i] = abs(newlist[i]) % 10

    return newlist


def fft2(numbers, newlist, offset):
    max_len = len(numbers)

    full_sum = sum(numbers[i] for i in range(offset, max_len))
    for i in range(offset, max_len):
        newlist[i] = abs(full_sum) % 10
        full_sum -= numbers[i]

    return newlist

## Part ONE
for i in range(100):
    data = fft1(data)

data = data[0:8]

print("Part ONE:")
print(''.join([str(x) for x in data]))

## Part TWO
with open("input.txt", "r") as f:
    data = [int(x) for x in list(f.readline().rstrip())]
data = data * 10000
offset = int(''.join([str(x) for x in data[0:7]]))
newlist = [0 for i in range(len(data))]

for i in range(100):
    newlist = fft2(data, newlist, offset)

    t = newlist
    newlist = data
    data = t

data = data[offset:offset+8]

print("Part TWO:")
print(data)
print(''.join([str(x) for x in data]))
