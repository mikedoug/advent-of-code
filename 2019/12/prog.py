import re
import hashlib
import itertools
import math
from functools import reduce

class Moon(object):
    def __init__(self, name, position, velocity=(0,0,0)):
        self.position = position
        self.name = name
        self.velocity = velocity

    def apply_gravity_from(self, other):
        if self != other:
            self.velocity = (
                self.velocity[0] + (-1 if other.position[0] < self.position[0] else 1 if other.position[0] > self.position[0] else 0),
                self.velocity[1] + (-1 if other.position[1] < self.position[1] else 1 if other.position[1] > self.position[1] else 0),
                self.velocity[2] + (-1 if other.position[2] < self.position[2] else 1 if other.position[2] > self.position[2] else 0)
            )

    def move(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
            self.position[2] + self.velocity[2]
        )
    
    def energy(self):
        return sum([abs(x) for x in self.position]) * sum([abs(x) for x in self.velocity])

    def print(self):
        print (self.get_string())

    def get_string(self, n=None):
        if n is None:
            return f'{self.name:10}: {self.position} {self.velocity}'
        else:
            return f'{self.name:10}: {self.position[n]} {self.velocity[n]}'

    def get_serialize(self):
        return [self.name, self.position, self.velocity]

    def short_string(self):
        return f'[{self.position}, {self.velocity}]'


class SingleAxisMoon(object):
    def __init__(self, name, position, velocity=0):
        self.position = position
        self.name = name
        self.velocity = velocity

    def apply_gravity_from(self, other):
        if self != other:
            self.velocity += (-1 if other.position < self.position else 1 if other.position > self.position else 0)

    def move(self):
        self.position += self.velocity
    
    def print(self):
        print (self.get_string())

    def get_string(self):
        return f'{self.name:10}: {self.position} {self.velocity}'


moons = []
with open("input.txt", "r") as f:
    reg = re.compile("^<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>")
    moonnames = ['Io', 'Europa', 'Ganymede', 'Callisto']
    for i, line in enumerate(f):
        matches = re.match(reg, line.strip())
        moons.append(Moon(moonnames[i], (int(matches[1]), int(matches[2]), int(matches[3]))))

print("Part ONE")
print("Original: ")
[x.print() for x in moons]

for step in range(1000):
    for moon in moons:
        [moon.apply_gravity_from(x) for x in moons]

    [moon.move() for moon in moons]

print()
print(f"Step: {step+1}")
[x.print() for x in moons]
energy=sum([x.energy() for x in moons])
print(f'Energy: {energy}')



print()
print("Part TWO")

axis_data = []
for axis in range(3):
    moons = []
    with open("input.txt", "r") as f:
        reg = re.compile("^<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>")
        moonnames = ['Io', 'Europa', 'Ganymede', 'Callisto']
        for i, line in enumerate(f):
            matches = re.match(reg, line.strip())
            moons.append(SingleAxisMoon(moonnames[i], int(matches[axis+1])))

    orig_data = [(moon.position, moon.velocity) for moon in moons]

    for step in itertools.count(start=1):
        for moon in moons:
            [moon.apply_gravity_from(x) for x in moons]
        [moon.move() for moon in moons]

        step_data = [(moon.position, moon.velocity) for moon in moons]

        if step_data == orig_data:
            print (f"Original state for axis {axis} found at step {step}")
            axis_data.append(step)
            break

answer = reduce(lambda x, y: x * y // math.gcd(x,y), axis_data)
print (f"Step 2 answer: {answer}")